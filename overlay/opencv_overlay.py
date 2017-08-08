import numpy as np
import cv2
import sys,os
from subprocess import call

segfile=sys.argv[1]
svsfile=sys.argv[2]

fname=os.path.splitext(segfile)[0]
tilefile=fname+'-tile.png'
overfile=fname+'-overlay.jpg'

im = cv2.imread(segfile)
height, width, channels = im.shape

w=str(width)
h=str(height)

call(['bash', 'run_overlay.sh', segfile, svsfile, w, h, tilefile])

tileim = cv2.imread(tilefile)

imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(imgray,127,255,0)

image, contours, hierarchy = cv2.findContours(imgray,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

img = cv2.drawContours(tileim, contours, -1, (0,255,0), 3)

cv2.imwrite(overfile,img)
