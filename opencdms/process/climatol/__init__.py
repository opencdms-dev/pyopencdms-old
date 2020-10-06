import os

import rpy2.robjects as ro
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter


def windrose(obs):
    r = ro.r

    script = os.path.join(
        os.path.dirname(__file__),
        'windrose.r',
    )
    r.source(script)

    with localconverter(ro.default_converter + pandas2ri.converter):
        _obs = ro.conversion.py2rpy(obs)

    _windrose = ro.globalenv['windrose']

    r(_windrose(_obs, 'Sxxx', 'Some place'))
    input()
