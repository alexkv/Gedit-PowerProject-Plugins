# Gedit Power Project Core Plugin
#
# Copyright (C) 2011 - Aleksei Kvitinskii
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

import gedit
import debug
from core import PowerProjectCore

CORE_INSTANCE_KEY = "PowerProjectCore"

class PowerProjectPlugin(gedit.Plugin):
	def __init__(self):
		debug.msg("PowerProjectPlugin init")


	def activate(self, window):
		debug.msg("PowerProjectPlugin activate %s" % str(window))
		window.set_data(CORE_INSTANCE_KEY, PowerProjectCore())


	def deactivate(self, window):
		debug.msg("PowerProjectPlugin deactivate")
		window.get_data(CORE_INSTANCE_KEY)


	def update_ui(self, window):
		pass


def get_core(window):
	return window.get_data(CORE_INSTANCE_KEY)


