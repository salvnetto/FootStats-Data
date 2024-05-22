# GOALS-Data

## Overview

The `GOALS-Data` repository is an auxiliary data source for the `GOALS` package. It contains raw and processed football data for various leagues and competitions. This repository is intended to provide users with easy access to high-quality football data for analysis and research purposes. The data in this repository is collected using a web scraper that extracts football statistics from [fbref.com](https://fbref.com). More info: <https://github.com/salvnetto/GOALS>

## Features

- Raw and processed data for multiple football leagues:
  - English Premier League
  - Brasileirão
  - Ligue 1
  - Serie A
  - La Liga
  - Bundesliga
- Data includes match history, league standings, and team squads.

## Usage

To use the data from the `GOALS-Data` repository, you can leverage the `loadData` function from the `GOALS` package.

### Example: Load Data with GOALS Package

```python
from goals import loadData

# Load processed match history data for Brasileirão
df = loadData('br', 'match_history')
print(df.head())

# Load raw standings data for the Premier League
df = loadData('en', 'standings', raw=True)
print(df.head())
```