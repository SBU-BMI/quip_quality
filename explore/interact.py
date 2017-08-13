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
import matplotlib.pyplot as plt
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

tolerance = 5
fig = plt.figure()
ax = fig.add_subplot(121)

#Plot the entire image
plotframe = frame
#    -- OR --
#Select a tile by index
#plotframe = flist[10]

plotframe.plot(ax=ax, kind='scatter', x='PhysicalSize', y='Circularity', picker=tolerance)

def getxy(f):
  xp = f.find('_x')
  yp = f.find('_y')
  zp = f.find('-', yp)
  x = float(f[xp+2:yp])
  y = float(f[yp+2:zp])
  return (int(x),int(y))

def onpick(event):
    the_file = plotframe['file'][event.ind].values[0]
    print ":::", 
    the_file = string.replace(the_file,"features.csv","seg-overlay.png")
    #the_file = string.replace(the_file,"features.csv","seg.png")
    im = mpimg.imread(the_file)

    poly_pts = plotframe['Polygon'][event.ind].values[0][1:-1].split(':') # the [1:-1] is to strip the [ and ] from the ends of the string
    # Need min and max of evens, and min and max of odds, then subtract
    # the tile offsets from the filename
    evens = range(0, len(poly_pts), 2)
    odds = range(1, len(poly_pts), 2)

    minx = 1000000000
    maxx = 0
    miny = 1000000000
    maxy = 0  
  
    for i in evens:
        me = int(float(poly_pts[i]))
        if me > maxx:
            maxx = me
        if me < minx:
            minx = me

    for i in odds:
        me = int(float(poly_pts[i]))
        if me > maxy:
            maxy = me
        if me < miny:
            miny = me

    print "found", minx, miny, maxx, maxy

    # Adjust to tile coordinates

#    tilex = 45056
#    tiley = 36864
    tilex, tiley = getxy(the_file)

    minx = minx - tilex
    miny = miny - tiley
    maxx = maxx - tilex
    maxy = maxy - tiley

    marginx = marginy = 0

    #cropped_im = im[minx:maxx, miny:maxy]    
    cropped_im = im[miny-marginy:maxy+marginy, minx-marginx:maxx+marginx]    

    fig.add_subplot(122)
    imgplot = plt.imshow(cropped_im)
    plt.draw()


cid = fig.canvas.callbacks.connect('pick_event', onpick)

plt.show(block=True)



