# -*- coding: utf-8 -*-

# Learn more: 

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()
    
# Read in package requirements.txt
requirements = open('requirements.txt').readlines()
requirements = [r.strip() for r in requirements]

setup(
    name='revanalyzer',
    version='0.1.1',
    description='Package for representativity analysis of 3D binary images',
    long_description=readme,
    author='Andrey Zubov',
    author_email='zubov.an.se@gmail.com',
    url='https://github.com/fatimp/REVAnalyzer',
    license=license,
    install_requires=requirements,
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True
)

