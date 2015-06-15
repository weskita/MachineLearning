from numpy import *

def loadDataSet():
	
	return None
	
def sentence2WordsVec(sentence):
	import re
	returnList = re.split('[\s\.\?\!,]+',sentence)
	for word in returnList:
		if word == None or len(word) == 0: returnList.remove(word)
	return returnList
	
	
def setOfWords2Vec(vocabList, inputSet):
	returnVec =[0] * len(vocabList)
	for word in inputSet:
		if word in vocabList:
			returnVec[vocabList.index(word)] = 1
		else: print "the word: %s is not in my Vocabulary!" % word
	return returnVec
	
def getSetList(inputArray):
	res = []
	for item in inputArray:
		if item not in res:
			res.append(item)			
	return res
	
def getCountDict(inputArray):
	res = {}
	for item in inputArray:
		res[item] = res.get(item,0) + 1
		
	return res
	
#This implementation expand the 2 category classification to n-categories classification 	
def trainNB(trainMatrix,trainCategory):
	numTrainDocs = len(trainMatrix)
	#trainCategory = trainMatrix[:,-1]
	#print trainCategory
	numWords = len(trainMatrix[0])
	countCategory = getCountDict(trainCategory)
	pCategories = {}	
	for item in countCategory.items():
		pCategories[item[0]] = float(item[1])/numTrainDocs
		
	vecCategories = {}
	sumWordCategories = {}
	for i in range(numTrainDocs):
		currentCategory = trainCategory[i]		
		vecCategories[currentCategory] = vecCategories.get(currentCategory,ones(numWords)) + trainMatrix[i]
		sumWordCategories[currentCategory] = sumWordCategories.get(currentCategory,numWords) + sum(trainMatrix[i])
		
	pWordCategories = {}
	for item in countCategory.keys():
		pWordCtg = vecCategories[item]/sumWordCategories[item]
		#print pWordCtg
		pWordCategories[item] = log(pWordCtg)
	return pWordCategories,pCategories
	
def classifyNB(pVec,pWordCategories,pCategories):
	res = None
	for category in pWordCategories.items():
		#print category
		pCi = sum(category[1] * pVec) + log(pCategories[category[0]])
		#print pCi
		if (res == None or pCi > res[1]):
			res = (category[0],pCi)
	res = (res[0],exp(res[1]))		
	return res
		
	
print sentence2WordsVec("This is a	sentence , isn't it?")
testMatrix = array([[1,0,1,0],[0,1,0,1],[1,1,1,0],[1,0,1,1]])

pWC,pC = trainNB(testMatrix,['a','b','d','a'])
#print pWC
#print pC

print classifyNB([0,1,0,2],pWC,pC)
#print getSetList(array(['a', 'a', 'b','c','a','d']).tolist())