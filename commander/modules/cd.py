import os

import commander.commands as commands
import commander.commands.completion
import commander.commands.result
from pp_core import debug, get_core, completion
#import pp-core.completion

__commander_module__ = True
__root__ = ['pwd']

@commands.autocomplete(folder=completion.foldername)

def __default__(folder, window):
	"""Set working directory"""

	get_core(window).set_path(folder)
	return commands.result.HIDE


def pwd(entry, window):
	"""Get working directory"""

	row = get_core(window).get_path()
	entry.info_show(row, True)
	return commands.result.HIDE


locals()['pwd'] = pwd
