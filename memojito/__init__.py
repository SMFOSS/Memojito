from memojito.memojito import Memojito


_m = Memojito()
memoize = _m.memoize
clearbefore = _m.clearbefore
clearafter = _m.clearafter
clear = _m.clear


def mproperty(func):
    return property(_m.memoize(func))
