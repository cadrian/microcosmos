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
"""
"Abstract ants" provide a common behaviour for all kinds of ants. (not
a lot, actually)
"""

import random

from net.cadrian.microcosmos.model.grid import LocatedObject


class Randomizer:
    def accept(self):
        return random.randint(0, 100) != 50


class AbstractAnt(LocatedObject):
    def __init__(self, grid, sprite, life, randomizer=None):
        LocatedObject.__init__(self, grid, sprite)
        self._randomizer = randomizer or Randomizer()
        self._life = life

    def isAlive(self):
        return True

    def canFly(self):
        return False

    def canSwim(self):
        return False

    def findScent(self, pheromoneKind):
        foundX, foundY = None, None
        foundScent = 0
        for x, y in self.grid.square(self.x, self.y):
            scent = self.grid.scent(x, y, pheromoneKind)
            if scent > foundScent and self._randomizer.accept():
                foundX, foundY, foundScent = x, y, scent
        return foundX, foundY, foundScent
