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
from pysge.objects.base import BasicSprite
from pysge.utils.logger import getLogger

_LOGGER = getLogger(__name__)


class AbstractAnt(BasicSprite):
    def __init__(self, config):
        config.theme = "%s_ant_%s" % (self.ANT_COLOR, self.ANT_CASTE)
        config.layer = 2
        BasicSprite.__init__(self, config)


class RedAnt(AbstractAnt):
    ANT_COLOR = "red"


class RedAntFemale(RedAnt):
    ANT_CASTE = "female"


class RedAntQueen(RedAnt):
    ANT_CASTE = "queen"


class RedAntSoldier(RedAnt):
    ANT_CASTE = "soldier"


class RedAntWorker(RedAnt):
    ANT_CASTE = "worker"
