from string import punctuation, whitespace
import re
import numpy as np
import scipy as sp
from random import random
from operator import itemgetter

"""
instances: # of times a word has appeared
initialCount: # of times word has been first in sentence
terminalCount: # of times word has terminated a sentence
word: The word itself
edgeList: {Word: String of the word, (WordNode:Connected word, Value:# of times connected)}
"""
class WordNode:
    def __init__(self, word, initial=False, terminal=False):
        self.instances = 0
        self.terminalCount = 0
        self.word = word
        self.edgeList = {}
        self.edges = 0
        if (terminal):
            self.terminalCount = 1

    def updateNode(self, nextWN=None):
        self.instances += 1
        if (nextWN == None):
            self.terminalCount += 1
        else:
            if (nextWN.word == self.word):
                #print("Skipped word due to loop possibility")
                return
            self.edges += 1
            if (nextWN.word in self.edgeList):
                count = self.edgeList[nextWN.word][1]
                self.edgeList[nextWN.word] = (nextWN, count + 1)
            else:
                self.edgeList[nextWN.word] = (nextWN, 1)

    """
    If None is returned, the sentence has terminated and no next was returned
    """
    def getNextNode(self):
        if (self.edges == 0):
            #print(self.word + " has 0 edges")
            return None
        elList = list(self.edgeList.items())
        wordArr = list(map(itemgetter(0), elList))
        valArr = list(map(itemgetter(1), elList))
        countArr = list(map(itemgetter(1), valArr))
        edgeArr = np.array([wordArr, countArr])
        edgeProb = edgeArr[1, :].astype(float)
        edgeProb /= self.edges
        chosen = np.random.choice(edgeArr[0, :], p=edgeProb)
        return self.edgeList[chosen][0]

"""
nodes: {word:String of the word, WordNode:Associated Node}
"""
class Graph:
    def __init__(self, user):
        self.user = user
        self.initial = {}
        self.initialCount = 0
        self.nodes = {}
        self.total = 0

    def updateGraphNode(self, word, terminal, nextWord=""):
        if (word in self.nodes):
            if ((nextWord in self.nodes)):
                self.nodes[word].updateNode(self.nodes[nextWord])
            elif (nextWord == ""):
                self.nodes[word].updateNode()
            else:
                self.nodes[nextWord] = WordNode(nextWord, terminal=terminal)
                self.nodes[word].updateNode(self.nodes[nextWord])
        else: #Word has not been encountered, so it does not exist as a WordNode
            self.nodes[word] = WordNode(word, terminal=terminal)
            if ((nextWord in self.nodes)):
                self.nodes[word].updateNode(self.nodes[nextWord])
            elif (nextWord == ""):
                self.nodes[word].updateNode()
            else:
                self.nodes[nextWord] = WordNode(nextWord, terminal=terminal)
                self.nodes[word].updateNode(self.nodes[nextWord])

    def updateInitial(self, word):
        self.initialCount += 1
        if (word in self.initial):
            self.initial[word] += 1
        else:
            self.initial[word] = 1

    def processSentence(self, sentence):
        sentence = sentence.lower()
        sentence = sentence.split(" ")
        if (len(sentence) == 0):
            return

        for idx in range(len(sentence)):
            sentence[idx] = sentence[idx].strip(punctuation)
            sentence[idx] = re.sub(r"\s+", "", sentence[idx], flags=re.UNICODE)

        sentence = list(filter(len, sentence))

        senLen = len(sentence)
        self.total += senLen

        if (senLen == 0):
            return
        elif (senLen == 1):
            self.updateInitial(sentence[0])
            self.updateGraphNode(sentence[0], True)
        elif (senLen == 2):
            self.updateInitial(sentence[0])
            self.updateGraphNode(sentence[0], False, sentence[1])
            self.updateGraphNode(sentence[1], True)
        else:
            self.updateInitial(sentence[0])
            self.updateGraphNode(sentence[0], False, sentence[1])
            for idx in range(1, senLen - 1):
                self.updateGraphNode(sentence[idx], False, sentence[idx + 1])
            self.updateGraphNode(sentence[senLen - 1], True)

    def getInitial(self):
        initialArr = np.array(list(self.initial.items()))
        transProb = initialArr[:, 1].astype(float)
        transProb /= self.initialCount
        word = np.random.choice(initialArr[:, 0], p=transProb)
        return self.nodes[word]
