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
import inspect

class ContractException(Exception): pass


def checkAssertion(instance, assertion, locals):
    if callable(assertion):
        if assertion(instance):
            return None
        return assertion.__name__
    try:
        assertionLocals = {"self": instance}
        assertionLocals.update(locals)
        if not eval(str(assertion), globals(), assertionLocals):
            return str(assertion)
    except Exception, e:
        return "%s - %s" % (assertion, e)


def checkAssertions(instance, assertions, locals):
    for assertion in assertions:
        error = checkAssertion(instance, assertion, locals)
        if error:
            return error


def checkInvariant(instance, cls):
    for c in inspect.getmro(cls)[1::-1]:
        error = checkAssertions(instance, c._invariants_, {})
        if error:
            raise ContractException(error)


def checkPrecondition(instance, name, locals):
    def check(cls):
        if hasattr(cls, name):
            c_feature = getattr(cls, name)
            if hasattr(c_feature, "_preconditions"):
                error = checkAssertions(instance, c_feature._preconditions, locals)
                if error:
                    return error

    checks = filter(lambda x: x is not None, map(check, inspect.getmro(instance.__class__)[1::-1]))
    if len(checks):
        raise ContractException("\n".join(checks))


def checkPostcondition(instance, name, locals):
    for cls in inspect.getmro(instance.__class__)[1::-1]:
        if hasattr(cls, name):
            c_feature = getattr(cls, name)
            if hasattr(c_feature, "_postconditions"):
                error = checkAssertions(instance, c_feature._postconditions, locals)
                if error:
                    raise ContractException(error)


def match(spec, instance, *a, **kw):
    values = []
    n = len(spec.args)
    if n > 0 and spec.args[0] == 'self':
        values.append(instance)
        n = n - 1

    values.extend(a)
    n = n - len(a)

    if spec.defaults is None:
        values.extend([None] * n)
    else:
        values.extend([None] * (n - len(spec.defaults)))
        values.extend(spec.defaults)

    result = dict(zip(spec.args, values))
    result.update(kw)
    return result


class ContractObject(object):
    def __new__(cls, *a, **kw):
        for c in inspect.getmro(cls)[:-1]:
            if not hasattr(c, "_invariants_"):
                c._invariants_ = []
        result = object.__new__(cls)
        result.__init__(*a, **kw)
        checkInvariant(result, cls)
        return result

    def __getattribute__(self, name):
        feature = object.__getattribute__(self, name)
        if not callable(feature) or name.startswith('__'):
            return feature

        spec = inspect.getargspec(feature)
        def dbc(*a, **kw):
            checkInvariant(self, self.__class__)
            checkPrecondition(self, name, match(spec, self, *a, **kw))
            result = feature(*a, **kw)
            kw["result"] = result
            checkPostcondition(self, name, match(spec, self, *a, **kw))
            checkInvariant(self, self.__class__)
            return result

        dbc.__name__ = feature.__name__
        return dbc


def invariant(*args):
    def dec(clazz):
        class deco(clazz):
            def __new__(cls, *a, **kw):
                result = clazz.__new__(cls, *a, **kw)
                map(cls._invariants_.append, args)
                checkInvariant(result, cls)
                return result
        deco.__name__ = clazz.__name__
        return deco
    return dec


def require(*args):
    def dec(feature):
        if not hasattr(feature, "_preconditions"):
            feature._preconditions = []
        feature._preconditions.extend(args)
        return feature
    return dec


def ensure(*args):
    def dec(feature):
        if not hasattr(feature, "_postconditions"):
            feature._postconditions = []
        feature._postconditions.extend(args)
        return feature
    return dec
