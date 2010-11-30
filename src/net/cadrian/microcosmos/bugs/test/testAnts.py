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
from net.cadrian.microcosmos.bugs import AntFemale, AntFemaleTarget, AntQueen, AntWorker
from net.cadrian.microcosmos.landscape import Grass, Sand, Soil


class DeterministRandomizer:
    def accept(self):
        return True


class AntFemaleTestCase(unittest.TestCase):
    def setUp(self):
        self.grid = Grid(5, 5)

    def test01a(self):
        """ no target => exploration """
        ant = AntFemale(self.grid, randomizer=DeterministRandomizer())
        self.grid.put(2, 2, ant)
        self.grid.diffuse()
        ant.prepareToMove()
        self.assertEquals("exploration", str(ant.state))

    def test01b(self):
        """ target not detected => exploration """
        ant = AntFemale(self.grid, randomizer=DeterministRandomizer())
        target = AntFemaleTarget(self.grid)
        self.grid.put(2, 2, ant)
        self.grid.put(0, 0, target)
        ant.goToTarget(target)
        self.grid.diffuse()
        ant.prepareToMove()
        self.assertEquals("exploration", str(ant.state))

    def test02(self):
        """ target detected => following the scent """
        ant = AntFemale(self.grid, randomizer=DeterministRandomizer())
        target = AntFemaleTarget(self.grid)
        self.grid.put(2, 2, ant)
        self.grid.put(0, 0, target)
        ant.goToTarget(target)
        self.grid.diffuse()
        self.grid.diffuse()
        ant.prepareToMove()
        self.assertEquals("followingTarget", str(ant.state))

    def test03(self):
        """ target reached => staying there """
        ant = AntFemale(self.grid, randomizer=DeterministRandomizer())
        target = AntFemaleTarget(self.grid)
        self.grid.put(2, 2, ant)
        self.grid.put(2, 2, target)
        ant.goToTarget(target)
        ant.prepareToMove()
        self.assertEquals("foundTarget", str(ant.state))

    def test04(self):
        """ ant movement in exploration """
        ant = AntFemale(self.grid, randomizer=DeterministRandomizer())
        self.grid.put(2, 2, ant)
        self.grid.diffuse()
        ant.prepareToMove()
        self.assertEquals("exploration", str(ant.state))
        ant.move()
        self.assertNotEquals((2, 2), (ant.x, ant.y))

    def test05(self):
        """ ant movement in target follow """
        ant = AntFemale(self.grid, randomizer=DeterministRandomizer())
        target = AntFemaleTarget(self.grid)
        self.grid.put(2, 2, ant)
        self.grid.put(0, 0, target)
        ant.goToTarget(target)
        self.grid.diffuse()
        self.grid.diffuse()
        ant.prepareToMove()
        self.assertEquals("followingTarget", str(ant.state))
        ant.move()
        self.assertEquals((1, 1), (ant.x, ant.y))
        ant.prepareToMove()
        ant.move()
        self.assertEquals((0, 0), (ant.x, ant.y))

    def test06(self):
        """ ant movement when target reached """
        ant = AntFemale(self.grid, randomizer=DeterministRandomizer())
        target = AntFemaleTarget(self.grid)
        self.grid.put(2, 2, ant)
        self.grid.put(2, 2, target)
        ant.goToTarget(target)
        self.grid.diffuse()
        self.grid.diffuse()
        ant.prepareToMove()
        self.assertEquals("foundTarget", str(ant.state))
        ant.move()
        self.assertEquals((2, 2), (ant.x, ant.y))

    def test07(self):
        """ ants die """
        ant = AntFemale(self.grid, life=3, randomizer=DeterministRandomizer())
        target = AntFemaleTarget(self.grid)
        self.grid.put(2, 2, ant)
        self.grid.put(2, 2, target)
        ant.goToTarget(target)
        self.grid.diffuse()
        self.grid.diffuse()
        ant.prepareToMove()
        ant.move()
        self.assertFalse(ant.isDead())
        ant.prepareToMove()
        ant.move()
        self.assertFalse(ant.isDead())
        ant.prepareToMove()
        ant.move()
        self.assertTrue(ant.isDead())
        self.assertEquals((None, None), (ant.x, ant.y))

    def test08(self):
        """ a female that reaches its target on soil becomes a queen """
        ant = AntFemale(self.grid, life=3, randomizer=DeterministRandomizer())
        target = AntFemaleTarget(self.grid)
        self.grid.put(2, 2, Soil(self.grid))
        self.grid.put(2, 2, ant)
        self.grid.put(2, 2, target)
        ant.goToTarget(target)
        self.grid.diffuse()
        self.grid.diffuse()
        ant.prepareToMove()
        self.assertEquals("foundTarget", str(ant.state))
        ant.move()
        queen = self.grid.bug(2, 2)
        self.assertNotEquals(ant, queen)
        self.assertEquals((2, 2), (queen.x, queen.y))
        self.assertEquals(AntQueen, queen.__class__)
        self.assertEquals(ant._life, queen._life)


