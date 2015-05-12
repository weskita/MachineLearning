from math import log
from csvHelper import *
import numpy

#getShannonEnt(): parameter: dataSet, the last colume is mark vector; the other columes of this matrix are feature vectors.
def getShannonEnt(dataSet):
	numEntries = len(dataSet)
	labelCounts = {}
	for featVec in dataSet:
		currentLabel = featVec[-1]
		if currentLabel not in labelCounts.keys():
			labelCounts[currentLabel] = 0
		
		labelCounts[currentLabel] += 1
		
	shannonEnt = 0.0
	for key in labelCounts:
		prob = float(labelCounts[key]) / numEntries
		shannonEnt -= prob * log(prob,2)
		
	return shannonEnt

	
def splitDataSet(dataSet, axis, value):
	retDataSet = []
	for featVec in dataSet:
		if featVec[axis] == value:
			reducedFeatVec = featVec[:axis]
			reducedFeatVec.extend(featVec[axis+1:])
			retDataSet.append(reducedFeatVec)
	return retDataSet
	
def discreteIntoBase4(vector):
	upLimit = max(vector)
	downLimit = min(vector)
	sectionSize = (upLimit - downLimit) / 4
	retVector = []
	for num in vector:
		retVector.append(int(round(num / sectionSize)))		
	return retVector
	
def chooseBestFeatureToSplit(dataSet):
	numFeatures = len(dataSet[0]) - 1
	baseEntropy = getShannonEnt(dataSet)
	bestInfoGain = 0.0; bestFeature = -1
	for i in range(numFeatures):
		featList = [example[i] for example in dataSet]
		uniqueVals = set(featList)   #de-duplicate value range in value domain
		newEntropy = 0.0
		for value in uniqueVals:
			subDataSet = splitDataSet(dataSet, i, value)
			prob = len(subDataSet)/float(len(dataSet))
			newEntropy += prob * getShannonEnt(subDataSet)
		infoGain = baseEntropy - newEntropy
		if(infoGain > bestInfoGain):
			bestInfoGain = infoGain
			bestFeature = id
	return bestFeature

	
[features,markVec] = readData('foodData.csv', True, True)
discreteFeats = []
for feat in features:
	discreteFeats.append(discreteIntoBase4(feat))
	
dataSet = createDataSet(discreteFeats,markVec)

#print dataSet
print splitDataSet(dataSet,0,1)
#print discreteFeats
#print markVec

	