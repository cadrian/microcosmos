from pysge.facade import PySGE
from pysge.objects.base import BasicSprite
from pysge.utils.data import DataContainer
from pysge.utils.logger import getLogger

_LOGGER = getLogger(__name__)


class LandscapeFeatureFactory:
    def __init__(self, config):
	self._theme = config.theme
	self._tilesRect = config.tilesRect

    def expand(self):
	(x, y), (w, h) = self._tilesRect
	for mapX in range(x, x+w):
	    for mapY in range(y, y+h):
		yield LandscapeFeature(DataContainer(theme=self._theme, mapX=mapX, mapY=mapY, standAlone=False))


class LandscapeFeature(BasicSprite):
    def __init__(self, config):
	BasicSprite.__init__(self, config)
	self._theme = config.theme
	self.mapX = config.mapX
	self.mapY = config.mapY

    def drawImage(self, x, y, tile):
	image = PySGE.engine.drawTexture(self._resource, ((x, y), (tile, tile)))
	rect = image.get_rect().move((x, y))
	return (image, rect)

    def __repr__(self):
	return "%s(layer=%s, map=%sx%s)" % (self._theme, self._layer, self.mapX, self.mapY)


class Grass(LandscapeFeatureFactory):
    def __init__(self, config):
	config.theme = "grass"
	LandscapeFeatureFactory.__init__(self, config)


class Sand(LandscapeFeatureFactory):
    def __init__(self, config):
	config.theme = "sand"
	LandscapeFeatureFactory.__init__(self, config)


class Soil(LandscapeFeatureFactory):
    def __init__(self, config):
	config.theme = "soil"
	LandscapeFeatureFactory.__init__(self, config)


class Wall(LandscapeFeatureFactory):
    def __init__(self, config):
	config.theme = "wall"
	LandscapeFeatureFactory.__init__(self, config)


class Water(LandscapeFeatureFactory):
    def __init__(self, config):
	config.theme = "water"
	LandscapeFeatureFactory.__init__(self, config)
