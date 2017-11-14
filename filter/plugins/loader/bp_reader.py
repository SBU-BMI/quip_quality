import numpy as np
import pandas as pd

import adios as ad

class loaderplugin:

  def __init__(self):
    pass
    print "loaderplugin created"

  def init(self):
    pass
    print "BP reader initialized"

  def load (self, filename):
    print "Get a dataframe for ", filename
    
    f = ad.file(filename)
    f.read()
    return pd.DataFrame(f)


