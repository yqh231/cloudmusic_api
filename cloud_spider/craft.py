import os
print (os.path.dirname(__file__))
print (os.path.pardir)
print(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)))