import logging
import os

from pysge.controllers.scores import Scores
from pysge.core.application import Application
from pysge.dataModel.scores import ScoresData
from pysge.facade import PySGE
from pysge.utils.logger import getLogger, setupTestLogging

from net.cadrian.microcosmos.controller import LevelController
from net.cadrian.microcosmos.menus import ChoiceMenuController, MainMenuController

_LOGGER = getLogger(__name__)

class Game(Application):
    def __init__(self):
        #setupTestLogging(logging.DEBUG)
        setupTestLogging(logging.INFO)

	configPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/game.ini")
        Application.__init__(self, configPath)

    def setUp(self):
        self._levels = []
        PySGE.objectFactory.registerModules("objects")
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