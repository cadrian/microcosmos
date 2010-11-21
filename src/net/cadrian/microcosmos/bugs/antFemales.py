import random

from net.cadrian.microcosmos.grid import LocatedObject
from net.cadrian.microcosmos.bugs.pheromones import PheromoneKind, Pheromone

TARGET_PHEROMONE_KIND = PheromoneKind(0.125)


class Target(LocatedObject):
    def __init__(self, ant):
        LocatedObject.__init__(self, ant.grid)
        self._ant = ant
        self.pheromone = Pheromone(TARGET_PHEROMONE_KIND, 16)
        self.pheromones = [self.pheromone]


class Randomizer:
    def accept(self):
        return random.randint(0, 100) != 50


class Exploration:
    def __init__(self, ant):
        self._ant = ant

    def __str__(self):
        return "exploration"

    def move(self):
        self._ant.moveTo(self._ant.x - 1, self._ant.y + 1)


class FollowingTarget:
    def __init__(self, ant, x, y):
        self._ant = ant
        self._x = x
        self._y = y

    def __str__(self):
        return "followingTarget"

    def move(self):
        self._ant.moveTo(self._x, self._y)


class FoundTarget:
    def __init__(self, ant):
        self._ant = ant

    def __str__(self):
        return "foundTarget"

    def move(self):
        pass


class AntFemale(LocatedObject):
    def __init__(self, grid, randomizer=None):
        LocatedObject.__init__(self, grid)
        self._randomizer = randomizer or Randomizer()
        self.pheromones = []
        self.state = ""
        self.target = Target(self)

    def prepareToMove(self):
        if self.target.x == self.x and self.target.y == self.y:
            self.state = FoundTarget(self)
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
