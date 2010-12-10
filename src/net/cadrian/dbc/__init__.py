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


def checkAssertion(instance, tag, assertion, globals, locals):
    if callable(assertion):
        if assertion(instance):
            return None
        return tag

    try:
        assertionLocals = {"self": instance}
        assertionLocals.update(locals)
        if not eval(str(assertion), globals, assertionLocals):
            return tag
    except Exception, e:
        return "%s - %s" % (tag, e)


def checkAssertions(instance, assertions, globals, locals):
    for tag, assertion in assertions.iteritems():
        error = checkAssertion(instance, tag, assertion, globals, locals)
        if error:
            return error


def checkInvariant(instance, cls):
    for c in inspect.getmro(cls)[1::-1]:
        error = checkAssertions(instance, c._invariants_, inspect.getmodule(c).__dict__, {})
        if error:
            raise ContractException(error)


def checkPrecondition(instance, name, locals):
    def check(cls):
        if hasattr(cls, name):
            c_feature = getattr(cls, name)
            if hasattr(c_feature, "_preconditions"):
                error = checkAssertions(instance, c_feature._preconditions, inspect.getmodule(cls).__dict__, locals)
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
                error = checkAssertions(instance, c_feature._postconditions, inspect.getmodule(cls).__dict__, locals)
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
                c._invariants_ = {}
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


def invariant(*args, **kwargs):
    def dec(clazz):
        class deco(clazz):
            def __new__(cls, *a, **kw):
                result = clazz.__new__(cls, *a, **kw)
                checkInvariant(result, cls)
                return result
        deco.__name__ = clazz.__name__
        deco.__module__ = clazz.__module__
        if not hasattr(clazz, "_invariants_"):
            clazz._invariants_ = {}
        clazz._invariants_.update(dict(zip([str(x) for x in args], args)))
        clazz._invariants_.update(kwargs)
        return deco
    return dec


def require(*args, **kwargs):
    def dec(feature):
        if not hasattr(feature, "_preconditions"):
            feature._preconditions = {}
        feature._preconditions.update(dict(zip([str(x) for x in args], args)))
        feature._preconditions.update(kwargs)
        return feature
    return dec


def ensure(*args, **kwargs):
    def dec(feature):
        if not hasattr(feature, "_postconditions"):
            feature._postconditions = {}
        feature._postconditions.update(dict(zip([str(x) for x in args], args)))
        feature._postconditions.update(kwargs)
        return feature
    return dec
