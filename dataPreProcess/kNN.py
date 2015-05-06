from numpy import *
import operator

def classify0(inX,dataSet,labels,k):
	dataSetSize = dataSet.shape[0]      				#the shape will return the size of a matrix,like for a 4*3 matrix, shape will return [4L,3L]
	diffMat = tile(inX, (dataSetSize,1)) - dataSet   	#tile the input vector and calc a difference matrix 
	sqDiffMat = diffMat**2 								#calc the square matrix
	sqDistances = sqDiffMat.sum(axis=1)					#get sum of difference square 
	distances = sqDistances ** 0.5
	sortedDistIndicies = distances.argsort()
	classCount={}
	for i in range(k):
		voteIlabel = labels[sortedDistIndicies[i]]
		classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1
	sortedClassCount = sorted(classCount.iteritems(),key=operator.itemgetter(1), reverse=True)
	return sortedClassCount
	
print classify0([1,2,3],array([[0,9,8],[4,7,8],[4,7,6]]), ['a','b','a','a'],2)