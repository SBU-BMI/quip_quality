import sys

import numpy as np
import pandas as pd


class filterplugin:
  def __init__(self, args):
    self.args = args
    print "plugin class instance created"

  def init(self):
    print "rangefilter init()"

  def filter(self, frame):
    print "rangefilter filter(", self.args, ")"

    if self.args['lts'] == '*' and self.args['gts'] == '*':
      return frame

    if self.args['lts'] == '*':
      return frame.loc[frame[self.args['var']] > self.args['gts']] 

    if self.args['gts'] == '*':
      return frame.loc[frame[self.args['var']] < self.args['lts']]

    sys.exit ("TODO: implement closed range filter...")
    

  def finalize(self):
    print "rangefilter finalize()"
