import os
import imp

import loaderpluginmanager

#Manage plugins in a single directory
class filterpluginmanager:

  def __init__(self, plugin_dir):
    self.plugin_dir = plugin_dir
    self.instances = []
    self.modules = {}

  # Get a list of the currently available plugins
  def get_available (self):

    #search for *.py in plugins directory
    files = os.listdir(self.plugin_dir)
    plugins = [f[:-3] for f in files if f.endswith(".py") ]
    return plugins

  def init (self, name, args):

    pmodule = '%s/%s.py'%(self.plugin_dir, name)
    self.modules[name] = imp.load_source (name, pmodule)

    ## get the plugin class object from the module and create an instance
    self.instances.append (getattr (self.modules[name], "filterplugin") (args) )


  # Call the method_name method of the instance of the specified plugin 
  #def do (self, plugin_name, method_name, *args, **kwargs):
  #  #getattr (self.instances[plugin_name], method_name)(*args, **kwargs)
  #  getattr (self.instances[plugin_name], method_name)()

  def filterall (self, frame): #must use individual do to use args for now
    #for plugin_name in self.get_available():
    #  self.do(plugin_name, method_name, args, kwargs)
    for plugin in self.instances:
      frame = getattr (plugin, "filter") (frame) # Apply each filter in turn to the frame

    return frame 

todo='''
Test filter chaining...

'''

if __name__ == '__main__':
    
    filterpluginmgr = filterpluginmanager('/home/jlogan/quip_quality/filter/plugins/filter')
    loaderpluginmgr = loaderpluginmanager.loaderpluginmanager('/home/jlogan/quip_quality/filter/plugins/loader')


    available = filterpluginmgr.get_available()
    print "Available filter plugins: "
    print available
    # Initialize a range filter
    args = {}
    args['var']='AreaInPixels'
    args['lts']=10
    args['gts']=20
    filterpluginmgr.init ('rangefilter', args)

    available = loaderpluginmgr.get_available()
    print "Available loader plugins: "
    print available
    # Initialize all plugins
    for name in available:
      loaderpluginmgr.init (name)


    # Make a test dataframe
    frame = loaderpluginmgr.load ("csv_reader", "data/sample.csv")


    # Apply the filter
    frame = filterpluginmgr.filterall (frame)

    print "Results:"
    print frame
