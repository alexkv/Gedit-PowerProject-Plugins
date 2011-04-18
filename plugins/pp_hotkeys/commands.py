import os
import types
import bisect
import module
from pp_core import debug
from pp_core.singleton import Singleton

def is_module(mod):
	mod = str(mod)
	return mod.endswith('.py') or (os.path.isdir(mod) and os.path.isfile(os.path.join(mod, '__init__.py')))


class Commands ():
	__metaclass__ = Singleton

	def __init__(self):
		self._modules = None



	def set_dirs(self, dirs):
		self._dirs = dirs



	def execute(self, command, subcommand, view):
		if self.command_exists(command):
			debug.msg('Commands execute %s %s' % (command, subcommand))
			return self._modules[command].execute(subcommand, view)



	def ensure(self):
		# Ensure that modules have been scanned
		if self._modules != None:
			return

		self._modules = {}

		for d in self._dirs:
			self.scan(d)


	def command_exists(self, command):
		self.ensure()
		return command in self._modules



	def scan(self, d):
		files = []
		
		try:
			files = os.listdir(d)
		except OSError:
			pass
		
		for f in files:
			full = os.path.join(d, f)

			if is_module(full):
				self.add_module(full)



	def add_module(self, filename):
		base = self.module_name(filename)
		
		# Check if module already exists
		if base in self._modules:
			return
		
		# Create new 'empty' module
		self._modules[base] = module.Module(base, os.path.dirname(filename))
		
		return True


	def module_name(self, filename):
		# Module name is the basename without the .py
		return os.path.basename(os.path.splitext(filename)[0])
