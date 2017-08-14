########
# Show histogram for each feature
# Use $> python histo.py to execute
# Loads specified features of all objects in an image and displays histograms

import numpy as np
import pandas as pd
import os

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

#Use interactive mode
plt.ion()
#import csv

import matplotlib.image as mpimg
import string

rootdir = "/data/shared/jlogan/wensi20170523/luad"

allfiles = os.listdir(rootdir)
imgdirs = [f for f in allfiles if not f.endswith(".svs") ]
#print "Images:"
#print imgdirs

########
## Select a single image to examine its features 
## Use this to select an image by indexing the directory
#imgroot = "%s/%s"%(rootdir,imgdirs[7])

## OR, use this to select an image by name
#imgroot = "%s/%s"%(rootdir,"TCGA-J2-8194-01Z-00-DX1.7700924D-B6AF-46A7-A7D7-B5C17A66C5F7")
imgroot = "%s/%s"%(rootdir,"TCGA-62-A46S-01Z-00-DX1.7A8A6F38-76EA-4F43-BC03-1C42E6787E33")

#print "imgroot is ", imgroot

allimgdata = os.listdir(imgroot)
csvfiles = ["%s/%s"%(imgroot,f) for f in allimgdata if f.endswith("features.csv")]

frame = pd.DataFrame()
flist = []

for f in csvfiles:
    #with open(f) as featurefile:
        #csv.field_size_limit(2000000) # Large number to accomodate results with VERY large polygon descriptors
        #reader = csv.DictReader(featurefile)


    #Let's use pandas instead of python to read csv...
    df = pd.read_csv(f, index_col=None, header=0, usecols=range(93))
    #df = pd.read_csv(f, index_col=None, header=0, usecols=[0,1,2,3])
    #df = pd.read_csv(f, index_col=None, header=0)
    df['file'] = f
    flist.append(df)
frame = pd.concat(flist, ignore_index=True)

print "Loaded dataframe containing %i features:"%len(list(frame))
print list(frame)

with PdfPages('pdf/histograms.pdf') as pdf:

  plt.subplots_adjust(wspace=5,hspace=5)

  max = 91
  per_page = 6
  for i in range (0, max, per_page):
    if i+per_page < 91:
      frame.iloc[:,i:i+per_page].hist()
    else:
      frame.iloc[:,i:i+max].hist()
    pdf.savefig(orientation='portrait')

  plt.close()
