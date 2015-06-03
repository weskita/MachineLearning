#Pro. Very simple.
#Con. Sensitive to data distribution. Large computation work.
import csvHelper
from numpy import *
import operator

#classify a vector inX with a train set dataSet with labels, get the top-k to judge
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
	
def assertClassifyRight(classifyRes,testLable):
	if classifyRes[0][0] == testLable:
		print "Totally Correct"
		return 1
	for item in classifyRes:
		if item[0] == testLable:
			print "Ambiguatual Correct"
			return 0	
	print "Assertion Failed"
	return -1

def _main():
	#print classify0([1,2,3],array([[0,9,8],[4,7,8],[4,7,6]]), ['a','b','a'],2)
	totalDataSet = csvHelper.readData("lenses.csv",False,True)
	trainSet,testSet = totalDataSet.splitDataSet(9,1)
	res = classify0(testSet.featVecs[0],trainSet.featMatrix,trainSet.labels,3)	
	assertClassifyRight(res,testSet.labels[0])
	
_main()