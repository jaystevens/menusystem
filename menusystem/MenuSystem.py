"""
Copyright (C) 2006  Daniel Mikusa

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
"""
import sys, xml.dom.minidom
"""Menu System

   Author:  Daniel Mikusa <dan@trz.cc>
Copyright:  April 4, 2006

A Menu System is a group of Menu and Choice Object arranged to provide a text
based interface for an end user.  These classes are aimed at making
development of Menu based systems easy and fast.

A Menu System is orgainzed into a heirarchy.  There is a top level Menu object,
which has a set of choices.  Any / All / None of this Menu's Choice objects can
contain sub-menus.  The Menu System heirarchy is extended downward by creating
Menu objects with Choice objects that have sub-menus.  As is natural, each 
Choice object can only have one sub-menu, but each Menu can have many Choice
objects.
"""
class Menu:
	"""Represents one level of a menu system
	
	A Menu System consists of one or more Menus.  Each Menu consists of a
	title, choices, and a prompt.  A Menu is required to have a title, a prompt
	and at least one choice.  There is no technical limit to the number of
	choices per menu, but asteticly and organizationally more than 10 will
	likely cause problems and should be divided into sub-menus.
	
	A Menu object is capable of displaying itself and of retreiving a choice
	from the user.  Both function only needs to be called on the top
	level menu object.  The calls will trickle down to all of the menu object
	beneath it in the heirarchy as needed.
	"""
	def __init__(self, title='', choice_list=[], prompt=''):
		"""Setup a new menu object
		
		Allows a new Menu object to be easily created by passing the required
		values into a constructor.  All parameters are optional.
		
			      title -- Menu object's title
			     prompt -- Menu object's prompt
			choice_list -- List of Choice object for Menu
		"""
		self.title = title
		self.choices = choice_list
		self.prompt = prompt
		
	def __getitem__(self, key):
		"""Overloads the [] operator for Menu object to get Choices
		
		Allows us to select a choice from a Menu object using the [] operator.
		print s['3'].  This is mostly a convenience, mostly.
		
		Given a string 'x', returns the Choice object that has the selector 'x'.
		"""
		if isinstance(key, str) and key in self.choices:
			return self.choices[self.choices.index(key)]
	
	def __repr__(self):
		"""Prints the Menu to Standard Out
		
		Prints the current Menu and triggers a recursive call to all sub-menus
		that are part of this Menu heirarchy.
		
		The format for display is as follows:
			
			TITLE
			
			choice 1
			choice ...
			choice n
			
			PROMPT
			
		A Choice object will handle its own formatting, all that is required is
		to call the Choice object's display function.
		"""
		if not self.choices:
			return "Please create some choices for this menu"
		tmp = "\n%s\n\n" % self.title
		for choice in self.choices:
			tmp += "\t%s\n" % str(choice)
		tmp += "\n%s" % self.prompt
		return tmp
		
	def waitForInput(self):
		"""Main event loop, progresses indefinitly
		
		Starts the main event loop for the menu system, which consists of 
		getting input from standard input, validating it, and calling the proper
		handler function.  Once the handler function returns we continue
		this process indefinitly.
		
		This process will loop forever, unless you create a return level / exit
		option for the user.  To return a level, or exit if it is the top level
		just return False from the handler function.
		"""
		loop = True
		while loop != False:
			print self,
			c = sys.stdin.readline().strip()
			if c in self.choices:
				if self[c].handler:
					loop = self[c].handler(self[c].value)
				if self[c].subMenu:
					self[c].subMenu.waitForInput()


