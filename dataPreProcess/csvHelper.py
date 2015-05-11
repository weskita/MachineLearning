import csv
import string
import numpy
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
	#print res
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
	return [featVecs,markVec]
	
# Union the features vectors and mark vector into a matrix
def createDataSet(featVecs,markVec):
	res = []
	i = 0
	print featVecs[i]	
	for mark in markVec:		
		featVecs[i].append(mark)		
		#print featVecs[i]
		res.append(featVecs[i])
		i+=1
	return res
		
#matrix2csv([[1,2,3],[4,5,6],[0,7,9]],"mycsv.csv",['a','b','c'])
#print csv2matrix("mycsv.csv",True,True)