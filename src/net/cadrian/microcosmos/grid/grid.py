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
#
# Grid          contains many Cells
#
# Cell          contains many _objects ([Object])
#                    and many _scents ({PheromoneKind -> Scent})
#
# Scent         contains  one kind (PheromoneKind)
#                    and  one value (float)
#
# Object        contains many pheromones ([Pheromone])
#
# Pheromone     contains  one value (float)
#                    and  one kind (PheromoneKind)
#
# PheromoneKind contains  one diffusion (float)
#

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

    def allowMove(self, obj):
        def together(obj1, obj2):
            return obj1.allowTogether(obj2) and obj2.allowTogether(obj1)
        return all([together(obj, other) for other in self._objects])

    def put(self, obj):
        self._objects.add(obj)
        for pheromone in obj.pheromones:
            self._ensurePheromone(pheromone.kind)
        obj.onGridPut(self.x, self.y)

    def remove(self, obj):
        self._objects.remove(obj)
        obj.onGridRemove(self.x, self.y)

    def _ensurePheromone(self, pheromoneKind):
        if not self._scents.has_key(pheromoneKind):
            self._scents[pheromoneKind] = Scent(pheromoneKind)

    def scent(self, pheromoneKind):
        return self._scents.get(pheromoneKind, NO_SCENT).value

    def diffuseScent(self, square):
        for pheromoneKind, scent in self._scents.iteritems():
            for cell in square:
                cell._ensurePheromone(pheromoneKind)
            scent.diffuseScent(square)
        for obj in self._objects:
            for pheromone in obj.pheromones:
                self._scents[pheromone.kind].fixScent(pheromone)

    def commitDiffusion(self):
        for scent in self._scents.values():
            scent.commitDiffusion()


class Grid:
    def __init__(self, width, height, cellFactory=Cell):
        self.width = width
        self.height = height
        self._cells = [cellFactory(x, y) for x, y in coordinates(self.width, self.height)]

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

    def allowMove(self, x, y, obj):
        return self.cell(x, y).allowMove(obj)

    def put(self, x, y, obj):
        if not self.allowMove(x, y, obj):
            raise MoveError
        self.cell(x, y).put(obj)

    def remove(self, x, y, obj):
        self.cell(x, y).remove(obj)

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

