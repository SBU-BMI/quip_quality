import os
import imp

import numpy as np
import pandas as pd

#Manage plugins in a single directory
class loaderpluginmanager:

  def __init__(self, plugin_dir):
    self.plugin_dir = plugin_dir
    self.instances = {}
    self.modules = {}

  # Get a list of the currently available plugins
  def get_available (self):

    #search for *.py in plugins directory
    files = os.listdir(self.plugin_dir)
    plugins = [f[:-3] for f in files if f.endswith(".py") ]
    return plugins

  def init (self, name):

    pmodule = '%s/%s.py'%(self.plugin_dir, name)
    self.modules[name] = imp.load_source (name, pmodule)

    ## get the plugin class object from the module and create an instance
    self.instances[name] = getattr (self.modules[name], "loaderplugin")()




  # Call the method_name method of the instance of the specified plugin 
  def load (self, plugin_name, filename, *args, **kwargs):
    #getattr (self.instances[plugin_name], method_name)(*args, **kwargs)
    return getattr (self.instances[plugin_name], "load")(filename)



if __name__ == '__main__':
    
    loaderpluginmanager = loaderpluginmanager('/home/jlogan/quip_quality/filter/plugins/loader')


    available = loaderpluginmanager.get_available()
    print "Available plugins: "
    print available

    
    # Initialize all plugins
    for name in available:
      loaderpluginmanager.init (name)

    # Make a test dataframe

    #frame = loaderpluginmanager.load ("csv_reader", "/data/shared/tcga_analysis/seer_data/results/17032547/0000b7e0-b163-4021-ad32-ee902933f941/17032547.17032547.1001272994_mpp_0.251_x63488_y14336-features.csv")
    print "loading empty csv frame..."
    frame = loaderpluginmanager.load ("csv_reader", "data/emptyframe.csv")

    print "loading sample csv frame..."
    frame = loaderpluginmanager.load ("csv_reader", "data/sample.csv")

    #print "loading sample bp frame..."
    #frame = loaderpluginmanager.load ("bp_reader", "data/sample.bp")

    print frame

