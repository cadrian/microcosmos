import unittest

from net.cadrian.microcosmos.grid import Grid


class PheromoneKind:
    def __init__(self, diffusion):
        self.diffusion = diffusion

PHEROMONE = PheromoneKind(0.125)


class Pheromone:
    def __init__(self, kind, value):
        self.kind = kind
        self._value = value

    def fixScent(self, value):
        return self._value + value


class AntiPheromone:
    def __init__(self, kind, diffusion):
        self.kind = kind
        self._diffusion = diffusion

    def fixScent(self, value):
        return self._diffusion * value


class Bug:
    """ Bugs diffuse pheromones """
    def __init__(self, pheromoneKind, pheromoneValue):
        self.pheromones = [Pheromone(kind=pheromoneKind, value=pheromoneValue)]


class Wall:
    """ Walls block pheromones """
    def __init__(self, pheromoneKind):
        self.pheromones = [AntiPheromone(kind=pheromoneKind, diffusion=0)]


class Pond:
    """ Ponds slow the pheromones diffusion """
    def __init__(self, pheromoneKind):
        self.pheromones = [AntiPheromone(kind=pheromoneKind, diffusion=0.25)]


class DiffusionTestCase(unittest.TestCase):
    def test01(self):
        """ one bug """

        grid = Grid(5, 5)
        bug = Bug(pheromoneKind=PHEROMONE, pheromoneValue=4)
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
        bug1 = Bug(pheromoneKind=PHEROMONE, pheromoneValue=4)
        bug2 = Bug(pheromoneKind=PHEROMONE, pheromoneValue=2)
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
        bug = Bug(pheromoneKind=PHEROMONE, pheromoneValue=4)

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

    def test04(self):
        """ one bug, one wall """

        grid = Grid(5, 5)
        bug = Bug(pheromoneKind=PHEROMONE, pheromoneValue=4)
        wall1 = Wall(pheromoneKind=PHEROMONE)
        wall2 = Wall(pheromoneKind=PHEROMONE)
        wall3 = Wall(pheromoneKind=PHEROMONE)
        wall4 = Wall(pheromoneKind=PHEROMONE)
        wall5 = Wall(pheromoneKind=PHEROMONE)

        grid.put(2, 2, bug)
        grid.put(1, 0, wall1)
        grid.put(1, 1, wall2)
        grid.put(1, 2, wall3)
        grid.put(1, 3, wall4)
        grid.put(1, 4, wall5)

        grid.diffuse()
        self.assertEquals(0, grid.scent(1, 1, PHEROMONE))
        self.assertEquals(4, grid.scent(2, 2, PHEROMONE))

        grid.diffuse()
        self.assertEquals(0   , grid.scent(0, 0, PHEROMONE))
        self.assertEquals(0   , grid.scent(0, 1, PHEROMONE))
        self.assertEquals(0   , grid.scent(0, 2, PHEROMONE))
        self.assertEquals(0   , grid.scent(1, 1, PHEROMONE))
        self.assertEquals(0.5 , grid.scent(2, 1, PHEROMONE))
        self.assertEquals(0   , grid.scent(2, 0, PHEROMONE))
        self.assertEquals(4   , grid.scent(2, 2, PHEROMONE))

        grid.diffuse()
        self.assertEquals(0     , grid.scent(0, 0, PHEROMONE))
        self.assertEquals(0     , grid.scent(0, 1, PHEROMONE))
        self.assertEquals(0     , grid.scent(0, 2, PHEROMONE))
        self.assertEquals(0     , grid.scent(1, 1, PHEROMONE))
        self.assertEquals(0.625 , grid.scent(2, 1, PHEROMONE))
        self.assertEquals(0.125 , grid.scent(2, 0, PHEROMONE))
        self.assertEquals(4.3125, grid.scent(2, 2, PHEROMONE))

    def test05(self):
        """ one bug, one pond """

        grid = Grid(5, 5)
        bug = Bug(pheromoneKind=PHEROMONE, pheromoneValue=4)
        pond1 = Pond(pheromoneKind=PHEROMONE)
        pond2 = Pond(pheromoneKind=PHEROMONE)
        pond3 = Pond(pheromoneKind=PHEROMONE)
        pond4 = Pond(pheromoneKind=PHEROMONE)
        pond5 = Pond(pheromoneKind=PHEROMONE)

        grid.put(2, 2, bug)
        grid.put(1, 0, pond1)
        grid.put(1, 1, pond2)
        grid.put(1, 2, pond3)
        grid.put(1, 3, pond4)
        grid.put(1, 4, pond5)

        grid.diffuse()
        self.assertEquals(0, grid.scent(1, 1, PHEROMONE))
        self.assertEquals(4, grid.scent(2, 2, PHEROMONE))

        grid.diffuse()
        self.assertEquals(0    , grid.scent(0, 0, PHEROMONE))
        self.assertEquals(0    , grid.scent(0, 1, PHEROMONE))
        self.assertEquals(0    , grid.scent(0, 2, PHEROMONE))
        self.assertEquals(0.125, grid.scent(1, 1, PHEROMONE))
        self.assertEquals(0.5  , grid.scent(2, 1, PHEROMONE))
        self.assertEquals(0    , grid.scent(2, 0, PHEROMONE))
        self.assertEquals(4    , grid.scent(2, 2, PHEROMONE))

        grid.diffuse()
        self.assertEquals(0.015625  , grid.scent(0, 0, PHEROMONE))
        self.assertEquals(0.03125   , grid.scent(0, 1, PHEROMONE))
        self.assertEquals(0.046875  , grid.scent(0, 2, PHEROMONE))
        self.assertEquals(0.14453125, grid.scent(1, 1, PHEROMONE))
        self.assertEquals(0.65625   , grid.scent(2, 1, PHEROMONE))
        self.assertEquals(0.140625  , grid.scent(2, 0, PHEROMONE))
        self.assertEquals(4.359375  , grid.scent(2, 2, PHEROMONE))


if __name__ == "__main__":
    unittest.main()
