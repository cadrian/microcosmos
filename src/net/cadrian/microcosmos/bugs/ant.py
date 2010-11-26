from net.cadrian.microcosmos.grid import LocatedObject


class AbstractAnt(LocatedObject):
    def canFly(self):
        return False

    def canSwim(self):
        return False
