import gtk
from pp_core import debug
from command_handler import CommandHandler 

class WindowHelper:
	handlers = {}
	status_label = None

	def __init__(self, plugin, window):
		self.window = window
		self.plugin = plugin
		self.command_handler = CommandHandler()

		self.set_status()

		for view in window.get_views():
			self.connect_handlers(view)
		
		window.connect('tab_added', self.on_tab_added)


	def deactivate(self):
		debug.msg('deactivate function called')
		for view in self.handlers:
			view.disconnect(self.handlers[view])
		
		self.window = None
		self.plugin = None


	def update_ui(self):
		self.set_status()


	def connect_handlers(self, view):
		handler = view.connect('key-press-event', self.on_key_press)
		self.handlers[view] = handler


	def on_tab_added(self, window, tab):
		self.connect_handlers(tab.get_view())


	def set_status(self, text=None):
		if not self.status_label:
			self.status_label = gtk.Label('PP')
			self.status_label.set_alignment(0, 1)
			self.status_label.show()
			frame = gtk.Frame()
			frame.add(self.status_label)
			frame.show()
			statusbar = self.window.get_statusbar()
			statusbar.add(frame)

		label = ''

		if text:
			label = "AP: %s " % (text)

		self.status_label.set_text(label)



	def on_key_press(self, view, event):
		hotkey = {
			'ctrl' : False,
			'shift' : False,
			'alt' : False,
			'key' : event.keyval
		}
		
		if event.state & gtk.gdk.CONTROL_MASK:
			hotkey['ctrl'] = True
		
		if event.state & gtk.gdk.SHIFT_MASK:
			hotkey['shift'] = True
		
		if event.state & gtk.gdk.MOD1_MASK:
			hotkey['alt'] = True


		result = self.command_handler.handle(hotkey, view)
		status_text = self.command_handler.get_status_text()
		debug.msg('set status: %s' % status_text) 
		self.set_status(status_text)
		return result


