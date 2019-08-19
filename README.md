# PrettyConfig
This library helps you to keep configuration and hyper-parameters pretty! Make your configuration as a neat hierarchical struct. Utilize PrettyConfig for hyper-parameter searching in addition to the ability of saving, and loading configuration from file.

Installation
------------

Latest PyPI stable release
~~~~~~~~~~~~~~~~~~~~~~~~~~
pip install --user PrettyConfig
~~~~~~~~~~~~~~~~~~~~~~~~~~

Basic Usage
------------
Define and Print:
```python
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
```
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

Save:
```python
    config_obj.save(saving path)
```

Load:
```python
    loaded_config_obj = Configuration(path)
```

Hyper-parameter Searching 
------------
Type of searchable hyper-parameters is ``ChoiceList``. When declaring a list of variable as ``ChoiceList``, you can make all possible config. In this way, you can use single for instead of nested for!
```python
from PrettyConfig import HyperParameters, ChoiceList, get_possible_hyper_parameters

class Configuration(HyperParameters):
    constval = 10
    param_a = ChoiceList([1,2])
    param_b = ChoiceList([3,4,5])

config_obj = Configuration()
configs = get_possible_hyper_parameters(config_obj)
for config in configs:
    print(" ")
    print(config)
```
~~~~~~~~~~~~~~~~~~~~~~~~~~
├──> param_a:1
├──> param_b:3
└──> constval:10
 
├──> param_a:2
├──> param_b:3
└──> constval:10
 
├──> param_a:1
├──> param_b:4
└──> constval:10
 
├──> param_a:2
├──> param_b:4
└──> constval:10
 
├──> param_a:1
├──> param_b:5
└──> constval:10
 
├──> param_a:2
├──> param_b:5
└──> constval:10
~~~~~~~~~~~~~~~~~~~~~~~~~~

