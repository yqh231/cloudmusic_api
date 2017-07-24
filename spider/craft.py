class countcalls(object):
   "Decorator that keeps track of the number of times a function is called."

   __instances = {}

   def __init__(self, f):
      self.__f = f
      self.__numcalls = 0
      countcalls.__instances[f] = self

   def __call__(self, *args, **kwargs):
      self.__numcalls += 1
      return self.__f(*args, **kwargs)

   def count(self):
      "Return the number of times the function f was called."
      return countcalls.__instances[self.__f].__numcalls

   @staticmethod
   def counts():
      "Return a dict of {function: # of calls} for all registered functions."
      return dict([(f.__name__, countcalls.__instances[f].__numcalls) for f in countcalls.__instances])

#example

@countcalls
def f():
   print ('f called')

@countcalls
def g():
   print ('g called')

f()
f()
f()
print (f.count()) # prints 3
print (countcalls.counts()) # same as f.counts() or g.counts()
g()
print (g.count()) # prints 1