# -*- coding: utf-8 -*-

#  Copyright (C) 2009 - Jesse van den Kieboom
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330,
#  Boston, MA 02111-1307, USA.

import os
import gtk
import gio
import glib
import gedit.commands
from pp_core import debug, get_core

from popup import Popup

ui_str = """<ui>
  <menubar name="MenuBar">
    <menu name="FileMenu" action="File">
      <placeholder name="FileOps_2">
				<menuitem name="APQuickOpen" action="APQuickOpen"/>
      </placeholder>
    </menu>
  </menubar>
</ui>
"""

class WindowHelper:
	def __init__(self, window, plugin, search_func):
		self._window = window
		self._plugin = plugin

		self._search_func = search_func

		self._popup = None
		self._install_menu()


	def deactivate(self):
		self._uninstall_menu()
		self._window = None
		self._plugin = None


	def update_ui(self):
		pass


	def _uninstall_menu(self):
		manager = self._window.get_ui_manager()
		manager.remove_ui(self._ui_id)
		manager.remove_action_group(self._action_group)
		manager.ensure_update()


	def _install_menu(self):
		manager = self._window.get_ui_manager()
		self._action_group = gtk.ActionGroup("GeditAPQuickOpenPluginActions")
		self._action_group.add_actions([
			("APQuickOpen", gtk.STOCK_OPEN, _("Axy Quick open"),
			 '<Ctrl><Alt>O', _("Axy Quickly open documents"),
			 self.on_quick_open_activate)
		])

		manager.insert_action_group(self._action_group, -1)
		self._ui_id = manager.add_ui_from_string(ui_str)


	def _create_popup(self):
		self._popup = Popup(self._window, self.on_result, self._search_func)
		self._popup.set_default_size(*self._plugin.get_popup_size())
		self._popup.set_transient_for(self._window)
		self._popup.set_position(gtk.WIN_POS_CENTER_ON_PARENT)

		self._window.get_group().add_window(self._popup)
		self._popup.connect('destroy', self.on_popup_destroy)


	def on_quick_open_activate(self, action):
		if not self._popup:
			self._create_popup()

		self._popup.show()


	def on_popup_destroy(self, popup):
		alloc = popup.get_allocation()
		self._plugin.set_popup_size((alloc.width, alloc.height))
		self._popup = None


	def on_result(self, path):
		path = os.path.join(get_core(self._window).get_path(), path)
		uri = gio.File(path).get_uri()
		gedit.commands.load_uri(self._window, uri, None, -1)
		return True


