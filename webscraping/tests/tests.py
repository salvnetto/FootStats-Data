import pytest
import pandas as pd

import webscraping as ws


def testLoadDataInvalidRegion():
    with pytest.raises(ValueError):
        ws.standings('invalid_region')


