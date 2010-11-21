
import os
from pysge.dataModel.data import DataFile
from pysge.controllers.base import AbstractController
from pysge.utils.logger import getLogger
from pysge.facade import PySGE

_LOGGER = getLogger(__name__)


class GameData(DataFile):
    def loadImpl(self):
        #self.startPosition = self.getObject('hero').getPosition()
        self.addObject("clock", self._symbols["clock"](position=(350, 230)))

    def addWall(self, wall):
        wall = self._symbols["wall"](wall[0], wall[1])
        self.getObject("walls").add(wall)
        return wall


class LevelController(AbstractController):
    def __init__(self, filePath):
        AbstractController.__init__(self, GameData(filePath))

    def startImpl(self):
        #self.getData().getObject("goal").setCollisionCallback(self.victory)
        #self.getData().getObject("walls").setCollisionCallback(self.death)
        PySGE.eventManager.connect("collision", self.handleCollision)
        PySGE.eventManager.connect("firstMove", lambda x:self.getData().getObject("clock").start())
        #PySGE.engine.addSprite(*self.getData().getObject("walls").sprites())
        PySGE.engine.addSprite(
            #self.getData().getObject("hero"),
            self.getData().getObject("clock"),
            #self.getData().getObject("goal"),
        )
        self.reset()

    def endImpl(self):
        _LOGGER.info("Ending level %s", self.getData())
        PySGE.eventManager.disconnect("collision", self.handleCollision)

    def reset(self):
        #self.getData().getObject("hero").setPosition(self.getData().startPosition)
        self.getData().getObject("clock").reset()
        PySGE.engine.updateAll()

    def death(self):
        _LOGGER.critical("DEAD!")
        PySGE.application.setScreen('defeat')

    def victory(self):
        _LOGGER.critical("WON! %s", self.getData().getObject("clock").getElapsedTime())
        PySGE.scores.setScore(self.getData().name, self.getData().getObject("clock").getElapsedTime())
        PySGE.application.setScreen('victory')

    def handleCollision(self, event):
        def getHandlerName(objectName):
            return "collideWith%s" % objectName.__class__.__name__

        if hasattr(event.secondObject, getHandlerName(event.firstObject)):
            getattr(event.secondObject, getHandlerName(event.firstObject))()


