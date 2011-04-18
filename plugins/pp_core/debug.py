import os
import time

path = os.path.expanduser('~/.gnome2/gedit/powerproject/debug.log')
debug_off = os.getenv('PP_DEBUG') != '1'

def msg(text):
	if debug_off:
		return

	f = open(path, 'a+')
	current = time.strftime("%a, %d %b %Y %H:%M:%S:  ")
	f.write(current)
	f.write(str(text))
	f.write("\r\n")
	f.close()
