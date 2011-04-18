import os
import gio
import gedit
import glob
import sys
import types
import inspect
import gio

import commander.commands as commands
import commander.commands.completion
import commander.commands.result
import commander.commands.exceptions

__commander_module__ = True
__root__ = ['rn', 'move', 'mv']

@commands.autocomplete(newfile=commander.commands.completion.filename)
def __default__(view, newfile):
	"""Rename current file: rename &lt;newname&gt;"""
	
	doc = view.get_buffer()
	
	if not hasattr(doc, 'set_uri'):
		raise commander.commands.exceptions.Execute('Your version of gedit does not support this action')
	
	if doc.is_untitled():
		raise commander.commands.exceptions.Execute('Document is unsaved and thus cannot be renamed')
	
	if doc.get_modified():
		raise commander.commands.exceptions.Execute('You have unsaved changes in your document')
	
	if not doc.is_local():
		raise commander.commands.exceptions.Execute('You can only rename local files')
	
	f = gio.File(doc.get_uri())
	
	if not f.query_exists():
		raise commander.commands.exceptions.Execute('Current document file does not exist')
	
	if os.path.isabs(newfile):
		dest = gio.File(newfile)
	else:
		dest = f.get_parent().resolve_relative_path(newfile)
	
	if f.equal(dest):
		yield commander.commands.result.HIDE
	
	if not dest.get_parent().query_exists():
		# Check to create parent directory
		fstr, words, modifierret = (yield commands.result.Prompt('Directory does not exist, create? [Y/n] '))
		
		if fstr.strip().lower() in ['y', 'ye', 'yes', '']:
			# Create parent directories
			try:
				os.makedirs(dest.get_parent().get_path())
			except OSError, e:
				raise commander.commands.exceptions.Execute('Could not create directory')
		else:
			yield commander.commands.result.HIDE
	
	if dest.query_exists():
		fstr, words, modifierret = (yield commands.result.Prompt('Destination already exists, overwrite? [Y/n]'))
		
		if not fstr.strip().lower() in ['y', 'ye', 'yes', '']:
			yield commander.commands.result.HIDE
	
	try:
		f.move(dest, _dummy_cb, flags=gio.FILE_COPY_OVERWRITE)
		
		doc.set_uri(dest.get_uri())
		yield commander.commands.result.HIDE
	except Exception, e:
		raise commander.commands.exceptions.Execute('Could not move file: %s' % (e,))


def _dummy_cb(num, total):
	pass


locals()['rn'] = __default__
locals()['mv'] = __default__
locals()['move'] = __default__