from numpy import *
from regressionPlotter import LinearPlotter as plotter

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
			weights[j,j] = exp(diffMat*diffMat.T/(-2.0*k**2))
			
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

def plot(xMat,yVec,ws):
	plt = plotter()
	#ax = plt.getSubplot()
	plt.plotLineScatter(xMat,yVec,ws.T)
	
def plotBrokenLine(xMat,yVec,yHat):
	plt = plotter()
	plt.plotBrokenLinesScatter(xMat,yVec,yHat)

def _main():
	featVec = mat([[1,0,1],[1,1,0],[1,0,0],[1,2,6],[1,4,9],[1,6,3]])
	yVec = mat([3,6,1,21,39,32])	 
	ws = LinearRegressionHelper.standardRegress(featVec,yVec)
	#print ws
	plot(featVec,yVec,ws)
	yHat = LinearRegressionHelper.continual_lwlr(featVec,featVec,yVec,1)
	#print featVec,mat(yVec).T
	#print yHat
	plotBrokenLine(featVec,yVec,yHat)
	
_main()
	