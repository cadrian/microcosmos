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
from net.cadrian.microcosmos.bugs.pheromones import PheromoneKind, Pheromone

from pysge.utils.logger import getLogger


_LOGGER = getLogger(__name__)


TRAIL_HOME = PheromoneKind(0.125)
TRAIL_FOOD = PheromoneKind(0.25)
TRAIL_LICE = PheromoneKind(0.25)

SCENT_HOME = Pheromone(TRAIL_HOME, 32)
SCENT_FOOD = Pheromone(TRAIL_FOOD, 16)
SCENT_LICE = Pheromone(TRAIL_LICE, 16)


class Explore:
    def __init__(self, ant):
        self.ant = ant

    def move(self):
        self.ant.grid.remove(self.ant.x, self.ant.y, self.ant)
        self.ant.grid.put(0, 0, self.ant)


class AntWorker(AbstractAnt):
    def __init__(self, grid, life=100):
        AbstractAnt.__init__(self, grid, life=life)
        self.pheromones = set()
        self.state = None

    def prepareToMove(self):
        self._checkHill()
        self.state = Explore(self)

    def _checkHill(self):
        def add(x, y):
            x.add(y)
            return x
        bugs = reduce(add, [self.grid.bug(x, y).__class__ for x, y in self.grid.square(self.x, self.y)], set())
        if AntQueen in bugs:
            self._setLeavingHome()

    def _setLeavingHome(self):
        self.pheromones.add(SCENT_HOME)

    def move(self):
        self.state.move()

    def isDead(self):
        return self.state.dead
