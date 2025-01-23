REVAnalyzer is an open source package for representativity analysis of binary images. It aims at representativity analysis for porosity, permeability, Euler density, pore-network characteristics, correlation functions and persistence diagrams. Both scalar and vector metrics can be considered. Using REVAnalyzer library, one can estimate determenistic and statistical representative elementary volumes (dREV and sREV) for these metrics. Stationarity analysis and comparison of different images using vector metrics are also possible.

=================================================================================

Installation
============
$pip install .

Prerequisites
=============
Python 3.x and Julia 1.x with packages StatsBase.jl, LinearAlgebra.jl, CorrelationFunctions.jl (version=0.11.0)
and EulerCharacteristic.jl should be installed.

Documentation
=============
To build the documentation read /docs/README.md

Authors
=======
Andrey S. Zubov, Digital Core group, MIPT.
