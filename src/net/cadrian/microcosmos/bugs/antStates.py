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

from pysge.utils.logger import getLogger


_LOGGER = getLogger(__name__)


class Exploration:
    def __init__(self, ant):
        self.ant = ant
        self.dead = False

    def __str__(self):
        return "exploration"

    def move(self):
        square = self.ant.grid.square(self.ant.x, self.ant.y)
        x, y = random.choice(square)
        while not self.ant.grid.allowMove(x, y, self.ant) and len(square) > 0:
            square.remove((x, y))
            x, y = random.choice(square)
        if len(square) > 0:
            self.ant.moveTo(x, y)


class FollowingScent:
    def __init__(self, ant, x, y, pheromoneKind):
        self.ant = ant
        self._x = x
        self._y = y
        self.dead = False
        self._str = "following %s" % pheromoneKind

    def __str__(self):
        return self._str

    def move(self):
        self.ant.moveTo(self._x, self._y)


class FoundTarget:
    def __init__(self, ant, grid, x, y, antPromotion):
        self.ant = ant
        self.grid = grid
        self.x = x
        self.y = y
        self.dead = False
        self.promote = False
        self.antPromotion = antPromotion

    def __str__(self):
        return "foundTarget"

    def move(self):
        self.grid.accept(self.x, self.y, self)
        if self.promote:
            self.grid.remove(self.x, self.y, self.ant)
            self.grid.put(self.x, self.y, self.antPromotion(self.grid, life=self.ant._life))

    def visitSoil(self, soil):
        self.promote = True

    def visitGrass(self, grass):
        self.promote = True


class Dead:
    def __init__(self, ant):
        self.ant = ant
        self.dead = True

    def __str__(self):
        return "dead"

    def move(self):
        self.ant.remove()
