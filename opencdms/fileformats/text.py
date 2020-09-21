# =================================================================
#
# Authors: Ian Edwards
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

import pandas as pd
from pandas.errors import ParserError


def read_badc(filepath, *args, **kwargs):
    """Read a BADC comma-separated values (CSV) file into Pandas DataFrame

    This function is a wrapper around `pandas.read_csv` which
    adds support for BADC formatted CSV files.

    Args:
        filepath (str): The path of the CSV file
        badc (bool): Indicates whether the CSV file is BADC format

    Returns:
        DataFrame: A Pandas DataFrame containing the data

    Example BADC CSV file:
    ```
    Conventions, G, BADC-CSV
    title, G, Example data
    creator, G, OpenCDMS Project
    long_name, 1, column one name
    long_name, 2, column two name
    data
    col1, col2
    a1, b1
    a2, b2
    a3, b3
    end data

    ```

    """
    df = None
    # Changing the default engine to 'python' in order to avoid warning
    # from Pandas when using skipfooter (which is not implemented in C)
    kwargs.setdefault("engine", "python")

    # Seek to the first line that contains actual data, then
    # pass the remaining data for Pandas to read
    with open(filepath) as file_buffer:
        for line_data in file_buffer:
            if line_data.strip() == "data":
                # In addition to any data rows already being skipped,
                # also skip the final row which should contain "end data"
                skip_footer = kwargs.get("skip_footer", 0) + 1
                df = pd.read_csv(
                    file_buffer, *args, skipfooter=skip_footer, **kwargs)
            if df is not None:
                # Pandas.read_csv seeks to EOF even with skipfooter
                # Check the contents of the final line where "end data"
                eof = file_buffer.tell()
                # Depending on line endings, the final ten characters
                # should be like "end data\r\n" or "\nend data\n"
                file_buffer.seek(eof - len("end data") - 2)
                if file_buffer.readline().strip() != "end data":
                    raise ParserError(
                        'Invalid BADC file. Final line must be "end data"'
                    )
    if df is None:
        raise ParserError(
            'Invalid BADC file. Line prior to data section must be "data"'
        )
    return df
