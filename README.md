REVAnalyzer - open source package for representativity analysis of binary images. 
Representativity for porosity, permeability, pore-network characteristics, correlation
functions and persistence diagrams can be studied, determenistic and statistical
representative elementary volumes (dREV and sREV) can be estimated.
=================================================================================

Installation
============
$git clone http://
$cd REVAnalyzer/
$pip install .

Prerequisites
=============
Python 3.x and Julia 1.x with packages StatsBase.jl, CorrelationFunctions.jl
and EulerCharacteristic.jl should be installed.

Installation of package Package.jl in Julia:
-------------------------------------------
$julia
julia> using Pkg
julia> Pkg.add("Package")

julia> exit()


Plugins
=======
REVAnalyzer requires additional plugins for the complete functionality:

Permeability generation
-----------------------
FDMSS:
In gitlab:
Built module in dcore-gpu (10.4.128.112): /home/azubov/fdmss/

PNM-extractor:
In gitlab: https://gce.digital-core.ru/gitlab-instance-4a5c00a2/pore-network-extraction, branch develop. Author - Dmitry Murygin.
install & build:
----------------
$git clone https://gce.digital-core.ru/gitlab-instance-4a5c00a2/pore-network-extraction.git
$cd pore-network-extraction/
$git checkout --track origin/develop
$cmake -B ./build -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=Release
$cd build/
$make -j

Built module in dcore-gpu (10.4.128.112):  (10.4.128.112): /home/azubov/pnm_extractor/pore-network-extraction/build/bin/extractor_example

MEF: 
In gitlab: https://gce.digital-core.ru/gitlab-instance-4a5c00a2/fluid-transport-in-pore-networks/-/tree/master, branch refactoring-4
install & build:
----------------
$git clone https://gce.digital-core.ru/gitlab-instance-4a5c00a2/fluid-transport-in-pore-networks.git
$cd fluid-transport-in-pore-networks/
$git checkout --track origin/refactoring-4
$cmake -B ./build -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=Release
$cd build/
$make -j

Built module in dcore-gpu (10.4.128.112): '/home/azubov/mef/fluid-transport-in-pore-networks/build/bin/flow_simulator_example'

PNM characteristics:
--------------------
PNM-extractor:
In gitlab: https://gce.digital-core.ru/gitlab-instance-4a5c00a2/pore-network-extraction, branch develop. Author - Dmitry Murygin.
install & build:
----------------
$git clone https://gce.digital-core.ru/gitlab-instance-4a5c00a2/pore-network-extraction.git
$cd pore-network-extraction/
$git checkout --track origin/develop
$cmake -B ./build -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=Release
$cd build/
$make -j
 
Built module in dcore-gpu (10.4.128.112):  (10.4.128.112): /home/azubov/pnm_extractor/pore-network-extraction/build/bin/extractor_example

PD-genearator: 
(requires C++17!)
In gitlab: https://gce.digital-core.ru/gitlab-instance-4a5c00a2/pore-network-extraction, branch ppairs_new. Author - Andrey Zubov
install & build:
----------------
$git clone https://gce.digital-core.ru/gitlab-instance-4a5c00a2/pore-network-extraction.git
$cd pore-network-extraction/
$git checkout --track origin/develop
$cmake -B ./build -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=Release
$cd build/
$make -j

Built module in dcore-gpu (10.4.128.112): None. No C++17 at dcore. 

Authors
=======
Andrey Zubov, Joint Institute for Nuclear Research, Dubna, Russia.
