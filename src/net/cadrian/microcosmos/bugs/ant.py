from net.cadrian.microcosmos.grid import LocatedObject


class AbstractAnt(LocatedObject):
    def __init__(self, grid, life):
        LocatedObject.__init__(self, grid)
        self._life = life

    def isAlive(self):
        return True

    def canFly(self):
        return False

    def canSwim(self):
        return False
