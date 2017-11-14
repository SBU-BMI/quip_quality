

class filterplugin:
  def __init__(self):
    pass
    print "plugin class instance created"

  def init(self):
    print "Hello World init()"

  def filter(self, frame):
    print "Hello World filter()"

  def finalize(self):
    print "Hello World finalize()"
