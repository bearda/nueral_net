#This should define three types of objects, and thier APIs
#   1. Nodes
#   2. Rows
#       A list of nodes
#   3. Nets
#       A list of rows

class Node:
    def __init__(self):
        self.signal = 0
        self.inputs = []
        self.weights= []
        self.threshold = 1
        self.epsilon = 0
        

    
    def setInputs(self, inputs):
        self.inputs = inputs
        if (len(inputs) != len(self.weights)):
            self.setWeights ([0]*len(weights))
    
    def setInputs(self, inputs, weights):
        if (len(inputs) != len(weights)):
            return -1
        self.inputs = inputs
        self.weights = weights
        return 0
    
    def setWeights(self, weights):
        if (len(self.inputs) != len(weights)):
            return -1
        self.weights = weights
        return 0

    def updateSignal(self):
        tmp = 0
        for inpt in self.inputs:
            tmp += inpt[0]*inpt[1]

        if tmp >= self.threshold:
            self.setSignal(1)
        else:
            self.setSignal(0)

    def updateWeights(self, error):
        self.threshold -= self.epsilon*error
        for i, weight in enumerate(self.weights):
            weight += error*self.inputs[i]*self.epsilon

    def setEpsilon(self, e):
        self.epsilon = e
    def setThreshold(self, t):
        self.threshold = t
    def setSignal(self, s):
        self.signal = s

    def getSignal(self):
        return self.signal
    def getInputs(self):
        return self.inputs
    def getWeights(self):
        return self.Weights
    def getThreshold(self):
        return self.threshold
    def getEpsilon(self):
        return self.epsilon


class Row:
    def __init__(self):
        self.nodeList = []

    def addNode(self, node):
        self.nodeList.append(node)

    def Initialize(self, size):
        self.nodeList = []
        i = 0
        while (i < size):
            self.addNode(Node())
            i += 1

    def setInputLists(self, inputLists):
        if (len(inputLists) != len(self.nodeList)):
            return -1
        for i, inputList in enumerate(inputLists):
            self.nodeList[i].setInputs(inputList)
        return 0

    def updateNodes(self):
        for node in self.nodeList:
            node.updateSignal()

    def updateWeights(self, errorList):
        if (len(errorList) != len(self.nodeList)):
            return -1
        for i, error in enumerate(errorList):
            self.nodeList[i].updateWeights(errorList)
        return 0

    def setSignalList(self, signalList):
        if (len(signalList) != len(self.nodeList)):
            return -1
        for i, signal in enumerate(signalList):
            self.nodeList[i].setSignal(signalList)
        return 0

    def setEpsilonList(self, epsilonList):
        if (len(epsilonList) != len(self.nodeList)):
            return -1
        for i, epsilon in enumerate(epsilonList):
            self.nodeList[i].setEpsilon(epsilon)
        return 0

    def setThresholdList(self, thresholdList):
        if (len(thresholdList) != len(self.nodeList)):
            return -1
        for i, threshold in enumerate(thresholdList):
            self.nodeList[i].setThreshold(threshold)
        return 0

    def getSignalList(self):
        ret = []
        for node in self.nodeList:
            ret.append(node.getSignal())
        return ret

    def getInputLists(self):
        ret = []
        for node in self.nodeList:
            ret.append(node.getInputs())
        return ret

    def getThresholdList(self):
        ret = []
        for node in self.nodeList:
            ret.append(node.getThreshold())
        return ret
        
    def getEpsilonList(self):
        ret = []
        for node in self.nodeList:
            ret.append(node.getEpsilon())
        return ret

    def getSize(self):
        return len(self.nodeList)


r = Row()
r.Initialize(4)
print(r.getEpsilonList())
r.setEpsilonList([1,2,3])
print(r.getEpsilonList())
r.setSignalList([0,4,1,2])