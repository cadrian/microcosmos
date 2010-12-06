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
"""
Drawable bugs.
"""

from pysge.facade import PySGE
from pysge.objects.base import BasicSprite
from pysge.utils.data import DataContainer
from pysge.utils.logger import getLogger

from net.cadrian.microcosmos.bugs import AntQueen as AntQueenModel, AntFemale as AntFemaleModel, AntSoldier as AntSoldierModel, AntWorker as AntWorkerModel

_LOGGER = getLogger(__name__)


class AntFactory:
    def __init__(self, config):
        self.mapX, self.mapY = config.position

    def get(self, model, sprite):
        return Ant(
            DataContainer(
                theme="%s_ant_%s" % (self.ANT_COLOR, self.ANT_CASTE),
                mapX=self.mapX,
                mapY=self.mapY,
                position=(0,0),
                standAlone=False,
                model=model,
                modelFactory=self.antModel,
            )
        )


class Bug(BasicSprite):
    def __init__(self, config):
        self._theme = config.theme
        self.mapX = config.mapX
        self.mapY = config.mapY
        self._model = config.modelFactory(config.model, self)
        BasicSprite.__init__(self, config)
        try:
            config.model.put(self.mapX, self.mapY, self._model)
        except:
            _LOGGER.exception("################ %s: cannot put at %sx%s (model: %s)", self, self.mapX, self.mapY, self._model)

    def drawImage(self, x, y, tile):
        image = PySGE.engine.drawTexture(self._resource, ((x, y), (tile, tile)))
        rect = image.get_rect().move((x, y))
        return (image, rect)


class Louse(Bug):
    def __init__(self, config):
        config.layer = 2
        Bug.__init__(self, config)


class Ant(Bug):
    def __init__(self, config):
        config.layer = 3
        Bug.__init__(self, config)


class RedAnt(AntFactory):
    ANT_COLOR = "red"


class RedAntFemale(RedAnt):
    ANT_CASTE = "female"

    def antModel(self, gridModel, sprite):
        return AntFemaleModel(gridModel, sprite=sprite)


class RedAntQueen(RedAnt):
    ANT_CASTE = "queen"

    def antModel(self, gridModel, sprite):
        return AntQueenModel(gridModel, sprite=sprite)


class RedAntSoldier(RedAnt):
    ANT_CASTE = "soldier"

    def antModel(self, gridModel, sprite):
        return AntSoldierModel(gridModel, sprite=sprite)


class RedAntWorker(RedAnt):
    ANT_CASTE = "worker"

    def antModel(self, gridModel, sprite):
        return AntWorkerModel(gridModel, sprite=sprite)
