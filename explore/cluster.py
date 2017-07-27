########
# Exploratory clustering of segmentation results
# Use $> python cluster.py to execute
# Loads specified features of all objects in an image and performs clustering

from sklearn import datasets
from sklearn.cluster import KMeans
import sklearn.metrics as sm

import numpy as np
import pandas as pd
import os
import matplotlib as mpl
#import csv

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
    #Let's use pandas instead of python to read csv...
    #with open(f) as featurefile:
        #csv.field_size_limit(2000000) # Large number to accomodate results with VERY large polygon descriptors
        #reader = csv.DictReader(featurefile)
    df = pd.read_csv(f, index_col=None, header=0, usecols=range(92))
    #df = pd.read_csv(f, index_col=None, header=0, usecols=[0,1,2,3])
    #df = pd.read_csv(f, index_col=None, header=0)
    flist.append(df)
frame = pd.concat(flist)

print "Loaded dataframe containing %i features:"%len(list(frame))
print list(frame)

# Let's try k-means with
model = KMeans (n_clusters=6)
model.fit (frame)

print model.labels_

# Make a scatter plot
# Can't do X forwarding on eagle?
mpl.use('pdf')
cm = np.array(['red','blue','green','orange','yellow','violet'])
import matplotlib.pyplot as plt
df.plot(kind='scatter', x='PhysicalSize', y='b_IntensityStd', c=cm[model.labels_])
plt.savefig('scatter.pdf')






