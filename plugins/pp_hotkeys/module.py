import os
import sys

class Module():
	def __init__(self, name, dirname):
		self.__name = name
		self.__dirname = dirname
		self.__mod = None



	def execute(self, subcommand, view):
		self.load()
		if subcommand not in self.__mod.__dict__:
			return

		return self.__mod.__dict__[subcommand](view)


	def load(self):
		if self.__mod != None:
			return

		if self.__name in sys.modules:
			raise Exception('Module already exists...')

		oldpath = list(sys.path)

		try:
			sys.path.insert(0, self.__dirname)
			self.__mod = __import__(self.__name, globals(), locals(), [], 0)
			if not self.is_hotkey_module(self.__mod):
				raise Exception('Module is not a commander module...')

		except:
			sys.path = oldpath
			
			if self.__name in sys.modules:
				del sys.modules[self.name]
			raise
		
		sys.path = oldpath


	def is_hotkey_module(self, mod):
		return mod and ('__hotkey_module__' in mod.__dict__)

