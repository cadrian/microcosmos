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
Various ant states describing what each ant is doing. Used by all ants
but the queen.
"""

from pysge.utils.logger import getLogger


_LOGGER = getLogger(__name__)


class Exploration:
    def __init__(self, ant):
        self.ant = ant
        self.dead = False

    def __str__(self):
        return "exploration"

    def move(self):
        x, y = self.ant.getRandomTarget()
        self.ant.moveTo(x, y)
        return self.ant


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
        return self.ant


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
        ant = self.ant
        self.grid.accept(self.x, self.y, self)
        if self.promote:
            self.grid.remove(self.x, self.y, ant)
            ant = self.antPromotion(life=ant._life)
            self.grid.put(self.x, self.y, ant)
        return ant

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


class StoreFood:
    def __init__(self, bug, store, scent, label=None):
        self._bug = bug
        self._store = store
        self._scent = scent
        self._str = "storing %s" % (label or scent.kind)

    def __str__(self):
        return self._str

    def move(self):
        self._bug._setFood(self._scent)
        self._store()
