########
# Initial exploration of feature results from segmentation runs
# Use $> python peek.py to execute
# Iterates over all tiles in one image, and filters out tiles that
# meet a specified condition
# Expects rootdir to contain subdirectories corresponding to individual images, 
# and that each subdirectory contains feature results in per-tile csv files named *features.csv

import os
import csv

tile_size = 4096
tile_area = tile_size * tile_size

rootdir = "/data/shared/jlogan/wensi20170523/luad"

allfiles = os.listdir(rootdir)
imgdirs = [f for f in allfiles if not f.endswith(".svs") ]

print "Images:"
print imgdirs

########
## Select a single image to examine its features 
## Use this to select an image by indexing the directory
#imgroot = "%s/%s"%(rootdir,imgdirs[7])

## OR, use this to select an image by name
#imgroot = "%s/%s"%(rootdir,"TCGA-J2-8194-01Z-00-DX1.7700924D-B6AF-46A7-A7D7-B5C17A66C5F7")
imgroot = "%s/%s"%(rootdir,"TCGA-62-A46S-01Z-00-DX1.7A8A6F38-76EA-4F43-BC03-1C42E6787E33")


allimgdata = os.listdir(imgroot)
csvfiles = [f for f in allimgdata if f.endswith("features.csv")]

for f in csvfiles:
    obj_count = 0
    max_area = 0
    line_no = 0
    total_area = 0
    max_blueStd = 0
    with open("%s/%s"%(imgroot,f) ) as featurefile:
        csv.field_size_limit(2000000) # Large number to accomodate results with VERY large polygon descriptors
        reader = csv.DictReader(featurefile)

        for row in reader:
            obj_count = obj_count + 1
            this_area = int(float(row['AreaInPixels'])) # convert to float first to handle scientific notation
            this_blueStd = float(row['StdB']) # convert to float first to handle scientific notation
            if this_area > max_area:
                max_area = this_area
            if this_blueStd > max_blueStd and this_area > 20000:
                max_blueStd = this_blueStd
            total_area = total_area + this_area

    pct_area = 100*total_area/float(tile_area)
    max_pct_area = 100*max_area/float(tile_area)

    # Extract URL components from filename
    # x pos is between '_x' and '_y', y pos is between '_y' and '-'

    img_end = f.find ('.', f.find('.')+1) #Ends at the second '.'
    img_id = f[0:img_end]
    xp = f.find('_x')
    yp = f.find('_y')
    zp = f.find('-', yp)
    x = f[xp+2:yp]
    y = f[yp+2:zp]
    url = "http://129.49.249.167/camicroscope/osdCamicroscope.php?tissueId=%s&x=%s&y=%s&zoom=20" % (img_id, x, y)

    if obj_count > 0:

        #if max_blueStd > 0:
        #    print "blueStd is %s"%max_blueStd

########
# Adjust filtering condition and output here:
        #if (max_pct_area>10 or max_pct_area < 0.5) and pct_area>20.0:
        if (max_pct_area>2 and max_pct_area<3):
            #print "***"
            print "Processing tile", f
            print url
            print "Tile has %s objects"%obj_count
            print "Maximum object area is %s"%max_area
            print "Maximum object area percentage is %s"%max_pct_area
            print "Total object area is %s"%total_area
            print "Percent object coverage area is %s%%"%pct_area
   



