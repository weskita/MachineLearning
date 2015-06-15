import csv
import string
import numpy
import random
class DataSet:
	featVecs = []
	labels = []
	featMatrix = None
	def __init__(self,featVecs,labels):
		self.featVecs = featVecs
		self.labels = labels
		self.featMatrix = numpy.array(featVecs)
		
	def splitDataSet(self,trainSetPart,testSetPart):
		cyclePart = trainSetPart + testSetPart
		totalRecord = len(self.featVecs)
	
		trainVecs = []
		trainLabels = []
		testVecs = []
		testLabels = []
	
		#we take the random split in totalPart size.
		iterTimes = totalRecord/cyclePart
		residualNum = totalRecord % cyclePart
		for i in range(iterTimes):
			offset = i * cyclePart
			shuffledIndex = range(offset,offset + cyclePart)
			random.shuffle(shuffledIndex)
			for j in range(trainSetPart):
				trainVecs.append(self.featVecs[shuffledIndex[j]])
				trainLabels.append(self.labels[shuffledIndex[j]])
			for j in range(trainSetPart,cyclePart):
				testVecs.append(self.featVecs[shuffledIndex[j]])
				testLabels.append(self.labels[shuffledIndex[j]])
				
		for i in range(-residualNum-1,-1):
			trainVecs.append(self.featVecs[shuffledIndex[i]])
			trainLabels.append(self.labels[shuffledIndex[i]])
		#print trainVecs
		#print testVecs
		trainSet = DataSet(trainVecs,trainLabels)
		testSet = DataSet(testVecs,testLabels)
	
		return trainSet,testSet

def matrix2csv(lines,csv_file_path,title_line):
	writer = csv.writer(file(csv_file_path, 'wb'))
	writer.writerow(title_line)	
	for line in lines:
		writer.writerow(line)
		
def csv2matrix(csv_file_path, has_title_line, has_line_header):
	reader = csv.reader(file(csv_file_path, 'rb'))
	rawMatrix = []
	start_offset = 1 if has_line_header else 0
	passed_first_line = False	
	
	for line in reader:
		if(has_title_line and not passed_first_line):
			passed_first_line = True
			continue		
		rawMatrix.append(line[start_offset:])
		
	matrix = numpy.array(rawMatrix)
	return matrix
	
def strVec2Numvec(strVec):
	res = []
	for item in strVec:
		res.append(string.atof(item))	
	return res	
	
def readData(filePath, hasTitleLine, hasLineHeader):	
	inputData = csv2matrix(filePath, hasTitleLine, hasLineHeader)
	strMatrix = numpy.array(inputData)
	size = strMatrix.shape
	strSet = strMatrix[:,0:size[1] - 1]
	featVecs = []
	for item in strSet:
		featVecs.append(strVec2Numvec(item))
	markVec = strMatrix[:,size[1] - 1]
	return DataSet(featVecs,markVec)
	
# Union the features vectors and mark vector into a matrix
def createDataSet(featVecs,markVec):
	res = []
	i = 0
	print featVecs[i]	
	for mark in markVec:		
		featVecs[i].append(mark)		
		res.append(featVecs[i])
		i+=1
	return res
	


def _main():	
	matrix2csv([[1,2,3],[4,5,6],[0,7,9]],"../../data/mycsv.csv",['a','b','c'])
	print csv2matrix("../../data/mycsv.csv",True,True)

	totalDataSet = readData("../../data/lenses.csv",False,True)
	dataSet2 = readData('../../data/foodData.csv', True, True)
	trainSet,testSet = totalDataSet.splitDataSet(9,1)
	print dataSet2
	print trainSet.featMatrix
	print testSet.featMatrix
	
#_main()