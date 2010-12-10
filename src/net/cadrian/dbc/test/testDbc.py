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

from net.cadrian.dbc import ContractException, ContractObject, invariant, require, ensure

def positive(instance):
    return instance.x > 0

def inrange(instance):
    return instance.x < 5

@invariant(positive)
class A(ContractObject):
    def __init__(self):
        self.x = 1
    def nop(self):
        pass

@invariant(inrange)
class B(A):
    def __init__(self, x=1):
        self.x = x

    @require("x > 0")
    @ensure("self.x == x")
    def setx(self, x, y=0):
        self.x = x

class InvariantTestCase(unittest.TestCase):

    def test01(self):
        """ class invariant """
        a = A()
        a.x = -1
        self.failUnlessRaises(ContractException, a.nop)

    def test02(self):
        """ invariant is inherited """
        a = B()
        a.x = -1
        self.failUnlessRaises(ContractException, a.nop)

    def test03a(self):
        """ invariant is verified on constructor too """
        self.failUnlessRaises(ContractException, B, -1)

    def test03b(self):
        """ B has its own invariant too """
        self.failUnlessRaises(ContractException, B, 6)

    def test04a(self):
        """ normal setx works """
        a = B(1)
        self.assertEquals(1, a.x)
        a.setx(4)
        self.assertEquals(4, a.x)
        a.setx(x=2)
        self.assertEquals(2, a.x)

    def test04b(self):
        """ making precondition fail """
        a = B(2)
        self.assertEquals(2, a.x)
        self.failUnlessRaises(ContractException, a.setx, -1)



if __name__ == '__main__':
    unittest.main()