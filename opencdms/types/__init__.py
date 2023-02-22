from typing import NewType
from collections import namedtuple

Geography = NewType("Geography", str)
Coordinates = namedtuple("Coordinates",["longitude", "latitude"])