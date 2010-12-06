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
The grid provides the framework universe: cells for the bugs to go to,
smells for the pheromones to diffuse...
"""


def coordinates(width, height):
    for x in range(width):
        for y in range(height):
            yield (x, y)

def square():
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if dx != 0 or dy != 0:
                yield (dx, dy)


class MoveError(Exception):
    pass


class Scent:
    """ The accumulated scent of a pheromone of some kind on a cell """

    def __init__(self, pheromoneKind):
        self._pheromoneKind = pheromoneKind
        self.value = 0
        self._next = 0

    def diffuseScent(self, square):
        initial = self.value
        squareValues = [cell._scents[self._pheromoneKind].value for cell in square]
        def add(value, more):
            return value + (more - initial)
        self._next = self._next + self._pheromoneKind.diffusion * reduce(add, squareValues, 0)

    def fixScent(self, pheromone):
        self._next = pheromone.fixScent(self._next)

    def commitDiffusion(self):
        self.value = self._next


class NoScent():
    """ The null-object pattern """

    def __init__(self):
        self.value = 0

NO_SCENT = NoScent()


class Cell:
    """ One cell of a grid. Contains objects and diffuses pheromones accumulated in scents """

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self._objects = set()
        self._scents = {}

    def put(self, obj):
        self._objects.add(obj)
        obj.onGridPut(self.x, self.y)

    def remove(self, obj):
        self._objects.remove(obj)
        obj.onGridRemove(self.x, self.y)

    def has(self, obj):
        return obj in self._objects

    def _ensurePheromone(self, pheromoneKind, quantity=0):
        if not self._scents.has_key(pheromoneKind):
            self._scents[pheromoneKind] = Scent(pheromoneKind)
            self._scents[pheromoneKind].value += quantity

    def scent(self, pheromoneKind):
        return self._scents.get(pheromoneKind, NO_SCENT).value

    def _ensurePheromones(self):
        self._allPheromones = set()
        map(self._allPheromones.update, [obj.pheromones for obj in self._objects])

        def ensure(pheromone):
            self._ensurePheromone(pheromone.kind)
        map(ensure, self._allPheromones)

    def _diffuseScents(self, square):
        def diffuse((pheromoneKind, scent)):
            def ensure(cell):
                cell._ensurePheromone(pheromoneKind)
            map(ensure, square)
            scent.diffuseScent(square)
        map(diffuse, self._scents.iteritems())

    def _fixPheromones(self):
        def fix(pheromone):
            self._scents[pheromone.kind].fixScent(pheromone)
        map(fix, self._allPheromones)

    def diffuseScent(self, square):
        self._ensurePheromones()
        self._diffuseScents(square)
        self._fixPheromones()

    def commitDiffusion(self):
        for scent in self._scents.values():
            scent.commitDiffusion()

    def accept(self, visitor):
        def acceptObject(object):
            object.accept(visitor)
        map(acceptObject, self._objects)


class Grid:
    def __init__(self, width, height, cellFactory=Cell, mover=None):
        self.width = width
        self.height = height
        self._cells = [cellFactory(x, y) for x, y in coordinates(self.width, self.height)]
        self._mover = mover or self.forceMove

    def __iter__(self):
        for cell in self._cells:
            yield cell

    def row(self, y):
        return [self.cell(x, y) for x in range(self.width)]

    def column(self, x):
        return [self.cell(x, y) for y in range(self.height)]

    def cell(self, x, y):
        x = (x + self.width ) % self.width
        y = (y + self.height) % self.height
        return self._cells[x * self.height + y]

    def put(self, x, y, obj):
        self.cell(x, y).put(obj)

    def remove(self, x, y, obj):
        self.cell(x, y).remove(obj)

    def forceMove(self, x, y, obj):
        self.remove(obj.x, obj.y, obj)
        self.put(x, y, obj)

    def move(self, x, y, obj):
        self._mover(x, y, obj)

    def diffuse(self):
        def begin((x, y)):
            self.cell(x, y).diffuseScent([self.cell(x+dx, y+dy) for dx, dy in square()])
        def commit((x, y)):
            self.cell(x, y).commitDiffusion()
        map(begin , coordinates(self.width, self.height))
        map(commit, coordinates(self.width, self.height))

    def square(self, x, y):
        return [(x+dx, y+dy) for dx, dy in square()]

    def scent(self, x, y, pheromoneKind):
        return self.cell(x, y).scent(pheromoneKind)

    def has(self, x, y, obj):
        return self.cell(x, y).has(obj)

    def accept(self, x, y, visitor):
        self.cell(x, y).accept(visitor)

    def _ensurePheromone(self, x, y, pheromoneKind, quantity=0):
        self.cell(x, y)._ensurePheromone(pheromoneKind, quantity=quantity)
