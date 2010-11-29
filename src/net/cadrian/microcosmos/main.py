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
import logging
import os
import pygame

from pysge.controllers.scores import Scores
from pysge.core.application import Application
from pysge.core.engine import SpriteEngine
from pysge.dataModel.scores import ScoresData
from pysge.facade import PySGE
from pysge.utils.logger import consoleHandler, fileHandler, getLogger, setupTestLogging

from net.cadrian.microcosmos.controller import LevelController
from net.cadrian.microcosmos.menus import ChoiceMenuController, MainMenuController


formatter = logging.Formatter("%(asctime)s | %(thread)d | %(name)-40s | %(levelname)-8s | %(message)s")
consoleHandler.setFormatter(formatter)
fileHandler.setFormatter(formatter)


_LOGGER = getLogger(__name__)


class MySpriteEngine(SpriteEngine):
    def loadImage(self, resource):
        def convertImage(filename):
            surface = pygame.image.load(filename).convert_alpha()
            #surface.set_colorkey(TRANSPARENCY, pygame.RLEACCEL)
            return surface

        return self._loadResource(resource, convertImage).copy()


class Game(Application):
    def __init__(self):
        #setupTestLogging(logging.DEBUG)
        setupTestLogging(logging.INFO)
        configPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/game.ini")
        Application.__init__(self, configPath)
        PySGE.engine = MySpriteEngine(
            PySGE.configuration.getScreenSize(),
            PySGE.configuration.getName(),
            PySGE.configuration.getResourcePath(),
            PySGE.eventManager
        )

    def setUp(self):
        self._levels = []
        PySGE.objectFactory.registerModules("net.cadrian.microcosmos.widgets")
        PySGE.setScoreHandler(ScoresData, PySGE.configuration.getScoresPath())
        self._makeLevels()
        self._makeMenus()

    def _makeLevels(self):
        levelNames = [levelPath for levelPath in os.listdir(PySGE.configuration.getLevelPath()) if levelPath.endswith(".data")]
        for level in levelNames:
            levelName, ext = level.split('.')
            levelController = LevelController(os.path.join(PySGE.configuration.getLevelPath(), level))
            self._screens[levelName] = levelController
            self._levels.append(levelName)
        self._levels.sort()
        _LOGGER.info("Known levels are: %s", self._levels)

    def _makeMenus(self):
        def makeMenu(factory, name, *args):
            return factory(os.path.join(PySGE.configuration.getBasePath(), name), *args)

        self._screens['firstScreen'] =  makeMenu(MainMenuController, "screens/mainMenu.data")
        self._screens['choose'] = makeMenu(ChoiceMenuController, "screens/choiceMenu.data", self._levels)
        #self._screens['victory'] = makeMenu(MenuController, "screens/victoryMenu.data")
        #self._screens['defeat'] = makeMenu(MenuController, "screens/defeatMenu.data")
        #self._screens['scores'] = makeMenu(Scores, "screens/scores.data")