class Choice:
	"""
	Represents one option of a Menu
	
	Each Menu requires one or more Choices.  A Choice consists of a selector,
	a description, a value, and a sub-menu.  The selector, description, and
	value are required, while the sub-menu is optional.
	
	The presence of a sub-menu will alter the way the Choice is displayed to
	indicate it is a sub-menu to the end user.
	
	A Choice object is capable of displaying itself and provides instructions
	on what to do if the Choice object is selected.
	"""
	def __init__(self, selector=1, description='',
						value=None, subMenu=None, handler=None):
		"""Setup a new Choice object
		
		Allows a new Choice object to be easily created by specifying the
		required values to the constructor.  All parameters are optional.
		
		Here are the parameters:
			
			   selector -- value that a user will enter to select a Choice
			description -- value that explains job this Choice will accomplish.
			      value -- value of the selected Choice.
			    subMenu -- the Menu object that will be triggered if this Choice
				           is selected.
			    handler -- the function that will be executed if this Choice
				           is selected.
		
		The handler function will be executed even if the Choice object contains
		a sub-menu.  The handler function will be executed, and then control
		will be switched to the handler function.
		
		The handler function will be passed a single parameter containing the 
		value of the Choice object that was selected.  This can be used to find
		out what choice was selected by the end user.  This value will always
		be a string.
		
		The handler function should never return 'False' unless the desired
		effect is to either go up one level in the menu heirarchy or exit if it
		is at the top level of the menu heirarchy.  If the handler returns 
		anything else it is ignored.  Returning True or None are typically best
		and will keep you at the same menu level, Returning False will return
		one level.
		"""
		self.selector = selector
		self.description = description
		self.value = str(value)
		self.subMenu = subMenu
		self.handler = handler
	
	def __repr__(self):
		"""Prints the Choice to Standard Out
		
		The format for display is as follows:
			
			SELECTOR.) DESCRIPTION
			
		If the Choice has a sub-menu it will be displayed as follows:
			
			SELECTOR.) DESCRIPTION **
		
		DO NOT INCLUDE END OF LINE CHARACTERS!
		"""
		if not self.selector or not self.description:
			return "Menu needs to be defined before it can be printed."
		if not self.subMenu:
			return "%s.) %s" % (self.selector, self.description)
		else:
			return "%s.) %s **" % (self.selector, self.description)

	def __eq__(self, ch):
		"""Overloads the == operator for Choice object
		
		This allows us to determine if two Choice objects are equal by saying 
		choiceA == choiceB.  This is mostly a convenience, mostly.
		"""
		if isinstance(ch, str):
			return ch == str(self.selector)


class MenuGenie:
	"""Generic Interface for loading and saving Menu Systems.
	
	Defines an Interface for loading and saving Menu Systems.  This is just
	an Interface, it doesn't define how the Menu System is stored.
	
	To implement this interface you need to define two functions:  load and
	save.  As you would expect, load will create a menu from permanent storage
	and return the top level Menu object.  Save takes a Menu object as
	a parameter and will write that Menu object and all sub-menus to permanent
	storage.
	"""
	def load(self):
		"""Load a Menu object from permanent storage
		
		Load and create a Menu object from permanent storage.  This is simply a
		place holder, and needs to be overloaded in a derived class.  Returns
		a menu object that is loaded.
		"""
		pass
		
	def save(self, menu):
		"""Writes a Menu object to permanent storage
		
		Write an existing Menu object and all sub-mens to permenant storage.
		This is simply a place holder, and needs to be overloaded in a derived
		class.  Parameter menu is the menu object to write.
		"""
		pass


