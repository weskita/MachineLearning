#pro. Not very complicated calculation. Easy to understand the classification result.Not sensitive to mid-level value. 
#		Ability to process non-relative feature.

#con. Bias to intenser samples, since they can bring more information gain.
#		Time-cost to train, time-efficient to use.
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

def majorityCnt(classList):
	classCount = {}
	for vote in classList:
		if vote not in classCount.keys(): classCount[vote] = 0
		classCount[vote] +=1
	sortedClassCount = sorted(classCount.iteritems,key=operator.itemgetter(1),reverse=True)
	return sortedClassCount[0][0]
	
def createTree(dataSet,labels):
	classList = [example[-1] for example in dataSet]
	if classList.count(classList[0]) == len(classList):
		return classList[0]
	if len(dataSet[0]) == 1:
		return majorityCnt(classList)
		
	bestFeat = chooseBestFeatureToSplit(dataSet)
	bestFeatLabel = labels[bestFeat]
	myTree = {bestFeatLabel:{}}
	del(labels[bestFeat])
	featValues = [example[bestFeat] for example in dataSet]
	uniqueVals = set(featValues)
	for value in uniqueVals:
		subLabels = labels[:]
		myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet,bestFeat,value),subLabels)
	return myTree
	
def storeTree(inputTree,filename):
	import pickle
	fw = open(filename,'w')
	pickle.dump(inputTree,fw)
	fw.close()
	
def grabTree(filename):
	import pickle
	fr = open(filename,'r')
	return pickle.load(fr)

	
[features,markVec] = readData('foodData.csv', True, True)
discreteFeats = []
for feat in features:
	discreteFeats.append(discreteIntoBase4(feat))
	
dataSet = createDataSet(discreteFeats,markVec)

#print dataSet
print splitDataSet(dataSet,0,1)
#print discreteFeats
#print markVec

	