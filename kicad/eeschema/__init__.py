# TODO:
# 1. Recursive operation on sheets (offset ref)
# 2. Cleanup
# 3. Tests


from sch import Sch, A3_landscape, A4_landscape
from schItem import Component, NoConnect, TextItem
from schItem import Wire, Connection, Entry, Sheet, Bitmap

# Lengths
mil = 1.0
inch = 0.001
mm = inch / 2.54

# Angles
degree = 0.1


