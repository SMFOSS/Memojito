from functools import wraps
import collections


class Memojito(object):
    """
    The memojito provides a series of decorators for managing method
    memos on an instance.
    """
    
    propname = '_memojito_'

    def clear(self, inst):
        if hasattr(inst, self.propname):
            delattr(inst, self.propname)

    def clearbefore(self, func):
        @wraps(func)
        def clear(*args, **kwargs):
            inst=args[0]
            self.clear(inst)
            return func(*args, **kwargs)
        return clear
    
    def clearafter(self, func):
        @wraps(func)
        def clear(*args, **kwargs):
            inst=args[0]
            val = func(*args, **kwargs)
            self.clear(inst)
            return val 
        return clear

    def get_key(self, func, args, **kwargs):
        inst = args[0]
        clean_args = list(args)
        for i, a in enumerate(args):
            if a is inst:
                # avoid issues with mutable subclasses
                clean_args[i] = id(a)
                continue
            if not isinstance(a, collections.Hashable):
                # safety over guaranteed accuracy.  if you are passing
                # large multidimensional dicts into a memoize function,
                # you might want to reconsider your approach.
                clean_args[i] = frozenset(a)

        # XXX this could be potentially big, a custom key should
        # be used if the arguments are expected to be big
                    
        key = (func.__name__, tuple(clean_args), frozenset(kwargs.items()))
        return key

    def memoize(self, func):
        @wraps(func)
        def memogetter(*args, **kwargs):
            inst = args[0]
            cache = getattr(inst, self.propname, None)
            if cache is None:
                setattr(inst, self.propname, {})
                cache = getattr(inst, self.propname)

            key = self.get_key(func, args, **kwargs)
            
            val = cache.get(key)
            if val is None:
                val=func(*args, **kwargs)
                cache[key]=val
                setattr(inst, self.propname, cache)
            return val
        return memogetter





