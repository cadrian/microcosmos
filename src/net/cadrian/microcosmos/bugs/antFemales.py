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

    def allowTogether(self, other):
        return other == self._ant


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
    def __init__(self, ant):
        self._ant = ant
        self.dead = False

    def __str__(self):
        return "foundTarget"

    def move(self):
        pass


class Dead:
    def __init__(self, ant):
        self._ant = ant
        self.dead = True

    def __str__(self):
        return "dead"

    def move(self):
        self._ant.remove()


class AntFemale(LocatedObject):
    def __init__(self, grid, life=100, randomizer=None):
        LocatedObject.__init__(self, grid)
        self._randomizer = randomizer or Randomizer()
        self.pheromones = []
        self.state = None
        self.target = Target(self)
        self._life = life

    def prepareToMove(self):
        self._life = self._life - 1
        if self._life <= 0:
            self.state = Dead(self)
        elif self.target.x == self.x and self.target.y == self.y:
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

    def isDead(self):
        return self.state.dead

    def allowTogether(self, other):
        return other == self.target
