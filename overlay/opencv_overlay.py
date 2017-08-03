import numpy as np
import cv2
import sys,os
from subprocess import call

inpfile=sys.argv[1]

fname=os.path.splitext(inpfile)[0]
tilefile=fname+'-tile.jpg'
overfile=fname+'-overlay.jpg'

im = cv2.imread(inpfile)
height, width, channels = im.shape

w=str(width)
h=str(height)

call(['bash', 'run_overlay.sh', inpfile, w, h, tilefile])

tileim = cv2.imread(tilefile)

imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(imgray,127,255,0)

image, contours, hierarchy = cv2.findContours(imgray,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

img = cv2.drawContours(tileim, contours, -1, (0,255,0), 3)

cv2.imwrite(overfile,img)
