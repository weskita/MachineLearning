'''
Created on 2015Äê6ÔÂ16ÈÕ

@author: Sean Zhao
'''
from numpy import *
from scimath.units.plugin.new_scalar_wizard import NewScalarWizard

#default split point: the mean value of last feature.
def regLeaf(dataSet):
    return mean(dataSet[:,-1])

def regErr():
    return None


class treeNode:
    def __init__(self,feat,val,right,left):
        featureToSplitOn = feat
        valueOfSplit = val
        rightBranch = right
        leftBranch = left
        
class CART:
    @staticmethod
    def binSplitDataSet(dataSet,featCol,value):
        mat0 = dataSet[nonzero(dataSet[:,featCol] > value)[0],:]
        mat1 = dataSet[nonzero(dataSet[:,featCol] <= value)[0],:]
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
    def chooseBestSplit(dataSet, leafType, errType, ops):        
        tolS = ops[0]; tolN = ops[1]
        if len(set(dataSet[:,-1]).T.tolist()[0]) == 1:
            return None,leafType(dataSet)
        
        m,n = shape(dataSet)
        S = errType(dataSet)
        bestS = inf; bestIndex = 0; bestValue = 0
        for featIndex in range(n-1):
            for splitVal in set(dataSet[:,featIndex]):
                mat0,mat1 = CART.binSplitDataSet(dataSet,bestIndex,bestValue)
                if (shape(mat0)[0] < tolN or (shape(mat1)[0] < tolN)): continue
                newS = errType(mat0) + errType(mat1)
                if newS < bestS:
                    bestIndex = featIndex
                    bestValue = splitVal
                    bestS = newS
        
        if (S - bestS) < tolS:
            return None, leafType(dataSet)
        mat0,mat1 = CART.binSplitDataSet(dataSet, bestIndex, bestValue)
        if (shape(mat0)[0] < tolN) or (shape(mat1)[0] < tolN):
            return None,leafType(dataSet)
        
        return bestIndex,bestValue
                    
        return None,None