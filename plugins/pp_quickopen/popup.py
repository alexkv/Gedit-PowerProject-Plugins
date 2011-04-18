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

import gtk
import gtk.gdk
import gobject
import os
import pango
import glib
import fnmatch
import xml.sax.saxutils
from pp_core import debug


class Popup(gtk.Dialog):
	def __init__(self, window, handler, search_func = None):
		gtk.Dialog.__init__(self,
				    title=_('Quick Open'),
				    parent=window,
				    flags=gtk.DIALOG_DESTROY_WITH_PARENT | gtk.DIALOG_NO_SEPARATOR | gtk.DIALOG_MODAL)

		self.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
		self._open_button = self.add_button(gtk.STOCK_OPEN, gtk.RESPONSE_ACCEPT)

		self._handler = handler
		self._window = window
		self._search = search_func
		self._build_ui()

		self._theme = None
		self._cursor = None
		self._shift_start = None

		accel_group = gtk.AccelGroup()
		accel_group.connect_group(gtk.keysyms.l, gtk.gdk.CONTROL_MASK, 0, self.on_focus_entry)

		self.add_accel_group(accel_group)


	def _build_ui(self):
		vbox = self.get_content_area()
		vbox.set_spacing(3)

		self._entry = gtk.Entry()

		self._entry.connect('changed', self.on_changed)
		self._entry.connect('key-press-event', self.on_key_press_event)

		sw = gtk.ScrolledWindow(None, None)
		sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		sw.set_shadow_type(gtk.SHADOW_OUT)

		tv = gtk.TreeView()
		tv.set_headers_visible(False)

		self._store = gtk.ListStore(int, str)
		tv.set_model(self._store)

		self._treeview = tv
		tv.connect('row-activated', self.on_row_activated)

		renderer = gtk.CellRendererText()
		column = gtk.TreeViewColumn()

		column.pack_start(renderer, True)
		column.set_attributes(renderer, markup = 1)

		column.set_cell_data_func(renderer, self.on_cell_data_cb)

		tv.append_column(column)
		sw.add(tv)
		
		selection = tv.get_selection()
		selection.connect('changed', self.on_selection_changed)
		selection.set_mode(gtk.SELECTION_MULTIPLE)

		vbox.pack_start(self._entry, False, False, 0)
		vbox.pack_start(sw, True, True, 0)

		lbl = gtk.Label()
		lbl.set_alignment(0, 0.5)
		lbl.set_ellipsize(pango.ELLIPSIZE_MIDDLE)
		self._info_label = lbl

		vbox.pack_start(lbl, False, False, 0)

		# Initial selection
		self.on_selection_changed(tv.get_selection())
		vbox.show_all()


	def on_cell_data_cb(self, column, cell, model, piter):
		path = model.get_path(piter)
		
		if self._cursor and path == self._cursor.get_path():
			style = self._treeview.get_style()
			bg = style.bg[gtk.STATE_PRELIGHT]
			
			cell.set_property('cell-background-gdk', bg)
			cell.set_property('style', pango.STYLE_ITALIC)
		else:
			cell.set_property('cell-background-set', False)
			cell.set_property('style-set', False)


	def normalize_relative(self, parts):
		if not parts:
			return []

		out = self.normalize_relative(parts[:-1])

		if parts[-1] == '..':
			if not out or (out[-1] == '..') or len(out) == 1:
				out.append('..')
			else:
				del out[-1]
		else:
			out.append(parts[-1])

		return out


	def _append_to_store(self, item):
		if not item in self._stored_items:
			self._store.append(item)
			self._stored_items[item] = True


	def _clear_store(self):
		self._store.clear()
		self._stored_items = {}



	def _remove_cursor(self):
		if self._cursor:
			path = self._cursor.get_path()
			self._cursor = None

			self._store.row_changed(path, self._store.get_iter(path))



	def do_search(self):
		self.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
		self._remove_cursor()

		text = self._entry.get_text().strip()
		self._clear_store()
		
		if text:
			for row in self._search(text, self._window):
				self._append_to_store((0, row))

		piter = self._store.get_iter_first()

		if piter:
			self._treeview.get_selection().select_path(self._store.get_path(piter))

		self.window.set_cursor(None)


	def do_show(self):
		gtk.Window.do_show(self)

		self._entry.grab_focus()
		self._entry.set_text("")

		self.do_search()


	def on_changed(self, editable):
		self.do_search()
		self.on_selection_changed(self._treeview.get_selection())


	def _shift_extend(self, towhere):
		selection = self._treeview.get_selection()
		
		if not self._shift_start:
			model, rows = selection.get_selected_rows()
			start = rows[0]

			self._shift_start = gtk.TreeRowReference(self._store, start)
		else:
			start = self._shift_start.get_path()

		selection.unselect_all()
		selection.select_range(start, towhere)


	def _select_index(self, idx, hasctrl, hasshift):
		path = (idx,)
		
		if not (hasctrl or hasshift):
			self._treeview.get_selection().unselect_all()
		
		if hasshift:
			self._shift_extend(path)
		else:
			self._shift_start = None
			
			if not hasctrl:
				self._treeview.get_selection().select_path(path)

		self._treeview.scroll_to_cell(path, None, True, 0.5, 0)
		self._remove_cursor()

		if hasctrl or hasshift:
			self._cursor = gtk.TreeRowReference(self._store, path)
			
			piter = self._store.get_iter(path)
			self._store.row_changed(path, piter)


	def _move_selection(self, howmany, hasctrl, hasshift):
		num = self._store.iter_n_children(None)

		if num == 0:
			return True

		# Test for cursor
		path = None
		
		if self._cursor:
			path = self._cursor.get_path()
		else:
			model, rows = self._treeview.get_selection().get_selected_rows()
			
			if len(rows) == 1:
				path = rows[0]

		if not path:
			if howmany > 0:
				self._select_index(0, hasctrl, hasshift)
			else:
				self._select_index(num - 1, hasctrl, hasshift)
		else:
			idx = path[0]

			if idx + howmany < 0:
				self._select_index(0, hasctrl, hasshift)
			elif idx + howmany >= num:
				self._select_index(num - 1, hasctrl, hasshift)
			else:
				self._select_index(idx + howmany, hasctrl, hasshift)

		return True


	def _activate(self):
		model, rows = self._treeview.get_selection().get_selected_rows()
		ret = True
		
		for row in rows:
			s = model.get_iter(row)
			info = model.get(s, 1)
			debug.msg(str(info))
			ret = True and self.	_handler(info[0])

		if rows and ret:
			self.destroy()

		return ret


	def toggle_cursor(self):
		if not self._cursor:
			return
		
		path = self._cursor.get_path()
		selection = self._treeview.get_selection()
		
		if selection.path_is_selected(path):
			selection.unselect_path(path)
		else:
			selection.select_path(path)


	def on_key_press_event(self, widget, event):
		move_mapping = {
			gtk.keysyms.Down: 1,
			gtk.keysyms.Up: -1,
			gtk.keysyms.Page_Down: 5,
			gtk.keysyms.Page_Up: -5
		}
		
		if event.keyval == gtk.keysyms.Escape:
			self.destroy()
			return True
		elif event.keyval in move_mapping:
			return self._move_selection(move_mapping[event.keyval], event.state & gtk.gdk.CONTROL_MASK, event.state & gtk.gdk.SHIFT_MASK)
		elif event.keyval in [gtk.keysyms.Return, gtk.keysyms.KP_Enter, gtk.keysyms.Tab, gtk.keysyms.ISO_Left_Tab]:
			return self._activate()
		elif event.keyval == gtk.keysyms.space and event.state & gtk.gdk.CONTROL_MASK:
			self.toggle_cursor()

		return False


	def on_row_activated(self, view, path, column):
		self._activate()


	def do_response(self, response):
		if response != gtk.RESPONSE_ACCEPT or not self._activate():
			self.destroy()


	def on_selection_changed(self, selection):
		model, rows = selection.get_selected_rows()
		button_active = False
		
		if len(rows) == 1:
			path = model.get(model.get_iter(rows[0]), 1)[0]
			fname = xml.sax.saxutils.escape(path)
			button_active = True
		else:
			fname = ''

		self._open_button.set_sensitive(button_active)
		self._info_label.set_markup(fname)


	def on_focus_entry(self, group, accel, keyval, modifier):
		self._entry.grab_focus()

gobject.type_register(Popup)

# ex:ts=8:et:
