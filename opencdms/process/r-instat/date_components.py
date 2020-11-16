from io import BytesIO
import logging
import os
import rpy2.robjects as ro
from rpy2.rinterface_lib.callbacks import logger as rpy2_logger
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter
from rpy2.robjects.packages import importr
import numpy as np
import time

# dates, a column of dates to extract the year from
# Question: what format will this come in from the database?
# start_month, the month (1 to 12) to start the year in. Default is 1 to start on 1 January.
# e.g. start_month = 8 defines a year from 1 August to 31 July.
# In such cases year_num returns the calendar year of the beginning of the year 
# e.g. year_num(["2020/08/10", "2021/01/20"], start_month = 8) = c(2020, 2020)  
def year_num(dates, start_month = 1):
    # Display errors from R, but not warnings
    rpy2_logger.setLevel(logging.ERROR)

    r = ro.r

    script = os.path.join(
        os.path.dirname(__file__),
        'yday_366.r',
    )
    r.source(script)

    base = importr("base")
    # This may need to change depending on the format of the dates parameter.
    # The following may be an alternative:
    # _dates = ro.vectors.DateVector(dates)
    _dates = base.as_Date(dates)
    _start_month = ro.vectors.IntVector([start_month])

    ro.globalenv['dates'] = _dates
    ro.globalenv['start_month'] = start_month

    r('''

    library("lubridate")
    if (!start_month %in% 1:12) stop("start_month must be an integer between 1 and 12. ", start_month, " is invalid.")
    year_col <- lubridate::year(dates)
    if (start_month > 1) {
        # Using a leap year as year to ensure consistent day of year across years.
        start_doy <- lubridate::yday(as.Date(paste("2000", start_month, 1), format = "%Y %m %d"))
        doy_col <- as.integer(yday_366(dates))
        s_doy <- doy_col - start_doy + 1
        s_year <- year_col
        s_year[s_doy < 1] <- year_col[s_doy < 1] - 1
        year_col <- s_year
    }

    ''')
    year_data = ro.globalenv['year_col']
    # Is this the correct Python structure to return?
    year_data = np.array(year_data)
    return year_data