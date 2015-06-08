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
		ax.scatter(xMat[:,m].flatten().A[0], yMat.T[:,0].flatten().A[0])

	def plotLine(self,xMat,ws,m,ax):		
		xLocal = xMat.copy()
		xLocal.sort(0)
		yHat = xLocal * ws.T
		print xLocal[:,m],yHat
		ax.plot(xLocal[:,m],yHat)
	
	#plot scatter (xMat(:,m),yMat) and line (xMat(:,m),ws) on screen 
	def plotLineScatter(self,xMat,yMat,ws,m = 1,ax = None):
		# 0 is the subscript for const item.
		if m <= 0:
			return
		if ax == None:
			ax = self.getSubplot()
		self.plotScatter(xMat,yMat,m,ax)
		self.plotLine(xMat,ws,m,ax)
		plt.show()
		
def _main():	
	plotter = LinearPlotter()
	ax = plotter.getSubplot()
	xMat = mat([[1,0],[1,1],[1,3]])
	yMat = mat([2,7,9])
	ws = mat([1,2])	
	plotter.plotLineScatter(xMat,yMat,ws,1,ax)
	plotter.clearFigure()	
	plotter.plotLineScatter(xMat,yMat,ws,1,ax)

#_main()