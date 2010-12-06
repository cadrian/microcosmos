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
Some smelly chemical product that diffuses around.
"""

class PheromoneKind:
    def __init__(self, diffusion, name):
        self.diffusion = diffusion
        self.name = name

    def __str__(self):
        return self.name


class Pheromone:
    def __init__(self, kind, value):
        self.kind = kind
        self._value = value

    def fixScent(self, value):
        return self._value + value
