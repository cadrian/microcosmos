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
The graphical elements, to be plugged into PySGE.
"""

from net.cadrian.microcosmos.widgets.bugs import RedAntFemale, RedAntQueen, RedAntSoldier, RedAntWorker
from net.cadrian.microcosmos.widgets.button import TemplateButton
from net.cadrian.microcosmos.widgets.grid import Grid
from net.cadrian.microcosmos.widgets.landscape import Grass, Sand, Soil, Wall, Water


builtins = {
    "templateButton": TemplateButton,

    "grid": Grid,

    "grass": Grass,
    "sand": Sand,
    "soil": Soil,
    "wall": Wall,
    "water": Water,

    "redAntFemale": RedAntFemale,
    "redAntQueen": RedAntQueen,
    "redAntSoldier": RedAntSoldier,
    "redAntWorker": RedAntWorker,
}
