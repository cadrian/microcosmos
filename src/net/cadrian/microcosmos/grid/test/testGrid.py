import unittest

from net.cadrian.microcosmos.grid import Grid


class PheromoneKind:
    def __init__(self, diffusion):
        self.diffusion = diffusion

PHEROMONE = PheromoneKind(0.125)


class Pheromone:
    def __init__(self, kind, value):
        self.kind = kind
        self.value = value


class Bug:
    def __init__(self, pheromone):
        self.pheromones = [pheromone]


class DiffusionTestCase(unittest.TestCase):
    def test01(self):
        """ one bug """

        grid = Grid(5, 5)
        bug = Bug(pheromone=Pheromone(kind=PHEROMONE, value=4))
        grid.put(2, 2, bug)

        grid.diffuse()
        self.assertEquals(4, grid.scent(2, 2, PHEROMONE))

        grid.diffuse()
        self.assertEquals(0.5, grid.scent(1, 1, PHEROMONE))
        self.assertEquals(4  , grid.scent(2, 2, PHEROMONE))

        grid.diffuse()
        self.assertEquals(0.0625, grid.scent(0, 0, PHEROMONE))
        self.assertEquals(0.125 , grid.scent(0, 1, PHEROMONE))
        self.assertEquals(0.1875, grid.scent(0, 2, PHEROMONE))
        self.assertEquals(0.625 , grid.scent(1, 1, PHEROMONE))
        self.assertEquals(4.5   , grid.scent(2, 2, PHEROMONE))

    def test02(self):
        """ two bugs with the same scent """

        grid = Grid(5, 5)
        bug1 = Bug(pheromone=Pheromone(kind=PHEROMONE, value=4))
        bug2 = Bug(pheromone=Pheromone(kind=PHEROMONE, value=2))
        grid.put(2, 2, bug1)
        grid.put(1, 1, bug2)

        grid.diffuse()
        self.assertEquals(2, grid.scent(1, 1, PHEROMONE))
        self.assertEquals(4, grid.scent(2, 2, PHEROMONE))

        grid.diffuse()
        self.assertEquals(2.5 , grid.scent(1, 1, PHEROMONE))
        self.assertEquals(4.25, grid.scent(2, 2, PHEROMONE))

        grid.diffuse()
        self.assertEquals(2.875 , grid.scent(1, 1, PHEROMONE))
        self.assertEquals(4.8125, grid.scent(2, 2, PHEROMONE))

    def test03(self):
        """ one moving bug """

        grid = Grid(5, 5)
        bug = Bug(pheromone=Pheromone(kind=PHEROMONE, value=4))

        grid.put(2, 2, bug)
        grid.diffuse()
        self.assertEquals(4, grid.scent(2, 2, PHEROMONE))

        grid.remove(2, 2, bug)
        grid.put(2, 3, bug)
        grid.diffuse()
        self.assertEquals(0.5, grid.scent(1, 1, PHEROMONE))
        self.assertEquals(0  , grid.scent(2, 2, PHEROMONE))
        self.assertEquals(4.5, grid.scent(2, 3, PHEROMONE))

        grid.remove(2, 3, bug)
        grid.put(3, 3, bug)
        grid.diffuse()
        self.assertEquals(0.0625, grid.scent(0, 0, PHEROMONE))
        self.assertEquals(0.125 , grid.scent(0, 1, PHEROMONE))
        self.assertEquals(0.1875, grid.scent(0, 2, PHEROMONE))
        self.assertEquals(0.125 , grid.scent(1, 1, PHEROMONE))
        self.assertEquals(1     , grid.scent(2, 2, PHEROMONE))
        self.assertEquals(0.25  , grid.scent(2, 3, PHEROMONE))
        self.assertEquals(4.625 , grid.scent(3, 3, PHEROMONE))


if __name__ == "__main__":
    unittest.main()
