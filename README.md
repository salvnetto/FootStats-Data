# DYNMO - Dynamic Linear Models for Football

## Overview

The `DYNMO` package facilitates game outcome analysis using statistical learning techniques. It is designed for modeling and predicting football match results based on various statistical features.

## Features

- Web scraping techniques to gather football data.
- Preprocessing functions for cleaning and transforming data.

## Usage

To use the `DYNMO` package, install it via pip:

```
pip install DYNMO
```

### Example: Loading Data

```python
from DYNMO import loadData

# Load processed match history data for Brasileirão
df = loadData('br', 'match_history')
print(df.head())
```