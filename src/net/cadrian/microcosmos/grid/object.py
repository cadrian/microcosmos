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
class LocatedObject:
    def __init__(self, grid):
        self.x = None
        self.y = None
        self.grid = grid

    def onGridPut(self, x, y):
        self.x = x
        self.y = y

    def onGridRemove(self, x, y):
        self.x = None
        self.y = None

    def moveTo(self, x, y):
        self.grid.remove(self.x, self.y, self)
        self.grid.put(x, y, self)

    def remove(self):
        self.grid.remove(self.x, self.y, self)
