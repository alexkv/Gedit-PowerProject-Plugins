# -*- coding: utf-8 -*-
# __init__.py
# This file is part of gedit Session Saver Plugin
#
# Copyright (C) 2006-2007 - Steve Frécinaux <code@istique.net>
#
# gedit Session Saver Plugin is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# gedit Session Saver Plugin is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with gedit Session Saver Plugin; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, 
# Boston, MA  02110-1301  USA

import gobject
import gtk
import gedit
import os.path
import gettext
from store import XMLSessionStore, Session
from dialogs import SaveSessionDialog, SessionManagerDialog
from pp_core.singleton import Singleton
from pp_core import debug, get_core

try:
	from gpdefs import *
	gettext.bindtextdomain(GETTEXT_PACKAGE, GP_LOCALEDIR)
	_ = lambda s: gettext.dgettext(GETTEXT_PACKAGE, s);
except:
	_ = lambda s: s

class SessionSaverWindowHelper(object):
	ACTION_HANDLER_DATA_KEY = "SessionSaverActionHandlerData"
	SESSION_MENU_PATH = '/MenuBar/FileMenu/FileOps_2/FileSessionMenu/SessionPluginPlaceHolder'
	SESSION_MENU_UI_STRING = """
		<ui>
		  <menubar name="MenuBar">
			<menu name="FileMenu" action="File">
			  <placeholder name="FileOps_2">
				<separator/>
				<menu name="FileSessionMenu" action="FileSession">
				  <placeholder name="SessionPluginPlaceHolder"/>
				  <separator/>
				  <menuitem name="FileSessionSaveMenu" action="FileSessionSave"/>
				  <menuitem name="FileSessionManageMenu" action="FileSessionManage"/>
				</menu>
			  </placeholder>
			</menu>
		  </menubar>
		</ui>"""

	def __init__(self, plugin, window):
		self.plugin = plugin
		self.window = window
		manager = window.get_ui_manager()

		self._menu_action_group = gtk.ActionGroup("SessionSaverPluginActions")
		self._menu_action_group.add_actions(
			(("FileSession", None, _("Sa_ved sessions")),
			 ("FileSessionSave", gtk.STOCK_SAVE_AS, _("_Save current session"), None, _("Save the current document list as a new session"), self.on_save_session_action),
			 ("FileSessionManage", None, _("_Manage saved sessions..."), None, _("Open the saved session manager"), self.on_manage_sessions_action)))
		manager.insert_action_group(self._menu_action_group, -1)
		self._menu_ui_id = manager.add_ui_from_string(self.SESSION_MENU_UI_STRING)

		self._ui_id = 0
		self._action_group = gtk.ActionGroup("SessionSaverPluginSessionActions")
		manager.insert_action_group(self._action_group, -1)
		self.update_session_menu()

		manager.ensure_update()

	def on_save_session_action(self, action):
		SessionDialogs().save_session(self.window)

	def on_manage_sessions_action(self, action):
		SessionDialogs().session_manager()

	def session_menu_action(self, action, session):
		SessionOperations().load(session.name, self.window)

	def remove_session_menu(self):
		if self._ui_id != 0:
			self.window.get_ui_manager().remove_ui(self._ui_id)
			self._ui_id = 0

		for action in self._action_group.list_actions():
			handler = action.get_data(self.ACTION_HANDLER_DATA_KEY)
			if handler is not None:
				action.disconnect(handler)
			self._action_group.remove_action(action)

	def update_session_menu(self):
		manager = self.window.get_ui_manager()

		self.remove_session_menu()
		self._ui_id = manager.new_merge_id()

		i = 0
		for session in self.plugin.sessions:
			action_name = 'SessionSaver%X' % i
			action = gtk.Action(action_name, session.name, _("Recover '%s' session") % session.name, None)
			handler = action.connect("activate", self.session_menu_action, session)

			action.set_data(self.ACTION_HANDLER_DATA_KEY, handler)
			self._action_group.add_action(action)

			manager.add_ui(self._ui_id, self.SESSION_MENU_PATH,
						   action_name, action_name,
						   gtk.UI_MANAGER_MENUITEM, False)
			i += 1

	def update_ui(self):
		pass

	def deactivate(self):
		manager = self.window.get_ui_manager()
		manager.remove_ui(self._menu_ui_id)
		manager.remove_action_group(self._menu_action_group)
		self.remove_session_menu()
		manager.remove_action_group(self._action_group)


class SessionSaverPlugin(gedit.Plugin):
	WINDOW_DATA_KEY = "SessionSaverWindowData"

	def __init__(self):
		super(SessionSaverPlugin, self).__init__()
		self.operations = SessionOperations(self)
		self.dialogs = SessionDialogs(self)
		self.sessions = XMLSessionStore()
		debug.msg(str(self.sessions))

	def activate(self, window):
		helper = SessionSaverWindowHelper(self, window)
		window.set_data(self.WINDOW_DATA_KEY, helper)

	def deactivate(self, window):
		self.operations.close_current_session(window)
		window.get_data(self.WINDOW_DATA_KEY).deactivate()
		window.set_data(self.WINDOW_DATA_KEY, None)

	def update_ui(self, window):
		window.get_data(self.WINDOW_DATA_KEY).update_ui()
	
	def update_session_menu(self):
		for window in gedit.app_get_default().get_windows():
			window.get_data(self.WINDOW_DATA_KEY).update_session_menu()


class SessionDialogs():
	__metaclass__ = Singleton

	def __init__(self, plugin):
		self.__plugin = plugin
	
	def save_session(self, window):
		SaveSessionDialog(window, self.__plugin).run()

	def session_manager(self):
		SessionManagerDialog(self.__plugin).run()



class SessionOperations():
	CURRENT_SESSION_NAME_KEY = 'PPCurrentSessionName'

	__metaclass__ = Singleton

	def __init__(self, plugin):
		self.plugin = plugin


	def save(self, name, window):
		files = [doc.get_uri()
					for doc in window.get_documents()
					if doc.get_uri() is not None]

		path = get_core(window).get_path()
		self.plugin.sessions.add(Session(name, files, path))
		self.plugin.sessions.save()
		self.plugin.update_session_menu()


	def load(self, name, window = None):
		session = self.plugin.sessions.get_by_name(name)
		
		if session is None:
			return

		app = gedit.app_get_default()

		if window is None:
			window = app.get_active_window()

		tab = window.get_active_tab()
		if tab is not None and \
			 not (tab.get_document().is_untouched() and \
				tab.get_state() == gedit.TAB_STATE_NORMAL):
			window = app.create_window()
			window.show()

		window.set_data(self.CURRENT_SESSION_NAME_KEY, name)
		get_core(window).set_path(session.get_path())
		gedit.commands.load_uris(window, session.files, None, 0)


	def save_current_session(self, window):
		name = window.get_data(self.CURRENT_SESSION_NAME_KEY)
		if not name:
			return
		
		debug.msg('SessionOperations save_current_session')
		self.save(name, window)

	def close_current_session(self, window):
		debug.msg('SessionOperations close_current_session')
		name = window.set_data(self.CURRENT_SESSION_NAME_KEY, None)

# ex:ts=4:et:

