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
Ant soldiers: the hill's gardians, they attack ennemy ants.
"""

from net.cadrian.microcosmos.model.grid import LocatedObject
from net.cadrian.microcosmos.model.bugs.ant import AbstractAnt
from net.cadrian.microcosmos.model.bugs.pheromones import PheromoneKind, Pheromone


class AntSoldier(AbstractAnt):
    def __init__(self, grid, sprite, life=100):
        AbstractAnt.__init__(self, grid, sprite, life=life)
        self.pheromones = []
