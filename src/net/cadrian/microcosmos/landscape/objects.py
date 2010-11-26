from net.cadrian.microcosmos.grid import LocatedObject


class LandscapeFeature(LocatedObject):
    def __init__(self, grid):
	LocatedObject.__init__(self, grid)
	self.pheromones = []

    def allowTogether(self, other):
	return True


class Grass(LandscapeFeature):
    pass


class Sand(LandscapeFeature):
    pass


class Soil(LandscapeFeature):
    pass


class Wall(LandscapeFeature):
    def allowTogether(self, other):
	return False


class Water(LandscapeFeature):
    def allowTogether(self, other):
	return False
