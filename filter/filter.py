import os
from sklearn import datasets
from sklearn.cluster import KMeans
import sklearn.metrics as sm
import sklearn.preprocessing as pre

import numpy as np
import pandas as pd
import os
import string

import matplotlib as mpl
import matplotlib.pyplot as plt

from tqdm import tqdm
import math
import msviewer

#Show the available images

svsroot = '/data/shared/jlogan/seer-images'
#hard_coded = "17032556.svs"
#hcf = "%s/%s"%(imgroot, hard_coded)

#rootdir = "/data10/shared/jlogan/wensi20170523/luad"
rootdir = "/data/shared/tcga_analysis/seer_data/results"
allfiles = os.listdir(rootdir)
imgdirs = [f for f in allfiles if not f.endswith(".svs") ]
#for i in  zip (range(len(imgdirs)), imgdirs): #sh w image names with indices
#  print i


#Get a list of all of the csv files across all images, picking the first set of results for each
allcsv = []
print "Scanning csv files"
for imgdir in tqdm(imgdirs):
    imgroot = "%s/%s"%(rootdir,imgdir)
    first_seg = "%s/%s"%(imgroot,os.listdir(imgroot)[0])
    #allcsv = os.listdir(first_seg)
    csvfiles = ["%s/%s"%(first_seg,f) for f in os.listdir(first_seg) if f.endswith("features.csv")]
    allcsv.extend (csvfiles)
allcsv


#Perform a query by loading all data frames and filtering desired results
million = 1000000
out_freq = 10000
results = pd.DataFrame()
print "Filtering objects"
for id in tqdm(range(len(allcsv))):
    if id%out_freq==0:
        # Write results to output file
        results.to_csv ("results.csv")

    csvfile = allcsv[id]
    svsfile = "%s/%s.svs"%(svsroot,string.split(csvfile, '/')[6]) #Pull out the image name and construct the path to the svs file
    #print "svsfile is " + svsfile
    df = pd.read_csv(csvfile, index_col=None, header=0)
    r = df.loc[df['AreaInPixels'] > 5*million/100] # 50k

    if r.empty:
      continue

# Add a column for filename
    r.loc[:,"fname"] = svsfile
    #r["fname"] = csvfile [:-12] + "seg.png"  # Remove features.csv and add seg.png to get image path NOPE, that's the mask
    
    if results.empty:
        results = r
    else:
        results = pd.concat ([results, r], ignore_index=True)
    #print "Frame has %i results" % len(r.index)
    #if results

#print results

# Write results to output file
results.to_csv ("results.csv")

#msviewer.start(results)
