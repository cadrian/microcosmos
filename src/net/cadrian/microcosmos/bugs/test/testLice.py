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
import unittest

from net.cadrian.microcosmos.grid import Grid
from net.cadrian.microcosmos.bugs import Louse
from net.cadrian.microcosmos.landscape import Grass, Sand, Soil

from pysge.utils.logger import getLogger


_LOGGER = getLogger(__name__)


NO_SPRITE = "no sprite"


class LouseTestCase(unittest.TestCase):
    def setUp(self):
        self.grid = Grid(5, 5)
        def louseFactory(life):
            return Louse(self.grid, NO_SPRITE, louseFactory, life=life)
        self.louse = louseFactory(life=10)

    def test01a(self):
        """ lice just die on sand; they don't produce milk """
        self.grid.put(2, 2, Sand(self.grid))
        self.grid.put(2, 2, self.louse)
        self.louse.prepareToMove()
        self.assertEquals(9, self.louse._life)

    def test01b(self):
        """ lice strive on soil; they reproduce but they don't produce milk """
        self.grid.put(2, 2, Soil(self.grid))
        self.grid.put(2, 2, self.louse)
        self.louse.prepareToMove()
        self.assertEquals(9, self.louse._life)
        newLouse = self.louse.move()
        self.assertTrue(self.grid.has(2, 2, self.louse))
        self.assertEquals(5, self.louse._life)
        self.assertEquals(0, self.louse._milk)
        lice = [(x,y) for x, y in self.grid.square(2, 2) if self.grid.has(x, y, newLouse)]
        self.assertEquals(1, len(lice))
        self.assertEquals(4, newLouse._life)
        self.assertEquals(0, newLouse._milk)

    def test01c(self):
        """ lice strive on grass; they reproduce and produce milk """
        self.grid.put(2, 2, Grass(self.grid))
        self.grid.put(2, 2, self.louse)
        self.louse.prepareToMove()
        self.assertEquals(9, self.louse._life)
        newLouse = self.louse.move()
        self.assertTrue(self.grid.has(2, 2, self.louse))
        self.assertEquals(5, self.louse._life)
        self.assertEquals(1, self.louse._milk)
        lice = [(x,y) for x, y in self.grid.square(2, 2) if self.grid.has(x, y, newLouse)]
        self.assertEquals(1, len(lice))
        self.assertEquals(4, newLouse._life)
        self.assertEquals(0, newLouse._milk)


if __name__ == "__main__":
    import logging
    from pysge.utils.logger import setupTestLogging
    setupTestLogging(logging.DEBUG)
    unittest.main()