class XMLMenuGenie(MenuGenie):
	"""Loads and Saves Menu Systems to XML
	
	Implements the MenuGenie Interface allowing Menu Systems to be saved as
	XML files.  The format of the XML file is as follows:
		
		<menu>  -  represents a menu object (valid anywhere).  Must contain at
					least one choice object.  Title and prompt attributes are
					required.
			attribute list
				title  -  menu title
				prompt -  menu prompt

		<choice> - represents a choice object (only valid in menu tag).  A
					choice object may contain one and only one menu object.
					If the choice object contains a menu object, then the choice
					object becomes a sub-menu.  All attributes are valid for 
					regular choices and sub-menus.  Selector, description, and
					handler attributes are required.  If value is not specified
					then value will be set to equal selector.
			attribute list
				   selector -  used to determine if an object is selected
				description -  text to describe object to end user
				      value -  value representation passed to handler function
					handler -  name of python function to call when selected
	
	The use of other tags will trigger an error.  The use of unspecified
	attributes will not result in an error, they will be ignored.
	"""
	def __init__(self, loc, module_name):
		"""Initalize the XMLGenie Object
		
		Parameter loc sets the location of the XML file that will be read or
		written to.  Parameter module_name should be the module that defines 
		all of the functions that are used to handle menu choices.
		"""
		self.loc = loc
		self.module = __import__(module_name)
		
	def load(self):
		"""Load a Menu System from XML File
		
		Loads a Menu System from an XML file in the above specified format.  The
		parameter location is used to specify where to find the XML.  It can be
		a file object, the path to a local file, a URL, or the actual XML as
		a Python String.
		
		After the XML is processed, a Menu object is returned which contains
		the top level menu of the Menu System.
		"""
		fp = self._open('r')
		doc = xml.dom.minidom.parse(fp)
		fp.close()
		m = self._load(doc.documentElement)
		doc.unlink()
		return m
		
	def _load(self, head):
		"""Creates all menu object recursivly
		
		Starting at the document root, processes all menu tags thus building
		the menu system.
		
		Each meun tag is processed for it's attributes and contained choices.
		If one of the menu's choices is itself a [sub]menu, then recursivly
		process all of that menu's attributes and choices.
		
		The parameter to this function is the xml an menu tag object.  Start 
		with the document root, and recursivly progress down through submenus.
		
		The return value of this function is the head Menu object representing
		the entire menu system.
		"""
		choice_list = []
		for child in [x for x in head.childNodes if isinstance(x, xml.dom.minidom.Element) and x.tagName.lower() == 'choice']:
			c = Choice()
			c.selector = int(child.getAttribute('selector'))
			c.description = child.getAttribute('description')
			c.value = child.getAttribute('value')
			handler_name = child.getAttribute('handler')
			if handler_name != 'None':
				c.handler = getattr(self.module, handler_name)
			else:
				c.handler = None
			if child.hasChildNodes():
				tmp_m = [x for x in child.childNodes if isinstance(x, xml.dom.minidom.Element) and x.tagName.lower() == 'menu']
				try:
					c.subMenu = self._load(tmp_m[0])
				except IndexError:
					pass
			choice_list.append(c)
		return Menu(title=head.getAttribute('title'), prompt=head.getAttribute('prompt'), choice_list=choice_list)
	
	def save(self, menu):
		"""Saves a Menu System to XML File
		
		Saves a complete Menu System and all sub-menus to an XML file in the
		above specified format.  The parameter location is used to specify
		where the file is written to.  It can be a file object, the path to a
		local file or a string which will be set with the actual XML.
		
		Note unlike the load function, you cannot save to a URL.
		"""
		self.doc = xml.dom.minidom.Document()
		self.doc.appendChild(self._save(menu))
		fp = self._open('w')
		if fp:
			self.doc.writexml(fp,addindent='\t', newl='\n')
			fp.close()
		else:
			print 'Unable to output xml'
		self.doc.unlink()
		
	def _save(self, menu):
		"""Helper function for Saving
		
		Helper function to implement recursion for traversing the Menu System.
		
		Parameter menu is the current menu object.
		
		Returns the menu xml element
		"""
		m = self.doc.createElement('menu')
		m.setAttribute('title', str(menu.title))
		m.setAttribute('prompt', str(menu.prompt))
		for choice in menu.choices:
			c = self.doc.createElement('choice')
			c.setAttribute('selector', str(choice.selector))
			c.setAttribute('description', str(choice.description))
			c.setAttribute('value', str(choice.value))
			if choice.handler:
				c.setAttribute('handler', choice.handler.func_name)
			else:
				c.setAttribute('handler', 'None')
			if choice.subMenu:
				c.appendChild(self._save(choice.subMenu))
			m.appendChild(c)
		return m
		
	def _open(self, mode):
		"""Open any location for reading or writing
		
		Helper function to open a file, url, or string for reading or writing.
		Used in conjunction with the save and load functions.
		
		Valid options for mode are 'w' for write and 'r' for read.  There is no
		need for append.
		
		The src parameter can be any valid url, file location, string, or file
		object.
		
		This method was borrowed from
			http://www.diveintopython.org/xml_processing/index.html, and
		modified slightly.
		
		The return value will be a file object unless there is an error.  In
		that case the return value will equal None.
		"""
		mode = mode.lower()
		if mode not in ('w', 'r'):
			return None
		
		if self.loc == '-' and mode == 'w':
			return sys.stdout
		if self.loc == '-' and mode == 'r':
			return sys.stdin
		
		if hasattr(self.loc, 'read') and mode == 'r':
			return self.loc
		if hasattr(self.loc, 'write') and mode == 'w':
			return self.loc
		
		if mode == 'r':
			import urllib
			try:
				return urllib.urlopen(self.loc)
			except (IOError, OSError):
				pass
		
		try:
			return open(self.loc, mode)
		except (IOError, OSError):
			pass

		if type(self.loc) == str:
			import StringIO
			return StringIO.StringIO(self.loc)
			
		return None

