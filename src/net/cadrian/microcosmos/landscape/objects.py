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
