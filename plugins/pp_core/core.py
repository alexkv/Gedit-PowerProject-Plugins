import os
import debug

class PowerProjectCore (object):

	def __init__(self):
		self.__path = os.path.expanduser('~')


	def set_path(self, p):
		self.__path = self.__prepare(p)


	def get_path(self):
		return self.__path


	def __prepare(self, path):
		path = os.path.expanduser(path)

		if os.path.isabs(path):
			return path

		path = os.path.join(self.__path, path)
		path = os.path.normpath(path)
		return path

