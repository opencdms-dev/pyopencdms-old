# =================================================================
#
# Authors: Stephen Lloyd
#          Ian Edwards
#
# Copyright (c) 2020, OpenCDMS Project
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# =================================================================


def windrose(
    speed,
    direction,
    facet,
    n_directions=12,
    n_speeds=5,
    speed_cuts="NA",
    col_pal="GnBu",
    ggtheme="grey",
    legend_title="Wind Speed",
    calm_wind=0,
    variable_wind=990,
    n_col=1,
):
    """
    Plot a windrose showing the wind speed and direction for given
    facets using ggplot2.

    Args:

    * speed
        Numeric vector of wind speeds.
    * direction
        Numeric vector of wind directions.
    * facet
        Character or factor vector of the facets used to plot the
        various windroses.

    Kwargs:

    * n_directions
        The number of direction bins to plot (petals on the rose)
        (default 12).
    * n_speeds
        The number of equally spaced wind speed bins to plot.
        This is used if speed_cuts is NA (default 5).
    * speed_cuts
        Numeric vector containing the cut points for the wind speed
        intervals (default "NA").
    * col_pal
        Character string indicating the name of the brewer.pal.info
        colour palette to be used for plotting (default "GNBU").
    * ggtheme
        Character string (partially) matching the ggtheme to be used
        for plotting, may be "grey", "gray", "bw", "linedraw", "light",
        "minimal", "classic" (default "grey").
    * legend_title
        Character string to be used for the legend title
        (default "Wind Speed").
    * calm_wind
        The upper limit for wind speed that is considered calm (default 0).
    * variable_wind
        Numeric code for variable winds (if applicable) (default 990).
    * n_col
        The number of columns of plots (default 1).

    """
    # clifro::windrose(
    #     speed, direction, facet, n_directions=12, n_speeds=5, speed_cuts=NA,
    #     col_pal="GnBu", ggtheme=c(
    #         "grey", "gray", "bw", "linedraw", "light", "minimal", "classic"),
    #      legend_title="Wind Speed", calm_wind=0, variable_wind=990,
    #      n_col=1, ...)
    return None
