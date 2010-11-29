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
import os
from pysge.dataModel.data import DataFile
from pysge.controllers.base import AbstractController
from pysge.utils.logger import getLogger
from pysge.facade import PySGE

_LOGGER = getLogger(__name__)


class LevelController(AbstractController):
    def __init__(self, filePath):
        AbstractController.__init__(self, DataFile(filePath))

    def endImpl(self):
        _LOGGER.info("Ending level %s", self.getData())
        PySGE.eventManager.disconnect("collision", self.handleCollision)

    def death(self):
        _LOGGER.critical("DEAD!")
        PySGE.application.setScreen('defeat')

    def victory(self):
        PySGE.application.setScreen('victory')

    def handleCollision(self, event):
        def getHandlerName(objectName):
            return "collideWith%s" % objectName.__class__.__name__

        if hasattr(event.secondObject, getHandlerName(event.firstObject)):
            getattr(event.secondObject, getHandlerName(event.firstObject))()
