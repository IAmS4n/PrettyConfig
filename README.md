# PrettyConfig
This library helps you to keep configuration and hyper-parameters pretty! Make your configuration as a neat hierarchical struct. Utilize PrettyConfig for hyper-parameter searching in addition to the ability of saving, and loading configuration from file.

Installation
------------

Latest PyPI stable release
~~~~~~~~~~~~~~~~~~~~~~~~~~
pip install --user PrettyConfig
~~~~~~~~~~~~~~~~~~~~~~~~~~

Usage
------------
Define and print
~~~~~~~~~~~~~~~~~~~~~~~~~~
from PrettyConfig import HyperParameters

class Configuration(HyperParameters):
    modelname = "Example"
    class modules(HyperParameters):
        names = ["m1", "m2"]
        path = "/tmp/c"
    class saving(HyperParameters): 
        class log(HyperParameters):
            path = "/tmp/a/"
            max_size = 100
        class data(HyperParameters):
            path = "/tmp/b/"
            max_size = 200

config_obj = Configuration()
print(config_obj)
~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~
├──> modelname:Example
├──saving
│  ├──data
│  │  ├──> max_size:200
│  │  └──> path:/tmp/b/
│  └──log
│     ├──> max_size:100
│     └──> path:/tmp/a/
└──modules
   ├──> names:['m1', 'm2']
   └──> path:/tmp/c
~~~~~~~~~~~~~~~~~~~~~~~~~~
Save
~~~~~~~~~~~~~~~~~~~~~~~~~~
config_obj.save(saving path)
~~~~~~~~~~~~~~~~~~~~~~~~~~
Load
~~~~~~~~~~~~~~~~~~~~~~~~~~
loaded_config_obj = Configuration(path)
~~~~~~~~~~~~~~~~~~~~~~~~~~
