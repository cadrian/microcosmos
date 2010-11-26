#  Microcosmos: an antsy game
#  Copyright (C) 2010 Cyril ADRIAN <cyril.adrian@gmail.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, version 3 exclusively.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from pysge.objects.widgets import NiceButton
from pysge.utils.data import DataContainer


class TemplateButton:
    def __init__(self, config):
	self._config = config
	self.standAlone = False

    def getButton(self, customize=None):
	config = dict(self._config._symbols)
	if customize is not None:
	    customize(config)
	return NiceButton(DataContainer(**config))
