####################
Creating new plugins
####################

The plugin mechanism is designed for adding new functionality to the filtering
pipeline without requiring any changes to the pipeline itself. A developer need
only create a python module that implements required functions, and drop it in
the correct directory. From there, the curation tool is capable of locating 
available plugins, presenting them to the user, and incorporating the functionality
from any user selected plugins into pipeline execution.


