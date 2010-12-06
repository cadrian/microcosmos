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
The graphical grid. Waiting for Benjamin to generalize it in PySGE. :-)
"""

import math

from pysge.facade import PySGE
from pysge.objects.base import BasicSprite
from pysge.objects.constants import TRANSPARENCY
from pysge.objects.scroll import Scroller
from pysge.utils.data import DataContainer
from pysge.utils.logger import getLogger

from net.cadrian.microcosmos.grid import Grid as GridModel


_LOGGER = getLogger(__name__)


class GridBehaviour:
    def __init__(self, host):
        self._host = host

    def __call__(self, x, y, obj):
        """ a model object asked to move. """
        _LOGGER.debug("%s asked to move to (%sx%s): its sprite is %s", obj, x, y, obj.sprite)

    def setBindings(self):
        pass

    def removeBindings(self):
        pass

    def update(self):
        pass


class Grid(BasicSprite):
    def __init__(self, config):
        config.behaviour = GridBehaviour(self)
        BasicSprite.__init__(self, config)
        self._tile = config.tile
        self._size = config.size
        self._visibleArea = PySGE.engine.getRect((0, 0), self._size)
        self._sprites = list(config.sprites or [])
        self._makeScrollers(config.scrollSize or int(self._tile / 2), config.scrollSpeed or 1)

        self._mapSize = config.mapSize
        x, y = self._mapSize
        self._model = GridModel(x, y, mover=self.behaviour)
        self._resource = PySGE.engine.getSurface((x * self._tile, y * self._tile), TRANSPARENCY)
        self.rect = self._resource.get_rect()

        self._scrollPosition = (0, 0)

        self._landscape = reduce(lambda x, y: x + y, [[tile for tile in feature.expand(self._model)] for feature in config.landscape], [])
        _LOGGER.debug("LANDSCAPE=%s", self._landscape)

        self._bugs = [bug.get(self._model) for bug in config.bugs]
        _LOGGER.debug("BUGS=%s", self._bugs)

    def _makeScrollers(self, scrollSize, scrollSpeed):
        x, y = self._position
        w, h = self._size
        self._scrollers = [
            Scroller(DataContainer(host=self, position=(x, y), size=(w, scrollSize), scrolling=(0, -scrollSpeed))), # Up
            Scroller(DataContainer(host=self, position=(x+w-scrollSize, y), size=(scrollSize, h), scrolling=(scrollSpeed, 0))), # Right
            Scroller(DataContainer(host=self, position=(x, y+h-scrollSize), size=(w, scrollSize), scrolling=(0, scrollSpeed))), # Down
            Scroller(DataContainer(host=self, position=(x, y), size=(scrollSize, h), scrolling=(-scrollSpeed, 0))), # Left
        ]

    def _fixTilePosition(self, tileX, tileY):
        x, y = self._scrollPosition
        mapWidth, mapHeight = self._mapSize
        return (
            (tileX - x + mapWidth) % mapWidth,
            (tileY - y + mapHeight) % mapHeight,
        )

    def _realTilePosition(self, tileX, tileY):
        x, y = self._fixTilePosition(tileX, tileY)
        return (x * self._tile, y * self._tile)

    def _isVisible(self, x, y):
        w, h = self._size
        return 0 <= x <= w and 0 <= y <= h

    def update(self):
        map(lambda x: x.update(), self._scrollers + self._sprites)

        def updateGridElement(feature):
            x, y = self._realTilePosition(feature.mapX, feature.mapY)
            if self._isVisible(x, y):
                image, rect = feature.drawImage(x, y, self._tile)
                PySGE.engine.draw(self._resource, image, rect)
        map(updateGridElement, self._landscape)
        map(updateGridElement, self._bugs)

        for sprite in self._sprites:
            PySGE.engine.draw(self._resource, sprite.image, sprite.rect)

        self.image = self._resource.subsurface(self._visibleArea)
        self.rect = self.image.get_rect().move(self._position)

    def getMousePosition(self):
        realPosition = BasicSprite.getMousePosition(self)
        return (
            realPosition[0] - self._position[0],
            realPosition[1] - self._position[1],
        )

    def setBindings(self):
        map(lambda x: x.setBindings(), self._sprites)

    def removeBindings(self):
        map(lambda x: x.removeBindings(), self._sprites)

    def scroll(self, dx, dy):
        x, y = self._scrollPosition
        _LOGGER.critical("#### SCROLL: %sx%s + %sx%s", x, y, dx, dy)
        self._scrollPosition = (x + dx, y + dy)
