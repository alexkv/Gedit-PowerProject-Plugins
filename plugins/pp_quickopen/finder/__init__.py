import os
import subprocess
from pp_core.singleton import Singleton


class Finder:
	__metaclass__ = Singleton
	__controller_file = os.path.dirname(os.path.abspath(__file__)) + '/controller.rb'
	__process = None

	def close(self):
		self.__connect()
		self.write('exit\n')


	def __connect(self):
		if self.__process != None and self.__process.returncode == None:
			return

		self.__process = subprocess.Popen(['ruby', self.__controller_file], shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE)


	def search(self, path, text):
		self.__connect()

		self.write('search\n')
		self.write('%s\n' % path)
		self.write('%s\n' % text)

		result = []
		while 1:
			output = self.__process.stdout.readline().rstrip()
			if output == '%%last%%': break
			result.append(output)

		return result


	def flush(self, path):
		self.__connect()
		self.write('flush\n')


	def write(self, text):
		self.__process.stdin.write(text)












