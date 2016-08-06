from menusystem import MenuSystem
from handlers import *

"""Project 1

   Author: Daniel Mikusa <dan@trz.cc>
Copyright: April 4, 2006

Sample project to demonstrate the use of the MenuSystem set of classes.

In effect this project will create a menu with a few choices, some sub-menus, 
etc...

When run the user can then navigate through the system.
"""

"""Create A Menu and Sub Menu by hand"""
# Create Sub Menu
lst = []
lst.append(MenuSystem.Choice(selector=1, value=1, handler=print_ok, description='Sub Menu Do Noting Some'))
lst.append(MenuSystem.Choice(selector=2, value=2, handler=print_ok, description='Sub Menu Do Noting More'))
lst.append(MenuSystem.Choice(selector=3, value=3, handler=print_bad, description='Sub Menu Do Noting Alot'))
lst.append(MenuSystem.Choice(selector=4, value=4, handler=done, description='Return to Main Menu'))
sub = MenuSystem.Menu(title='Sub Menu', choice_list=lst, prompt='Select Choice.> ')

# Create Some Choices
lst = []
lst.append(MenuSystem.Choice(selector=1, value=1, handler=print_ok, description='Do Noting Some'))
lst.append(MenuSystem.Choice(selector=2, value=2, handler=None, description='Do Noting More'))
lst.append(MenuSystem.Choice(selector=3, value=3, handler=print_bad, description='Do Noting Alot'))
lst.append(MenuSystem.Choice(selector=4, value=4, handler=None, description='Sub Menu', subMenu=sub))
lst.append(MenuSystem.Choice(selector=5, value=5, handler=done, description='Exit'))

# Creat Menu & Begin Execution
head = MenuSystem.Menu(title='Main Menu', choice_list=lst, prompt='Select Choice.> ')
head.waitForInput()

"""Save Menu To XML"""
# Save Menu
xml = MenuSystem.XMLMenuGenie('save.xml', 'handlers')
xml.save(head)
head2 = xml.load()
head2.waitForInput()

"""Load Menu from XML"""
# Load Menu
#loader = MenuSystem.XMLMenuGenie('save.xml', 'choice_handlers')
#head2 = loader.load()
#head2.waitForInput()


