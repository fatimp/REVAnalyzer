REVAnalyzer - open source package for representativity analysis of binary images. 
Representativity for porosity, permeability, pore-network characteristics, correlation
functions and persistence diagrams can be analyzed, determenistic and statistical representative elementary volumes (dREV and sREV) can be estimated.


=================================================================================

Actual branch
=============
develop

Installation
============
$git clone https://gce.digital-core.ru/gitlab-instance-4a5c00a2/rev-analyzer.git
$pip install .

Prerequisites
=============
Python 3.x and Julia 1.x with packages StatsBase.jl, CorrelationFunctions.jl
and EulerCharacteristic.jl should be installed.

Installation of package Package.jl in Julia:
------------------------------------------------------------
$julia
julia> using Pkg
julia> Pkg.add("Package")

julia> exit()


Plugins
=======
REVAnalyzer requires additional plugins for the complete functionality:

Permeability generation
-----------------------------------

FDMSS:
------------
In gitlab: https://gce.digital-core.ru/gitlab-instance-4a5c00a2/fdmss.git Questions how it works to Andrey Zubov, Valiliy Postnikov or Kirill Gerke.
Built module in dcore-gpu (10.4.128.112): /home/azubov/fdmss/

install & build:
-------------------
$git clone https://gce.digital-core.ru/gitlab-instance-4a5c00a2/fdmss.git
$cmake .
$make


PNM-extractor:
---------------------
In gitlab: https://gce.digital-core.ru/gitlab-instance-4a5c00a2/pore-network-extraction, branch develop. Author - Dmitry Murygin.
Built module in dcore-gpu (10.4.128.112):  /home/azubov/pnm_extractor/pore-network-extraction/build/bin/extractor_example

install & build:
-------------------
$git clone https://gce.digital-core.ru/gitlab-instance-4a5c00a2/pore-network-extraction.git
$cd pore-network-extraction/
$git checkout --track origin/develop
$cmake -B ./build -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=Release
$cd build/
$make -j


MEF: 
-------
In gitlab: https://gce.digital-core.ru/gitlab-instance-4a5c00a2/fluid-transport-in-pore-networks/, branch refactoring-4. Author - Dmitry Murygin.
Built module in dcore-gpu (10.4.128.112): '/home/azubov/mef/fluid-transport-in-pore-networks/build/bin/flow_simulator_example'

install & build:
---------------------
$git clone https://gce.digital-core.ru/gitlab-instance-4a5c00a2/fluid-transport-in-pore-networks.git
$cd fluid-transport-in-pore-networks/
$git checkout --track origin/refactoring-4
$cmake -B ./build -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=Release
$cd build/
$make -j

PNM characteristics generation
----------------------------------------------
PNM-extractor:
---------------------
In gitlab: https://gce.digital-core.ru/gitlab-instance-4a5c00a2/pore-network-extraction, branch develop. Author - Dmitry Murygin.
Built module in dcore-gpu (10.4.128.112):  (10.4.128.112): /home/azubov/pnm_extractor/pore-network-extraction/build/bin/extractor_example

###install & build:###
---------------------
$git clone https://gce.digital-core.ru/gitlab-instance-4a5c00a2/pore-network-extraction.git
$cd pore-network-extraction/
$git checkout --track origin/develop
$cmake -B ./build -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=Release
$cd build/
$make -j
 

PD generation
---------------------

PD-generator: 
----------------------
(requires C++17!)
In gitlab: https://gce.digital-core.ru/gitlab-instance-4a5c00a2/pore-network-extraction, branch ppairs_new. Author - Andrey Zubov
Built module in dcore-gpu (10.4.128.112):

###install & build:###
---------------------
$git clone https://gce.digital-core.ru/gitlab-instance-4a5c00a2/pore-network-extraction.git
$cd pore-network-extraction/
$git checkout --track origin/ppairs_new
$cmake -B ./build -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=Release
$cd build/
$make -j

Documentation
=============
To see the documentation open /docs/html/index.html
To build the documentation read /docs/README.md

Authors
=======
Andrey Zubov, Digital Core group, Moscow and Joint Institute for Nuclear Research, Dubna, Russia.