class AntQueenTestCase(unittest.TestCase):
    def setUp(self):
        self.grid = Grid(5, 5)
        self.ant = AntQueen(self.grid, life=10, nextPosition=lambda square: square[0], nextAnt=lambda: (AntFemale, 4))

    def test01a(self):
        """ a queen that does not produce an ant does not lose life points """
        self.ant._next = None
        self.assert_(self.ant._createNext() is None)
        self.assertEquals(10, self.ant._life)

    def test01b(self):
        """ a queen that produces an ant loses some life """
        self.ant._next = lambda grid: AntFemale(grid)
        self.ant._cost = 1
        self.assertEquals(AntFemale, self.ant._createNext().__class__)
        self.assertEquals(9, self.ant._life)

    def test01c(self):
        """ a queen with not enough life left will not produce the ant """
        self.ant._life = 3
        self.ant._cost = 3
        self.ant._next = lambda grid: AntFemale(grid)
        self.assert_(self.ant._createNext() is None)
        self.assertEquals(3, self.ant._life)

    def test02a(self):
        """ a queen can produce ants on soil """
        self.grid.put(2, 2, Soil(self.grid))
        self.grid.put(2, 2, self.ant)
        self.assert_(self.ant._next is None)
        self.ant.prepareToMove()
        self.assert_(self.ant._next is not None)
        self.ant.move()
        self.assertEquals(AntFemale, self.grid.bug(1, 1).__class__)

    def test02b(self):
        """ a queen can produce ants on grass """
        self.grid.put(2, 2, Grass(self.grid))
        self.grid.put(2, 2, self.ant)
        self.assert_(self.ant._next is None)
        self.ant.prepareToMove()
        self.assert_(self.ant._next is not None)
        self.ant.move()
        self.assertEquals(AntFemale, self.grid.bug(1, 1).__class__)

    def test02c(self):
        """ a queen cannot produce ants on sand """
        self.grid.put(2, 2, Sand(self.grid))
        self.grid.put(2, 2, self.ant)
        self.assert_(self.ant._next is None)
        self.ant.prepareToMove()
        self.assert_(self.ant._next is None)
        self.ant.move()
        self.assert_(self.grid.bug(1, 1) is None)

    def test03(self):
        """ a dead queen produces nothing """
        self.grid.put(2, 2, Grass(self.grid))
        self.grid.put(2, 2, self.ant)
        self.assert_(self.ant._next is None)
        self.ant._life = 0
        self.ant.prepareToMove()
        self.assert_(self.ant._next is None)
        self.ant.move()
        self.assert_(self.grid.bug(1, 1) is None)


class AntWorkerTestCase(unittest.TestCase):
    from net.cadrian.microcosmos.bugs.antWorkers import TRAIL_HOME

    def setUp(self):
        self.grid = Grid(5, 5)
        self.queen = AntQueen(self.grid)
        self.ant = AntWorker(self.grid)

    def test01a(self):
        """ an ant moving from the hill leaves a trail -- note; the hill is the square around the queen -- ant in the hill """
        self.grid.put(2, 2, self.queen)
        self.grid.put(1, 1, self.ant)
        self.ant.prepareToMove()
        self.grid.diffuse()
        self.assertEquals(32, self.grid.scent(1, 1, self.TRAIL_HOME))

    def test01b(self):
        """ an ant moving from the hill leaves a trail -- note; the hill is the square around the queen -- ant outside the hill """
        self.grid.put(2, 2, self.queen)
        self.grid.put(0, 0, self.ant)
        self.ant.prepareToMove()
        self.grid.diffuse()
        self.assertEquals(0, self.grid.scent(0, 0, self.TRAIL_HOME))

    def test01c(self):
        """ an ant moving from the hill leaves a trail -- note; the hill is the square around the queen -- ant out of the fill but marked as coming from it """
        self.ant._setLeavingHome()
        self.grid.put(2, 2, self.queen)
        self.grid.put(0, 0, self.ant)
        self.ant.prepareToMove()
        self.grid.diffuse()
        self.assertEquals(32, self.grid.scent(0, 0, self.TRAIL_HOME))


if __name__ == "__main__":
    import logging
    from pysge.utils.logger import setupTestLogging
    setupTestLogging(logging.DEBUG)
    unittest.main()
