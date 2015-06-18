#coding: utf8
'''
Created on 2015��6��16��

@author: Sean Zhao
'''
from numpy import *
from dataloader.txtTabSeperateHelper import loadNumData

#default split point: the mean value of last feature.
def regLeaf(dataSet):
    return mean(dataSet[:,-1])

def regErr(dataSet):
    return var(dataSet[:,-1]) * shape(dataSet)[0]

def regTreeEval(model, inDat):
    return float(model)

def modelTreeEval(model, inDat):
    n = shape(inDat)[1]
    X = mat(ones((1,n+1)))
    X[:,1:n+1]=inDat
    return float(X*model)

class treeNode:
    def __init__(self,feat,val,right,left):
        featureToSplitOn = feat
        valueOfSplit = val
        rightBranch = right
        leftBranch = left
        
class CART:
    @staticmethod
    def binSplitDataSet(dataSet,featCol,value):
        mat0 = dataSet[nonzero(dataSet[:,featCol] > value)[0],:][0]
        mat1 = dataSet[nonzero(dataSet[:,featCol] <= value)[0],:][0]
        return mat0,mat1
    
    @staticmethod
    def createTree(dataSet, leafType=regLeaf, errType=regErr, ops=(1,4)):
        feat,val = CART.chooseBestSplit(dataSet, leafType, errType, ops)        
        #return only value when meeting stop condition.
        if feat == None: return val
        
        retTree = {}
        retTree['spInd'] = feat
        retTree['spVal'] = val
        lSet, rSet = CART.binSplitDataSet(dataSet,feat,val)
        
        retTree['left'] = CART.createTree(lSet, leafType, errType, ops)
        retTree['right'] = CART.createTree(rSet, leafType, errType, ops)
        return retTree
    
    @staticmethod
    def chooseBestSplit(dataSet, leafType=regLeaf, errType = regErr, ops=(1,4)):        
        tolS = ops[0]; tolN = ops[1]
        if len(set(dataSet[:,-1].T.tolist()[0])) == 1:
            return None,leafType(dataSet)
        
        m,n = shape(dataSet)
        S = errType(dataSet)
        bestS = inf; bestIndex = 0; bestValue = 0
        for featIndex in range(n-1):
            for splitVal in set(dataSet[:,featIndex]):
                mat0,mat1 = CART.binSplitDataSet(dataSet,featIndex,splitVal)
                if (shape(mat0)[0] < tolN or (shape(mat1)[0] < tolN)): continue
                newS = errType(mat0) + errType(mat1)
                if newS < bestS:
                    bestIndex = featIndex
                    bestValue = splitVal
                    bestS = newS
        print bestIndex,bestValue
        if (S - bestS) < tolS:
            return None, leafType(dataSet)
        
        mat0,mat1 = CART.binSplitDataSet(dataSet, bestIndex, bestValue)
        if (shape(mat0)[0] < tolN) or (shape(mat1)[0] < tolN):
            return None,leafType(dataSet)
       
        return bestIndex,bestValue
    
    @staticmethod
    def isTree(obj):
        return (type(obj).__name__=='dict')
    
    @staticmethod
    def getMean(tree):
        if CART.isTree(tree['right']): tree['right'] = CART.getMean(tree['right'])
        if CART.isTree(tree['left']): tree['left'] = CART.getMean(tree['left'])
        return (tree['left'] + tree['right']) / 2
    
    @staticmethod
    def prune(tree,testData):
        if shape(testData)[0] <= 0 : return CART.getMean(tree)
        if (CART.isTree(tree['left']) or CART.isTree(tree['right'])) :
            lSet, rSet = CART.binSplitDataSet(testData,tree['spInd'],tree['spVal'])
        if CART.isTree(tree['left']): tree['left'] = CART.prune(tree['left'], lSet)
        if CART.isTree(tree['right']): tree['right'] = CART.prune(tree['right'], rSet)
        if not (CART.isTree(tree['left']) or CART.isTree(tree['right'])):
            lSet,rSet = CART.binSplitDataSet(testData, tree['spInd'], tree['spVal'])
            errorNoMerge = sum(power(lSet[:,-1] - tree['left'], 2)) + sum(power(lSet[:,-1] - tree['right'], 2)) 
            treeMean = (tree['left'] + tree['right'] / 2.0)
            errorMerge = sum(power(testData[:,-1] - treeMean,2))
            if errorMerge < errorNoMerge:
                print 'merging'
                return treeMean
            else:
                return tree
        else:
            return tree
        
    @staticmethod
    def treeForeCast(tree, inData, modelEval=regTreeEval):
        return
 
def _main():
    myDat =  loadNumData('../../data/ex00.txt')  
    myMat = mat(myDat)    
    tree = CART.createTree(myMat)    
    print tree         
    
_main()