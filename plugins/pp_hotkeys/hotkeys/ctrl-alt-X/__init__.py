import subprocess
from pp_core import debug, get_core
from pp_sessions import SessionOperations, SessionDialogs

__hotkey_module__ = True


def S (view):
	window = view.get_toplevel()
	SessionOperations().save_current_session(window)
	return 'session was saved'


def N (view):
	window = view.get_toplevel()
	SessionDialogs().save_session(window)
	return 'saving session'


def O (view):
	window = view.get_toplevel()
	SessionDialogs().session_manager()
	return 'managing session'


def T (view):
	window = view.get_toplevel()
	path = get_core(window).get_path()
	subprocess.Popen(['gnome-terminal', "--working-directory=%s" % path])
	return 'opening project terminal'


