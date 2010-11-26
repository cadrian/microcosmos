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
import copy
import os

from pysge.controllers.base import AbstractMenu
from pysge.dataModel.menu import MenuData
from pysge.controllers.scores import Scores
from pysge.facade import PySGE
from pysge.utils.logger import getLogger
from pysge.objects.widgets import NiceButton

_LOGGER = getLogger(__name__)


class MainMenuController(AbstractMenu):
    def __init__(self, filename):
	AbstractMenu.__init__(
	    self,
	    filename,
	    actions={
		"start": self.onStart,
	    })

    def startImpl(self):
	AbstractMenu.startImpl(self)

    def onStart(self, _):
	PySGE.application.setScreen('choose')


class ChoiceMenuController(AbstractMenu):
    def __init__(self, filename, levels):
	self._levels = levels
	AbstractMenu.__init__(self, filename)

    def startImpl(self):
	buttonTemplate = self.getData().getObject("choice")
	for i, level in enumerate(self._levels):
	    def customize(config):
		def action(_):
		    self.onLevel(level)
		config["text"] = config["text"] % level
		config["action"] = action
		x, y = config["position"]
		dx, dy = config["increment"]
		config["position"] = (x + dx * i, y + dy * i)

	    PySGE.engine.addSprite(buttonTemplate.getButton(customize=customize))

    def onLevel(self, level):
	_LOGGER.info("Going to level: %s", level)
	PySGE.application.setScreen(level)
