import keys
from pp_core import debug
from commands import Commands

class CommandHandler:

	__command_group = None
	__status_text = None

	def __init__(self):
		pass


	def handle(self, hotkey, view):

		if self._wait_for_subcommand() :
			return self._handle_subcommand(hotkey, view)
		else:
			return self._set_command_group(hotkey)



	def get_status_text(self):
		text = ''
		if self.__command_group:
			text = self.__command_group
		elif self.__status_text:
			text = self.__status_text
			self.__status_text = ''

		return text



	def _set_command_group(self, hotkey):
		group = self._hotkey2command_group(hotkey)

		if not self._is_command_group_exists(group):
			return False

		self.__command_group = group
		return True



	def _is_command_group_exists(self, key):
		return Commands().command_exists(key)



	def _handle_subcommand(self, hotkey, view):
		if keys.is_cancel_key(hotkey['key']):
			self._reset()
			return False

		key = keys.get_key_name(hotkey['key'])
		self.__status_text = Commands().execute(self.__command_group, key, view)

		self._reset()
		return True



	def _wait_for_subcommand(self):
		return self.__command_group is not None



	def _reset(self):
		debug.msg('CommandHandler reset')
		self.__command_group = None



	def _hotkey2command_group(self, hotkey):
		s = ''
		
		if hotkey['ctrl']:
			s += 'ctrl-'

		if hotkey['shift']:
			s += 'shift-'

		if hotkey['alt']:
			s += 'alt-'

		s += keys.get_key_name(hotkey['key'])

		return s




