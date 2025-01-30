from datetime import datetime

CURRENT_DATE = datetime.now()
EARLIEST_SEASON = 2019

AVAILABLE_SEASONS = [
    [str(year) for year in range(EARLIEST_SEASON, CURRENT_DATE.year+1)],
    (
        [f"{year}-{year+1}" for year in range(2019, CURRENT_DATE.year) if CURRENT_DATE.month < 7] +
        [f"{year}-{year+1}" for year in range(2019, CURRENT_DATE.year + 1) if CURRENT_DATE.month >= 7]
    )
]

CURRENT_SEASON = [
    AVAILABLE_SEASONS[0][-1],
    AVAILABLE_SEASONS[1][-1]
]
