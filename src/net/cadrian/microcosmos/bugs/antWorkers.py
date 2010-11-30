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
from net.cadrian.microcosmos.bugs.ant import AbstractAnt
from net.cadrian.microcosmos.bugs.antQueens import AntQueen
from net.cadrian.microcosmos.bugs.antStates import Dead, Exploration, FollowingScent
from net.cadrian.microcosmos.bugs.pheromones import PheromoneKind, Pheromone

from pysge.utils.logger import getLogger


_LOGGER = getLogger(__name__)


TRAIL_HILL = PheromoneKind(0.125, "hill")
TRAIL_FOOD = PheromoneKind(0.25, "food")
TRAIL_LICE = PheromoneKind(0.25, "lice")

SCENT_HILL = Pheromone(TRAIL_HILL, 32)
SCENT_FOOD = Pheromone(TRAIL_FOOD, 16)
SCENT_LICE = Pheromone(TRAIL_LICE, 16)


class AntWorker(AbstractAnt):
    def __init__(self, grid, life=100, randomizer=None):
        AbstractAnt.__init__(self, grid, life=life, randomizer=randomizer)
        self.pheromones = set()
        self.state = None

    def prepareToMove(self):
        self._life = self._life - 1
        if self._life <= 0:
            self.state = Dead(self)
        else:
            self._checkHill()
            foodX, foodY, foodScent = self.findScent(TRAIL_FOOD)
            liceX, liceY, liceScent = self.findScent(TRAIL_LICE)
            if foodScent > liceScent:
                self.state = FollowingScent(self, foodX, foodY, TRAIL_FOOD)
            elif liceScent > 0:
                self.state = FollowingScent(self, liceX, liceY, TRAIL_LICE)
            else:
                self.state = Exploration(self)

    def _checkHill(self):
        def add(x, y):
            x.add(y)
            return x
        bugs = reduce(add, [self.grid.bug(x, y).__class__ for x, y in self.grid.square(self.x, self.y)], set())
        if AntQueen in bugs:
            self._setLeavingHill()

    def _setLeavingHill(self):
        self.pheromones.add(SCENT_HILL)

    def move(self):
        self.state.move()

    def isDead(self):
        return self.state.dead
