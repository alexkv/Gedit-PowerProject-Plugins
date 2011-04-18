import gedit
import gtk
import os
from pp_core import debug
from windowhelper import WindowHelper
from commands import Commands

class PowerProjectHotkeysPlugin(gedit.Plugin):

	def __init__(self):
		gedit.Plugin.__init__(self)
		debug.msg(os.path.join(os.path.dirname(__file__), 'hotkeys'))
		Commands().set_dirs([
			os.path.expanduser('~/.gnome2/gedit/powerproject/hotkeys'),
			os.path.join(os.path.dirname(__file__), 'hotkeys'),
		])
		self.window = None


	def activate(self, window):
		debug.msg('PowerProjectHotkeysPlugin activating')
		self.window = WindowHelper(self, window)


	def deactivate(self, window):
		debug.msg('PowerProjectHotkeysPlugin deactivating')
		self.window = None


	def update_ui(self, window):
		self.window.update_ui()



