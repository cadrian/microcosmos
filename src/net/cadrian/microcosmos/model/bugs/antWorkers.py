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
Ant workers: feed the queen for her to breed new ants. They gather
food and milk plant lice.
"""

from net.cadrian.microcosmos.model.grid import LocatedObject
from net.cadrian.microcosmos.model.bugs.ant import AbstractAnt
from net.cadrian.microcosmos.model.bugs.antQueens import AntQueen, QUEEN_PHEROMONE_KIND
from net.cadrian.microcosmos.model.bugs.antStates import Dead, Exploration, FollowingScent, StoreFood
from net.cadrian.microcosmos.model.bugs.pheromones import PheromoneKind, Pheromone

from pysge.utils.logger import getLogger


_LOGGER = getLogger(__name__)


TRAIL_HILL = PheromoneKind(0.125, "hill")
TRAIL_FOOD = PheromoneKind(0.25, "food")
TRAIL_LICE = PheromoneKind(0.25, "lice")

SCENT_HILL = Pheromone(TRAIL_HILL, 32)
SCENT_FOOD = Pheromone(TRAIL_FOOD, 16)
SCENT_LICE = Pheromone(TRAIL_LICE, 16)


class AntWorker(AbstractAnt):
    def __init__(self, grid, sprite, life=100, randomizer=None):
        AbstractAnt.__init__(self, grid, sprite, life=life, randomizer=randomizer)
        self.pheromones = set()
        self.state = None
        self._food = None

    def prepareToMove(self):
        self._life = self._life - 1
        self.state = self._checkDead() or self._checkFood() or self._checkFoundFood() or self._checkHill() or Exploration(self)

    def _checkDead(self):
        if self._life <= 0:
            return Dead(self)

    def _checkFood(self):
        if self._food is not None:
            trailX, trailY, trailScent = self.findScent(TRAIL_HILL)
            queenX, queenY, queenScent = self.findScent(QUEEN_PHEROMONE_KIND)
            if trailScent > queenScent:
                return FollowingScent(self, trailX, trailY, TRAIL_HILL)
            else:
                return FollowingScent(self, queenX, queenY, QUEEN_PHEROMONE_KIND)

    def _checkFoundFood(self):
        host = self

        class FoodLookup:
            def __init__(self):
                self.state = None

            def visitFood(self, food):
                if food.store > 0 and self.state is None:
                    def takeFood():
                        food.store = food.store - 1
                        if food.store == 0:
                            food.remove()
                    self.state = StoreFood(host, takeFood, SCENT_FOOD)

            def visitLouse(self, louse):
                if louse.milk > 0:
                    def milkLouse():
                        louse.milk = louse.milk - 1
                    self.state = StoreFood(host, milkLouse, SCENT_LICE, "milk")

        lookup = FoodLookup()
        self.grid.accept(self.x, self.y, lookup)
        return lookup.state

    def _checkHill(self):

        class AntQueenLookup:
            def __init__(self):
                self.foundQueen = False

            def visitAntQueen(self, queen):
                self.foundQueen = True

        lookup = AntQueenLookup()
        for x, y in self.grid.square(self.x, self.y):
            self.grid.accept(x, y, lookup)
            if lookup.foundQueen:
                self._setLeavingHill()

        foodX, foodY, foodScent = self.findScent(TRAIL_FOOD)
        liceX, liceY, liceScent = self.findScent(TRAIL_LICE)
        if foodScent > liceScent:
            return FollowingScent(self, foodX, foodY, TRAIL_FOOD)
        elif liceScent > 0:
            return FollowingScent(self, liceX, liceY, TRAIL_LICE)

    def _setLeavingHill(self):
        self.pheromones.add(SCENT_HILL)
        self.pheromones.discard(SCENT_LICE)
        self.pheromones.discard(SCENT_FOOD)

    def _setFood(self, foodScent):
        self.pheromones.discard(SCENT_HILL)
        self._food = foodScent
        self.pheromones.add(foodScent)

    def _hasFood(self):
        return self._food is not None

    def move(self):
        return self.state.move()

    def isDead(self):
        return self.state.dead
