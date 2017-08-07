########
# Extracts polygons associated with clumps from csv version of feature/polygon file.
# This extracts polygons and polygon areas,  employs Python Shapely library's simplify
# method to replace sets of adjacent almost co-linear lines with single lines. 
# The function Create_clump_summaries invokes the simplify function
# on each polygon and sorts polygons by the longest vertex in each simplified polygon. 
# This script also allows users to view polygons by rank in list sorted by longest
# simplified edge.  The polygons are translated to a standard coordinate system

import os
import csv
from matplotlib import pyplot
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import shapely
from shapely.geometry.polygon import Polygon



#input_file = csv.DictReader(open("features.csv"))


#for row in input_file:
#   print(row)
#input_file.close()
def Create_clump_summaries(feature_file,simplify_threshold):
    
    """ Employs Panda Shapely library to simplify polygons by eliminating almost
    colinear vertices.  Generates two data structures: First - sort_clump_df:  Panda Dataframe
    containing the longest line in the simplified and unsimplified polygon, polygon area, 
    polygon number by order listed in feature_file.  The Dataframe is sorted by
    length of longest edge of simplified polygon. Second - polygon_dict which
    is a dictionary with numpy arrays representing normalized polygons """
    
    i= 0
    clump_dict = {'clump':[],'area':[], 'max_line':[], 'max_line_simplify':[]}
    polygon_dict ={}
    
    with open(feature_file) as input_file2:
        reader = csv.DictReader(input_file2)
        for row1 in reader:         
           
            row1_polygon = row1['Polygon']
            row1_polygon = row1_polygon[1:len(row1_polygon)-1]
            row1_polygon_list = row1_polygon.split(':')
            row1_polygon_list = [float(x) for x in row1_polygon_list]
            even_pts = row1_polygon_list[0:len(row1_polygon_list)-1:2]
            odd_pts = row1_polygon_list[1:len(row1_polygon_list):2]
            row1_tuples = list(zip(even_pts,odd_pts))
# clump represents the polygon representing each clump
            clump = Polygon(row1_tuples)
# Invoke Shapely to generate simplified polygon
            clump2 = clump.simplify(simplify_threshold)
# Obtain points defining polygon, compute length of edges
            npclump = np.array(clump.exterior)
            npclump_shift = np.roll(npclump,1,axis=0)
            diff_clump = npclump_shift - npclump
            l2_clump = np.sqrt(((diff_clump**2).sum(axis=1)))
            max_l2_clump = l2_clump.max()
            
            npclump2 = np.array(clump2.exterior)
            npclump2_shift = np.roll(npclump2,1,axis=0)
            diff_clump2 = npclump2_shift - npclump2
            l2_clump2 = np.sqrt(((diff_clump2**2).sum(axis=1)))
            max_l2_clump2 = l2_clump2.max()
            clump_dict['clump'].append(i)
            clump_dict['max_line'].append(max_l2_clump)
            clump_dict['area'].append(clump.area)
            clump_dict['max_line_simplify'].append(max_l2_clump2)
# shift x and y polygon axis 
            polygon_dict[i] = npclump2 - npclump2.min(axis=0)
            print('\n number', i, '\n area',clump.area, 'clump max line',max_l2_clump, 'simplified clump max line', max_l2_clump2)
            i +=1
        num_clumps = i-1
        clump_df = pd.DataFrame(clump_dict)
        sort_clump_df = clump_df.sort_values(by='max_line_simplify',ascending = False)
        sort_clump_df.reset_index(inplace=True)
    return sort_clump_df,polygon_dict, num_clumps

     
sort_clump_df, polygon_dict, num_clumps =    Create_clump_summaries('features.csv',0.2)  #%%






#%%


# Input list of clumps ordered by lenght of longest simplified polygon edge
print('\n Input list of clumps between 0 and ',num_clumps-1)
print_clumps_txt = input(' ')
print_clumps_split = print_clumps_txt.split()
print_clumps = [int(ii) for ii in print_clumps_split]



for jj in range(len(print_clumps)):
    plt.figure(jj+1)
    ii = print_clumps[jj]


# Print polygons - user is prompted for which rank ordered polygons/clumps to inspect
    sorted_clump = sort_clump_df.loc[ii,'clump']
    title_text = ('rank ' + str(ii) + ' clump ' + str(sort_clump_df.loc[ii,'clump']) + ' area ' + str(sort_clump_df.loc[ii,'area']) + ' max line ' 
                  + str(sort_clump_df.loc[ii,'max_line_simplify']))
    plt.title(title_text)
    
    plt.plot(polygon_dict[sorted_clump][:,0],polygon_dict[sorted_clump][:,1])
    
#%%
# Close out figures
close_figure = input('c to close figures ')
if close_figure == 'c':
    for jj in range(len(print_clumps)-1):
        plt.close(jj+1)
#        print(clump)


#    plt.figure(2)
#ax = plt.axes()

#for ii in range(len(clump_no)):
    
#    plt.plot(polygon_dict[44][:,0],polygon_dict[44][:,1])
#print('\n area',clump.area, ' max line',max_l2_clump, 'simplified c max line', max_l2_clump2)

#from shapely.geometry import Point
#patch = Point(0.0, 0.0).buffer(10.0)



    
#line = LineString([(0, 0), (2, 2)])
# create a point which lies along the line
#point = line.interpolate(1)
#line.contains(point)

#def pairs(lst):
#    for i in range(1, len(lst)):
#npc        yield lst[i-1], lst[i]

#line = LineString([(0,0),(1,2), (2, 2), (2,3), (4,2),(5,5)])

#for pair in pairs(list(line.coords)):
#    if LineString([pair[0],pair[1]]).contains(point): 
#        print(LineString([pair[0],pair[1]]))

        
        

#csv.field_size_limit(2000000) # Large number to accomodate results with VERY large polygon descriptors
#featurefile = 'features.csv'
#reader = csv.DictReader(featurefile)

# row in reader:
#   obj_count = obj_count + 1
#    this_area = row['AreaInPixels'] # convert to float first to handle scientific notation
#    total_area = total_area + this_area
#    pct_area = 100*total_area/float(tile_area)
#    print('pct_area',pct_area)
#max_pct_area = 100*max_area/float(tile_area)
#print('pct_area',pct_area,'max_pct_area',max_pct_area)
#
   





