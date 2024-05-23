import os
import sys

import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from webscraping import Standings

def testLoadDataInvalidRegion():
    with pytest.raises(ValueError):
        Standings('invalid_region')


