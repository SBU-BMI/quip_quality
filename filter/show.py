import sys

import numpy as np
import pandas as pd

import msviewer


if __name__ == "__main__":

  # Read results from csv
  filename = sys.argv[1]
  results = pd.read_csv (filename)

  results.sort_values("AreaInPixels", ascending=False, inplace=True) 

  msviewer.start(results)
