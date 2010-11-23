import math

from pysge.facade import PySGE
from pysge.objects.base import BasicSprite, Scroller
from pysge.objects.constants import TRANSPARENCY
from pysge.utils.data import DataContainer
from pysge.utils.logger import getLogger

_LOGGER = getLogger(__name__)


class Grid(BasicSprite):
    def __init__(self, config):
        BasicSprite.__init__(self, config)
        self._tile = config.tile
        self._size = config.size
        self._visibleArea = PySGE.engine.getRect((0, 0), self._size)
        self._sprites = list(config.sprites or [])
        self._makeScrollers(config.scrollSize or int(self._tile / 2), config.scrollSpeed or 1)

        self._mapSize = config.mapSize
        x, y = self._mapSize
        self._resource = PySGE.engine.getSurface((x * self._tile, y * self._tile), TRANSPARENCY)
        self.rect = self._resource.get_rect()

        width, height = self._size
        self._visibleSize = (math.ceil(width / self._tile), math.ceil(height / self._tile))
        self._scrollPosition = (0, 0)

        self._landscape = reduce(lambda x, y: x + y, [[tile for tile in feature.expand()] for feature in config.landscape], [])
        _LOGGER.debug("LANDSCAPE=%s", self._landscape)

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

    def _isVisible(self, tileX, tileY):
        x, y = self._fixTilePosition(tileX, tileY)
        w, h = self._visibleSize
        return 0 <= x <= w and 0 <= y <= h

    def update(self):
        map(lambda x: x.update(), self._scrollers + self._sprites)

        def updateLandscapeFeature(feature):
            if self._isVisible(feature.mapX, feature.mapY):
                x, y = self._realTilePosition(feature.mapX, feature.mapY)
                image, rect = feature.drawImage(x, y, self._tile)
                PySGE.engine.draw(self._resource, image, rect)
        map(updateLandscapeFeature, [feature for feature in self._landscape])

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
