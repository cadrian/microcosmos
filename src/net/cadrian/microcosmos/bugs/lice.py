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
from net.cadrian.microcosmos.grid import LocatedObject

from pysge.utils.logger import getLogger


_LOGGER = getLogger(__name__)


class LandscapeVisitor:
    def __init__(self):
        self.canLive = False
        self.canMilk = False

    def visitSoil(self, soil):
        self.canLive = True

    def visitGrass(self, grass):
        self.canLive = True
        self.canMilk = True


class Louse(LocatedObject):
    def __init__(self, grid, life):
        LocatedObject.__init__(self, grid)
        self._life = life
        self._milk = 0

    def isAlive(self):
        return True

    def canFly(self):
        return False

    def canSwim(self):
        return False

    def allowTogether(self, other):
        return not other.isAlive()

    def prepareToMove(self):
        self._life = self._life - 1
        if self._life > 0:
            self._landscapeVisitor = LandscapeVisitor()
            self.grid.accept(self.x, self.y, self._landscapeVisitor)

    def move(self):
        if self._landscapeVisitor.canLive:
            x, y = self.findEmptyCell()
            if x or y:
                life = self._life / 2
                if life:
                    self.grid.put(x, y, Louse(self.grid, life))
                    self._life = self._life - life
            if self._landscapeVisitor.canMilk:
                self._milk = self._milk + 1
