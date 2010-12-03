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
from net.cadrian.microcosmos.model.grid import LocatedObject
from net.cadrian.microcosmos.model.bugs.ant import AbstractAnt
from net.cadrian.microcosmos.model.bugs.antStates import Dead, Exploration, FollowingScent, FoundTarget
from net.cadrian.microcosmos.model.bugs.pheromones import PheromoneKind, Pheromone

TARGET_PHEROMONE_KIND = PheromoneKind(0.125, "target")


class Target(LocatedObject):
    def __init__(self, grid, sprite):
        LocatedObject.__init__(self, grid, sprite)
        self.pheromone = Pheromone(TARGET_PHEROMONE_KIND, 16)
        self.pheromones = [self.pheromone]


class AntFemale(AbstractAnt):
    def __init__(self, grid, sprite, antPromotion, life=100, randomizer=None):
        AbstractAnt.__init__(self, grid, sprite, life=life, randomizer=randomizer)
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
            foundX, foundY, foundScent = self.findScent(TARGET_PHEROMONE_KIND)
            if foundScent == 0:
                self.state = Exploration(self)
            else:
                self.state = FollowingScent(self, foundX, foundY, TARGET_PHEROMONE_KIND)

    def move(self):
        return self.state.move()

    def isDead(self):
        return self.state.dead
