import sys
import os
import re
import debug
import pp_core

from commander.commands.completion import common_prefix

def _sort_nicely(l): 
	convert = lambda text: int(text) if text.isdigit() else text
	alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]

	l.sort(key=alphanum_key)


def foldername(words, idx, view):

	prefix = os.path.dirname(words[idx])
	partial = os.path.expanduser(words[idx])

	root = pp_core.get_core(view.get_toplevel()).get_path()

	if not os.path.isabs(partial):
		partial = os.path.join(root, partial)

	
	dirname = os.path.dirname(partial)
	
	try:
		files = os.listdir(dirname)
	except OSError:
		return None


	base = os.path.basename(partial)
	ret = []
	real = []


	for f in files:
		directory = os.path.join(dirname, f)
		if f.startswith(base) and (base or not f.startswith('.')) and os.path.isdir(directory):
			real.append(directory)
			ret.append(os.path.join(prefix, f))

	_sort_nicely(real)

	if len(ret) == 1:
		return ret, ret[0], '/'
	else:
		return map(lambda x: os.path.basename(x), real), common_prefix(ret)


