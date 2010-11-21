import unittest

from net.cadrian.microcosmos.grid import Grid
from net.cadrian.microcosmos.bugs import AntFemale

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
        target = ant.target
        self.grid.put(2, 2, ant)
        self.grid.put(0, 0, target)
        self.grid.diffuse()
        ant.prepareToMove()
        self.assertEquals("exploration", str(ant.state))

    def test02(self):
        """ target detected => following the scent """
        ant = AntFemale(self.grid, randomizer=DeterministRandomizer())
        target = ant.target
        self.grid.put(2, 2, ant)
        self.grid.put(0, 0, target)
        self.grid.diffuse()
        self.grid.diffuse()
        ant.prepareToMove()
        self.assertEquals("followingTarget", str(ant.state))

    def test03(self):
        """ target reached => staying there """
        ant = AntFemale(self.grid, randomizer=DeterministRandomizer())
        target = ant.target
        self.grid.put(2, 2, ant)
        self.grid.put(2, 2, target)
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
        target = ant.target
        self.grid.put(2, 2, ant)
        self.grid.put(0, 0, target)
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
        target = ant.target
        self.grid.put(2, 2, ant)
        self.grid.put(2, 2, target)
        self.grid.diffuse()
        self.grid.diffuse()
        ant.prepareToMove()
        self.assertEquals("foundTarget", str(ant.state))
        ant.move()
        self.assertEquals((2, 2), (ant.x, ant.y))


if __name__ == "__main__":
    unittest.main()
