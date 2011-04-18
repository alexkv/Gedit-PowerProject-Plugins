import gtk
import gedit
import commander.commands as commands

__commander_module__ = True
__root__ = ['hl']


def _set_highlight(lang_name, view):
	buffer = view.get_buffer()
	language_manager = gedit.get_language_manager()
	langs = language_manager.get_language_ids()
	model = gtk.ListStore(str)
	available_ids = {}

	for id in langs:
		lang = language_manager.get_language(id)
		name = lang.get_name()
		available_ids[name.upper()] = id
		model.append([name])
	
	lang_name = lang_name.upper()

	if available_ids.has_key(lang_name):
		lang_id = available_ids[lang_name]
		language = gedit.get_language_manager().get_language(lang_id)
		buffer.set_language(language)	
	
	return commands.result.HIDE

def __default__(lang_name, view):
	"""Set hightlight mode"""

	return _set_highlight(lang_name, view)

locals()['hl'] = __default__
