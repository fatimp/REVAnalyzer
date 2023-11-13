from julia.api import Julia
jl = Julia(compiled_modules=False)

from revanalyzer import REVAnalyzer
from revanalyzer.metrics import S2, L2, C2, SS2
from revanalyzer.vectorizers import CFVectorizer

norm = 2
mode = 'all' 
vectorizer = CFVectorizer(norm, mode) #vectorizer inizialization

normalize = True 
metric = SS2(vectorizer, normalize) #metric inizialization

#here insert your dirs and images: 
datadir = 'data'
outputdir = 'output'
image1 = 'ceramic300'
image2 = 'carb300'

#third argument is image size
metric.generate(datadir, image1, 300, outputdir)
metric.generate(datadir, image2, 300, outputdir)

v1 = metric.read(outputdir, image1, 0, 0)
v2 = metric.read(outputdir, image2, 0, 0)

#if metric is scalar type, v1 and v2 are scalars, and your result=2(|v1-v2|)/(v1+v2)

#if metric is vector type, you need the following:
output = metric.vectorize(v1, v2)
result = output[2]
print("Distance between images in SS2 metric: ", result)

