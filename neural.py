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
        self.epsilon = 0.4
        

    
    def setInputs(self, inputs):
        self.inputs = inputs
        if (len(inputs) != len(self.weights)):
            self.setWeights ([0]*len(inputs))

    
    def setInputsAndWeights(self, inputs, weights):
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
        signal = 0
        for pair in zip(self.inputs,self.weights):
            signal += pair[0]*pair[1]

        self.setSignal(signal)


    def updateWeights(self, error):
        print("start of update weights!")
        self.threshold -= self.epsilon*error
        print(self.threshold)
        for i, weight in enumerate(self.weights):
            print(self.weights[i])
            print(error)
            self.weights[i] += error*self.inputs[i]*self.epsilon
            print(self.weights[i])
        print("end of update weights!")

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
        return self.weights
    def getThreshold(self):
        return self.threshold
    def getEpsilon(self):
        return self.epsilon


class Row:
    def __init__(self):
        self.nodeList = []

    def __init__(self, size):
        self.nodeList = []
        self.Initialize(size)

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

    def setWeightLists(self, weightLists):
        if (len(weightLists) != len(self.nodeList)):
            return -1
        for i, weightList in enumerate(weightLists):
            self.nodeList[i].setWeights(weightList)
        return 0

    def updateNodes(self):
        for node in self.nodeList:
            node.updateSignal()

    def updateWeightLists(self, errorList):
        print ("update start")
        if (len(errorList) != len(self.nodeList)):
            return -1
            print ("update exit")
        for i, error in enumerate(errorList):
            self.nodeList[i].updateWeights(error)
        print ("update end")
        return 0

    def setSignalList(self, signalList):
        if (len(signalList) != len(self.nodeList)):
            return -1
        for i, signal in enumerate(signalList):
            self.nodeList[i].setSignal(signal)
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

    def getWeightLists(self):
        ret = []
        for node in self.nodeList:
            ret.append(node.getWeights())
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


class RowNet:
    def __init__(self,x,y):
        self.rowNum = x
        self.rowList = []
        for i in range(0,x):
            self.rowList.append(Row(y))
        #try to get the outputs of i to be the inputs of i + 1
        self.mapInputs()

    def mapInputs(self):
        inputs = []
        for row in self.rowList:
            self.mapRowInputs(row, inputs)
            inputs = row.getSignalList()

    def mapRowInputs(self, row, inputs):
        row.setInputLists([inputs] * row.getSize())

    def addRow(self, row):
        self.rowList.append(row)
        self.mapInputs()
        self.rowNum += 1

    def delRow(self, row):
        if (row >= 0 and row < self.rowNum):
            self.rowList.remove(row)
            self.mapInputs()
            self.rowNum -= 1
            return 0
        return -1

    def initializeWeights(self):
        numInputs = 0
        for row in self.rowList:
            row.setWeightLists([[0.5] * numInputs] * row.getSize())
            numInputs = row.getSize()

    def propagateSignals(self):
        signalList = self.getInputs()
        for row in self.rowList[1:]:
            self.mapRowInputs(row, signalList)
            row.updateNodes()
            singalList = row.getSignalList()


    def getRow(self, i):
        if i >= len(self.rowList):
            return -1
        return self.rowList[i]

    def getRowSignals(self, i):
        return self.getRow(i).getSignalList()
    def getInputs(self):
        return self.getRowSignals(0)
    def getOutputs(self):
        return self.getRowSignals(self.rowNum - 1)
    def setRowSignals(self, i, signalList):
        self.getRow(i).setSignalList(signalList)
    def setInputs(self, signalList):
        self.setRowSignals(0, signalList)
    def setOutputs(self, signalList):
        self.setRowSignals(self.rowNum - 1, signalList)

    def printRowSignals(self, row):
        print(self.getRowSignals(row))
    def printSignals(self):
        for i, row in enumerate(self.rowList):
            self.printRowSignals(i)
            

if __name__ == "__main__":
    net = RowNet(2,4)
    net.setInputs([3,2,1,1])
    net.initializeWeights()
    net.propagateSignals()

    node = Node()
    node.setInputs([1])
    node.setWeights([1])
    keepGoing = 1
    while keepGoing:
        node.updateSignal()
        print("the signal is: ", node.getSignal())
        print("the weight is: ", node.getWeights())
        raw_input("Done looking?")
        error = (1 - node.getInputs()[0]) - node.getSignal()
        print ("the error is: ", error)
        node.updateWeights( error)
        signal = int(raw_input("Next input? "))
        node.setInputs([signal])
        
