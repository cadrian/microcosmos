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
