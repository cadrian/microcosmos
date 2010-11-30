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
import random

from net.cadrian.microcosmos.grid import LocatedObject
from net.cadrian.microcosmos.bugs.ant import AbstractAnt
from net.cadrian.microcosmos.bugs.pheromones import PheromoneKind, Pheromone


def randomNextPosition(square):
    return random.choice(square)


class LandscapeVisitor:
    def __init__(self):
        self.sustainsQueen = False

    def visitSoil(self, soil):
        self.sustainsQueen = True

    def visitGrass(self, grass):
        self.sustainsQueen = True


class AntQueen(AbstractAnt):
    def __init__(self, grid, life=100, nextPosition=None, nextAnt=None):
        AbstractAnt.__init__(self, grid, life=life)
        self.pheromones = []
        self._next = None
        self._nextPositionFactory = nextPosition or randomNextPosition
        self._nextAntFactory = nextAnt

    def isDead(self):
        return self._life == 0

    def prepareToMove(self):
        self._life = self._life - 1
        if self._life > 0:
            landscapeVisitor = LandscapeVisitor()
            self.grid.accept(self.x, self.y, landscapeVisitor)
            if landscapeVisitor.sustainsQueen:
                self._next, self._cost = self._nextAntFactory()

    def move(self):
        newborn = self._createNext()
        if newborn:
            square = self.grid.square(self.x, self.y)
            x, y = self._nextPositionFactory(square)
            self.grid.put(x, y, newborn)
        self._next = None

    def _createNext(self):
        if self._next and self._cost < self._life:
            result = self._next(self.grid)
            self._life = self._life - self._cost
            return result
