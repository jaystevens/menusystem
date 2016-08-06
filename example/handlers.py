"""Menu Handlers

   Author: Daniel Mikusa <dan@trz.cc>
Copyright: April 5, 2006

Define all of you choice handler functions in a seperate module

You must define all of you choice handler functions in a seperate file.  This
is a good idea because it seperates your business logic code from your
presentation code and because it is technically required for the Menu System
to be able to find your functions.

For Function 'X' in module 'Y'

	Choice(selector=1, value=1, handler=X.Y, description='Do Something!')
"""
# Define Some Handler Functions
def print_ok(val):
	print 'OK: %s' % val
	
def print_bad(val):
	print 'BAD: %s' % val

def done(val):
	return False
	
def submenu_handler(val):
	print 'Going to submenu'

