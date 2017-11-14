import numpy as np
import pandas as pd

class loaderplugin:

  def __init__(self):
    pass
    print "loaderplugin created"

  def init(self):
    pass
    print "hello loader initialized"

  def load (self, filename):
    print "Get a dataframe for ", filename
    
    # Return a new empty dataframe
    return pd.DataFrame (np.random.randn (2, 2), columns=['Hello', 'World'])



