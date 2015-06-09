import matplotlib.pyplot as plt
from numpy import *
class LinearPlotter:
	fig = None
	ax = None	
	
	def __init__(self):
		self.fig = plt.figure()
		
	def getSubplot(self):
		if self.ax == None:
			self.ax = self.fig.add_subplot(111)			
		return self.ax
		
	def clearFigure(self):
		if self.fig != None:
			self.fig.clf()
		
	def plotScatter(self,xMat,yMat,m,ax):	
		print xMat
		ax.scatter(xMat[:,m].flatten().A[0], yMat.T[:,0].flatten().A[0])

	def plotLine(self,xMat,ws,m,ax):		
		xLocal = xMat.copy()
		xLocal.sort(0)
		yHat = xLocal * ws.T
		#print xLocal[:,m],yHat
		ax.plot(xLocal[:,m],yHat)
	
	#plot scatter (xMat(:,m),yMat) and line (xMat(:,m),ws) on screen 
	def plotLineScatter(self,xMat,yMat,ws,m = 1,ax = None):
		# 0 is the subscript for const item, it should be 1.
		if m <= 0:
			return
		if ax == None:
			ax = self.getSubplot()
		self.plotScatter(xMat,yMat,m,ax)
		self.plotLine(xMat,ws,m,ax)
		plt.show()
		
	def plotBrokenLines(self,xMat,yHat,m = 1,ax = None):
		if ax == None:
			ax = self.getSubplot()
		srtInd = xMat[:,1].argsort(0)    #return the sorted indexes
		#print srtInd
		#print yHat
		#print xMat
		xSort = xMat[srtInd][:,0,:]
		ySort = mat(yHat.T[srtInd][:,0])
		print xSort
		print ySort
		ax.plot(xSort[:,1].flatten().A[0],ySort.flatten().A[0])
		
		
	def plotBrokenLinesScatter(self,xMat,yMat,yHat,m = 1,ax = None):
		if ax == None:
			ax = self.getSubplot()
		self.plotScatter(xMat,yMat,m,ax)
		self.plotBrokenLines(xMat,yHat,m,ax)
		plt.show()		
		
def _main():	
	plotter = LinearPlotter()
	ax = plotter.getSubplot()
	xMat = mat([[1,3],[1,0],[1,1]])
	yMat = mat([9,2,7])
	yHat = mat([3,6,9])
	ws = mat([1,2])	
	#plotter.plotLineScatter(xMat,yMat,ws,1,ax)
	#plotter.clearFigure()
	plotter.plotBrokenLinesScatter(xMat,yMat,yHat)
	

#_main()