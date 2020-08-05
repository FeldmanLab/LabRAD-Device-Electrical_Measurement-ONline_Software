import os
print(__file__)
path = os.path.dirname(os.path.realpath(__file__))
print(os.path.join(path,'..'))
os.chdir(os.path.join(os.path.join(os.path.dirname(__file__), '..'),'Resources'))
