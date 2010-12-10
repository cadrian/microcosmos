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
The objects that live in grid cells.
"""

import random


from net.cadrian.dbc import ContractObject, require, ensure


class LocatedObject(ContractObject):
    def __init__(self, grid, sprite):
        self.x = None
        self.y = None
        self.grid = grid
        self.sprite = sprite
        self.pheromones = []

    def accept(self, visitor):
        visitorName = "visit" + self.__class__.__name__
        if hasattr(visitor, visitorName):
            getattr(visitor, "visit" + self.__class__.__name__)(self)

    @ensure("(x, y) == (self.x, self.y)")
    def onGridPut(self, x, y):
        self.x = x
        self.y = y

    @ensure("self.x is None and self.y is None")
    def onGridRemove(self, x, y):
        self.x = None
        self.y = None

    @require("self.x is None or self.grid.has(self.x, self.y, self)")
    @ensure("self.grid.has(x, y, self)")
    def moveTo(self, x, y):
        self.remove()
        self.grid.put(x, y, self)

    @ensure("self.x is None or not self.grid.has(self.x, self.y, self)")
    def remove(self):
        self.grid.remove(self.x, self.y, self)

    def isAlive(self):
        return False

    def getRandomTarget(self):
        return random.choice(self.grid.square(self.x, self.y))
