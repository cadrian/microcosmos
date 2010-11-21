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

    def start(self): # redefined because all the widgets are automatically created; the config only contains a template
        if self._data.hasObject("background"):
            PySGE.engine.addSprite(self.getData().getObject("background"))

	for i, level in enumerate(self._levels):
            def action(*_):
                self.onLevel(level)

	    button = copy.deepcopy(self.getData().getObject("choice"))
	    x, y = button._position
	    button._position = (x, y * (i+1))
	    button._text._resource = button._text._resource % level
            button._action = action
	    PySGE.engine.addSprite(button)

	PySGE.engine.addSprite(self.getData().getObject("mainMenu"))

    def onLevel(self, level):
        _LOGGER.info("################################ To level: %s", level)
	PySGE.application.setScreen(level)
