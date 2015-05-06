import csv
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
		
matrix2csv([[1,2,3],[4,5,6],[0,7,9]],"mycsv.csv",['a','b','c'])
print csv2matrix("mycsv.csv",True,True)