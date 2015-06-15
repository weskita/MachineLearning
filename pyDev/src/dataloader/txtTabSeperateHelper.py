#from numpy import *
#load data from tab seperated text files.
#The last colume is the dependent variable, called label, return labelMat
#The other columes are the independent variable, called features, returned dataMat. 
def loadData(filePath):
	numFeat = len(open(filePath).readline().split('\t')) - 1
	dataMat = []
	labelMat = []
	fr = open(filePath)	
	for line in fr.readlines():
		lineArr = []		
		curLine = line.split('\t')		
		for i in range(numFeat):
			if len(curLine) < numFeat:
				continue			
			lineArr.append(float(curLine[i]))
		dataMat.append(lineArr)
		labelMat.append(float(curLine[-1]))
		
	return dataMat,labelMat