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
from net.cadrian.microcosmos.bugs.antQueens import AntQueen
from net.cadrian.microcosmos.bugs.pheromones import PheromoneKind, Pheromone

TARGET_PHEROMONE_KIND = PheromoneKind(0.125)


class Target(LocatedObject):
    def __init__(self, grid):
        LocatedObject.__init__(self, grid)
        self.pheromone = Pheromone(TARGET_PHEROMONE_KIND, 16)
        self.pheromones = [self.pheromone]

    def allowTogether(self, other):
        return True


class Randomizer:
    def accept(self):
        return random.randint(0, 100) != 50


class Exploration:
    def __init__(self, ant):
        self._ant = ant
        self.dead = False

    def __str__(self):
        return "exploration"

    def move(self):
        square = self._ant.grid.square(self._ant.x, self._ant.y)
        x, y = random.choice(square)
        while not self._ant.grid.allowMove(x, y, self._ant) and len(square) > 0:
            square.remove((x, y))
            x, y = random.choice(square)
        if len(square) > 0:
            self._ant.moveTo(x, y)


class FollowingTarget:
    def __init__(self, ant, x, y):
        self._ant = ant
        self._x = x
        self._y = y
        self.dead = False

    def __str__(self):
        return "followingTarget"

    def move(self):
        self._ant.moveTo(self._x, self._y)


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
        self._ant = ant
        self.dead = True

    def __str__(self):
        return "dead"

    def move(self):
        self._ant.remove()


class AntFemale(AbstractAnt):
    def __init__(self, grid, antPromotion=AntQueen, life=100, randomizer=None):
        AbstractAnt.__init__(self, grid, life=life)
        self._randomizer = randomizer or Randomizer()
        self.pheromones = []
        self.state = None
        self.target = None
        self._antPromotion = antPromotion

    def goToTarget(self, target):
        self.target = target

    def canFly(self):
        return True

    def prepareToMove(self):
        self._life = self._life - 1
        if self._life <= 0:
            self.state = Dead(self)
        elif self.target is None:
            self.state = Exploration(self)
        elif self.target.x == self.x and self.target.y == self.y:
            self.state = FoundTarget(self, self.grid, self.x, self.y, self._antPromotion)
        else:
            foundX, foundY = None, None
            foundScent = 0
            for x, y in self.grid.square(self.x, self.y):
                scent = self.grid.scent(x, y, TARGET_PHEROMONE_KIND)
                if scent > foundScent and self._randomizer.accept():
                    foundX, foundY, foundScent = x, y, scent
            if foundScent == 0:
                self.state = Exploration(self)
            else:
                self.state = FollowingTarget(self, foundX, foundY)

    def move(self):
        self.state.move()

    def isDead(self):
        return self.state.dead

    def allowTogether(self, other):
        return not other.isAlive()
