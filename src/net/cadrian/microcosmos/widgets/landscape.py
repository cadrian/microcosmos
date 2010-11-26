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
from pysge.facade import PySGE
from pysge.objects.base import BasicSprite
from pysge.utils.data import DataContainer
from pysge.utils.logger import getLogger

from net.cadrian.microcosmos.grid import Grid as GridModel
from net.cadrian.microcosmos.landscape import Grass as GrassModel, Sand as SandModel, Soil as SoilModel, Wall as WallModel, Water as WaterModel

_LOGGER = getLogger(__name__)


class LandscapeFeatureFactory:
    def __init__(self, config):
        self._theme = config.theme
        self._tilesRect = config.tilesRect

    def expand(self, model):
        (x, y), (w, h) = self._tilesRect
        for mapX in range(x, x+w):
            for mapY in range(y, y+h):
                yield LandscapeFeature(
                    DataContainer(
                        theme=self._theme,
                        mapX=mapX,
                        mapY=mapY,
                        position=(0,0),
                        standAlone=False,
                        model=model,
                        modelFactory=self.featureModel,
                    )
                )


class LandscapeFeature(BasicSprite):
    def __init__(self, config):
        self._theme = config.theme
        self.mapX = config.mapX
        self.mapY = config.mapY
        self._model = config.modelFactory(config.model)
        BasicSprite.__init__(self, config)
        try:
            config.model.put(self.mapX, self.mapY, self._model)
        except:
            _LOGGER.exception("################ %s: OVERLAP at %sx%s (model: %s)", self, self.mapX, self.mapY, self._model)

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

    def featureModel(self, gridModel):
        return GrassModel(gridModel)


class Sand(LandscapeFeatureFactory):
    def __init__(self, config):
        config.theme = "sand"
        LandscapeFeatureFactory.__init__(self, config)

    def featureModel(self, gridModel):
        return SandModel(gridModel)


class Soil(LandscapeFeatureFactory):
    def __init__(self, config):
        config.theme = "soil"
        LandscapeFeatureFactory.__init__(self, config)

    def featureModel(self, gridModel):
        return SoilModel(gridModel)


class Wall(LandscapeFeatureFactory):
    def __init__(self, config):
        config.theme = "wall"
        LandscapeFeatureFactory.__init__(self, config)

    def featureModel(self, gridModel):
        return WallModel(gridModel)


class Water(LandscapeFeatureFactory):
    def __init__(self, config):
        config.theme = "water"
        LandscapeFeatureFactory.__init__(self, config)

    def featureModel(self, gridModel):
        return WaterModel(gridModel)
