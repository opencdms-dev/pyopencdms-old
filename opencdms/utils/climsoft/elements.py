import os

import pandas as pd

BASE_PATH = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

ELEMENT_LOOKUP_CSV_FILE_PATH = os.path.join(
    BASE_PATH,
    "static_tables/climsoft4/element_codes.csv"
)


def get_element_abbreviation_by_time_period(time_period: str):
    df = pd.read_csv(ELEMENT_LOOKUP_CSV_FILE_PATH)

    return list(
        df[
            df["time_period"] == time_period.lower()
        ]["abbreviation"].values
    )
