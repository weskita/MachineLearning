from numpy import *
from plotter.regressionPlotter import LinearPlotter as plotter
from dataloader.txtTabSeperateHelper import *
class LinearRegressionHelper: 
	@staticmethod
	def standardRegress(xArr, yArr):
		xMat = mat(xArr); yMat = mat(yArr).T
		xTx = xMat.T * xMat	
		ws = linalg.solve(xTx,xMat.T * yMat)		
		return ws
		
	@staticmethod
	def lwlr(testPoint,xArr, yArr, k=1.0):
		xMat = mat(xArr); yMat = mat(yArr).T
		m = shape(xMat)[0]
		weights = mat(eye((m)))
		for j in range(m):
			diffMat = testPoint - xMat[j,:]
			weights[j,j] = exp(diffMat*diffMat.T / (-2.0*k**2))
			
		xTx = xMat.T * (weights * xMat)
		xTy = xMat.T * (weights * yMat)		
		try:
			ws = linalg.solve(xTx,xTy)
		except linalg.LinAlgError:
			print "Meet LinAlgError('Singular matrix')"
		return testPoint * ws
	@staticmethod
	def continual_lwlr(testArr,xArr, yArr, k=1.0):		
		m = shape(testArr)[0]
		yHat = zeros(m)
		for i in range(m):			
			yHat[i] = LinearRegressionHelper.lwlr(testArr[i],xArr,yArr,k)	
			#print yHat[i]
		return yHat
		
	@staticmethod
	def __regularizeFeature__(featVec):
		featMat = mat(featVec)
		featMeans = mean(featMat)
		featStdVar = var(featMat)
		res = (featMat - featMeans)/featStdVar
		return res
		
	@staticmethod
	def ridgeRegress(xArr,yArr,lam = 0.2):
		xMat = mat(xArr)
		yMat = mat(yArr)
		xNorm = LinearRegressionHelper.__regularizeFeature__(xMat)		
		yNorm = (yMat - mean(yMat)).T   #translate y vector from raw vector to colume vector
		
		xTx = xNorm.T * xNorm
		denom = xTx + eye(shape(xNorm)[1])*lam
		if linalg.det(denom) == 0.0:
			print "Matrix singular"
			return
		ws = denom.I * (xNorm.T * yNorm)			
		return ws
	@staticmethod
	def __rssError__(yArr,yHatArr): #yArr and yHatArr both need to be arrays
		return ((yArr-yHatArr)**2).sum()	

	@staticmethod
	def stageWiseRegress(xArr,yArr,eps = 0.01, numIt = 100):
		xMat = mat(xArr)
		yMat = mat(yArr).T
		yMat = yMat - mean(yMat)
		xMat = LinearRegressionHelper.__regularizeFeature__(xMat)
		m,n = shape(xMat)
		returnMat = zeros((numIt,n))
		ws = zeros((n,1))
		wsTest = ws.copy()
		wsMax = ws.copy()
		for i in range(numIt):
			#print ws.T
			lowestError = inf
			for j in range(n):
				for sign in [-1,1]:
					wsTest = ws.copy()
					wsTest[j] += eps*sign
					yTest = xMat * wsTest
					rssE = LinearRegressionHelper.__rssError__(yMat.A,yTest.A)
					if rssE < lowestError:
						lowestError = rssE
						wsMax = wsTest
				ws = wsMax.copy()
				returnMat[i,:] = ws.T
		return returnMat		
	

def plot(xMat,yVec,ws):
	plt = plotter()
	plt.plotLineScatter(xMat,yVec,ws.T)
	
def plotBrokenLine(xMat,yVec,yHat):
	plt = plotter()
	plt.plotBrokenLinesScatter(xMat,yVec,yHat)
	

def __testStdRegression():
	featVec = mat([[1,0,1],[1,1,0],[1,0,0],[1,2,6],[1,4,9],[1,6,3]])
	yVec = mat([3,6,1,21,39,32])	 
	ws = LinearRegressionHelper.standardRegress(featVec,yVec)	
	plot(featVec,yVec,ws)
	
def __testLwlrRegression():
	xData,yData = loadLabeledData('../../data/ex0.txt')
	xMat = mat(xData)
	yMat = mat(yData)	
	yHat = LinearRegressionHelper.continual_lwlr(xMat,xMat,yMat,0.01)	
	plotBrokenLine(xMat,yMat,yHat)
def __testRidgeRegress():
	xData,yData = loadLabeledData('../../data/ex0.txt')
	#xData = mat([[1,0,1],[1,1,0],[1,0,0],[1,2,6],[1,4,9],[1,6,3]])
	#yData = mat([3,6,1,21,39,32])
	xMat = LinearRegressionHelper.__regularizeFeature__(xData)
	yMat = mat(yData)	
	ws = LinearRegressionHelper.ridgeRegress(xMat,yMat,0.3)	
	plot(xMat,yMat,ws)
	return	

def __testStageWiseRegress():
	xData,yData = loadLabeledData('../../data/ex0.txt')
	#xData = mat([[1,0,1],[1,1,0],[1,0,0],[1,2,6],[1,4,9],[1,6,3]])
	#yData = mat([3,6,1,21,39,32])
	xMat = LinearRegressionHelper.__regularizeFeature__(xData)
	yMat = LinearRegressionHelper.__regularizeFeature__(yData)	
	wsIters = LinearRegressionHelper.stageWiseRegress(xMat, yMat)	
	wsLast = mat(wsIters[-1,:])
	plot(xMat,yMat,wsLast.T)
	return	

def _main():	
	#__testRidgeRegress()
	__testStageWiseRegress()
	
_main()
	