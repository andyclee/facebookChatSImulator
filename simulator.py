from parser import Parsed
from graph import Graph
import random

class Simulator:
    parsed = None
    userGraphs = {} #{User string, User's graph}

    def __init__(self, fn):
        self.parsed = Parsed(fn)
        self.generateGraphs()

    def generateGraphs(self):
        for msg in self.parsed.messages:
            if (msg.user in self.userGraphs):
                self.userGraphs[msg.user].processSentence(msg.message)
            else:
                self.userGraphs[msg.user] = Graph(msg.user)
                self.userGraphs[msg.user].processSentence(msg.message)

    def printNames(self):
        for user in self.userGraphs:
            print("User: " + user)

    def simulateSentence(self, user):
        uGraph = self.userGraphs[user]
        initialWN = uGraph.getInitial()
        fullMsg = initialWN.word.capitalize()
        generating = True
        nextWN = initialWN
        termMod = 0.01
        while (generating):
            nextWN = nextWN.getNextNode()
            if (nextWN == None):
                fullMsg += "."
                return fullMsg
            termProb = nextWN.terminalCount / nextWN.instances
            if (termProb + termMod > random.random()):
                fullMsg += "."
                return fullMsg
            else:
                fullMsg += " "
                fullMsg += nextWN.word
                termMod += 0.01

    def simulateAll(self):
        for user in self.userGraphs:
            print(user + ": " + self.simulateSentence(user))
