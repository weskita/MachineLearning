from gensim.models import word2vec
import logging
import numpy as np
class sentence:    
    raw_vector = []    
    
    #__weight = 0
    
    def __init__(self,raw_sentences):
        self.raw_vector = raw_sentences.split()        
		
    def speak(self):
        print("%s is speaking: I am %d years old" %(self.name,self.age))
		
class sentence2vec:
	wordmodel = None
	sentenceRepo = []
	sentencesVec = []
	numPiece = 7
	
	def __init__(self,model):
		self.wordmodel = model	
		
	def calcSentenceVec(self,sentence):
		words = sentence.raw_vector
		stVec = []
		for word in words:
			stVec.append(self.wordmodel[word])			
		return stVec	
		
	def loadSentenceRepo(self):
		self.sentenceRepo = ["jack like swimming","harry like table","hello this is a sampled sentence for long sentence"]
		stItem = None
		for raw_sentence in self.sentenceRepo:
			stItem = sentence(raw_sentence)
			self.sentencesVec.append(self.calcSentenceVec(stItem))	
	
	def calcStVecsDist(self,vecsA,vecsB):
		wordCountA = len(vecsA)
		wordCountB = len(vecsB)		
		dimSize = vecsA[0].shape[0]
		
		vecSemanticCentroidA = self.__calcSegCentroids(vecsA,wordCountA,dimSize)
		vecSemanticCentroidB = self.__calcSegCentroids(vecsB,wordCountB,dimSize)
		
		print len(vecSemanticCentroidA)
		print len(vecSemanticCentroidB)
		
	def __calcSegCentroids(self,stWordVecs,wordCount,dimSize):
		res = []
		if wordCount < self.numPiece:
			res = stWordVecs[:]
			for i in range(wordCount,self.numPiece):
				res.append(np.zeros((dimSize,),dtype=np.float32))
		else:
			#TODO: fix this segmentation algorithm
			step = (wordCount + self.numPiece - 1)/self.numPiece
			print step
			for i in range(0,wordCount - step,step):
				segCentroid = self.__calcAvgVecOffset(stWordVecs[i:i+step])
				res.append(segCentroid)
				
			modEnd = step * self.numPiece
			if modEnd > wordCount:
				residualStart = modEnd - self.numPiece
				for i in range(residualStart,wordCount):
					print i
					print stWordVecs[i]
					segCentroid = self.__calcAvgVecOffset([stWordVecs[i]])
					res.append(segCentroid)	
				print "here"			
		return res	
		
		
	def getSplitPoint(self,start,end,nParts):
		#print start,end,nParts
		
		if nParts == end - start + 1:
			return range(start,end + 1)
		
		if (end == start) or (nParts == 1):
			return [end]
		else:
			midPoint = start + (end - start + 1) / 2
			preParts = nParts / 2
			postParts = nParts - preParts
			preRes = self.getSplitPoint(start,midPoint,preParts)
			postRes = self.getSplitPoint(midPoint + 1,end,postParts)
			
			#print preRes
			#print postRes
			res = []
			
			if preRes != None:
				res = preRes[:]			
				
			if postRes != None:	
				if res != None:
					res.extend(postRes)
				else:
					res = postRes
				
			print res			
			return res
		
			
	def __calcAvgVecOffset(self,vecSet):
		dimSize = vecSet[0].shape[0]
		res = np.zeros((dimSize,), dtype=np.float32)
		for vec in vecSet:
			res += vec
		res /= len(vecSet)	
		return res
		
		
	

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
model = word2vec.Word2Vec.load_word2vec_format('../models/text8.model.bin', binary=True)
stModel = sentence2vec(model)
stModel.loadSentenceRepo()

#stModel.calcStVecsDist(stModel.sentencesVec[0],stModel.sentencesVec[2])
print stModel.getSplitPoint(0,12,7)

print model.most_similar(['girl', 'father'], ['boy'], topn=3)

	
	

