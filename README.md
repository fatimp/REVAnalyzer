REVAnalyzer - open source package for representativity analysis of binary images. 
Representativity for porosity, permeability, pore-network characteristics, correlation
functions and persistence diagrams can be analyzed, determenistic and statistical representative elementary volumes (dREV and sREV) can be estimated.


=================================================================================

Actual branch
=============
parallel

Installation
============
$git clone https://gce.digital-core.ru/gitlab-instance-4a5c00a2/rev-analyzer.git
$pip install .

Prerequisites
=============
Python 3.x and Julia 1.x with packages StatsBase.jl, CorrelationFunctions.jl (version=0.11.0)
and EulerCharacteristic.jl should be installed.


Plugins
=======
REVAnalyzer requires additional plugins for the complete functionality:


PNM characteristics generation
----------------------------------------------
PNM-extractor:
---------------------
In gitlab: https://gce.digital-core.ru/gitlab-instance-4a5c00a2/pore-network-extraction, branch develop. Author - Dmitry Murygin.

###install & build:###
---------------------
see here: https://gce.digital-core.ru/gitlab-instance-4a5c00a2/pore-network-extraction/-/blob/develop/README.md
Executable file: ./bin/extractor_example 

PD generation
---------------------

PD-generator: 
----------------------
In gitlab: https://gce.digital-core.ru/gitlab-instance-4a5c00a2/pore-network-extraction, branch ppairs_new. Author - Andrey Zubov
Built module in dcore-gpu (10.4.128.112):

###install & build:###
---------------------
see here: https://gce.digital-core.ru/gitlab-instance-4a5c00a2/pore-network-extraction/-/blob/develop/README.md
Executable file: ./bin/persistence_pairs 

Documentation
=============
To see the documentation open /docs/html/index.html
To build the documentation read /docs/README.md

Authors
=======
Andrey Zubov, Digital Core group
