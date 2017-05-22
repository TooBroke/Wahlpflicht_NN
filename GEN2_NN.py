import random
import time
from GAMENEW import Game,Dir
import numpy as np
from pybrain.structure import FeedForwardNetwork
from pybrain.structure.modules.linearlayer import LinearLayer
from pybrain.structure.modules.sigmoidlayer import SigmoidLayer
from pybrain.structure.connections.full import FullConnection
from numpy import average

def rectify(value):
    return (0, 1)[value <= 0.5]

def play():
    
    field_arr = game.gamefield.getAs1DArray()
    out1, out2 = map(rectify, net.activate(field_arr))

    if out1 and out2:
        return Dir.NORTH
    elif not out1 and out2:
        return Dir.EAST
    elif out1 and not out2:
        return Dir.WEST
    else:
        return Dir.SOUTH

def buildPopulation():
    population= []
    
    for i in range(100):
        paramSet=[]
        for j in range(len(net.params)):
            paramSet.append(random.uniform(-10,10))
        population.insert(i, paramSet)
    return population

def selection(population):
    
    averageScores=[]
    selectedIndividuals = []
    for i in range(len(population)):
        scores = [] 
        net._setParameters(population[i])
        for j in range(gamesPerIndividual):
            sc = game.runGame(play)
            scores.append(sc)
        averageScores.append(sum(scores)/len(scores))
    print sorted(averageScores, reverse = True)
    for i in range(20):
        selectedIndividuals.append(population[averageScores.index(max(averageScores))])
        averageScores.pop(averageScores.index(max(averageScores)))
    return selectedIndividuals
    
def crossover(selectedIndividuals): 
    newPopulation = []
    for entry in selectedIndividuals:
        newPopulation.append(entry)
    for i in range(80):
        parent1 = selectedIndividuals[random.randint(0,19)]
        parent2 = selectedIndividuals[random.randint(0,19)]
        child = parent1[len(parent1)/2:]+parent2[:len(parent2)/2]
        newPopulation.append(child)
    return newPopulation


def mutate(population):
    mutationLoc= random.randint(0,99)
    mutatingIndividual=population[mutationLoc]
    for i in range(len(mutatingIndividual)):
        mutatingIndividual.insert(i, random.uniform(-10,10))
    population.insert(mutationLoc, mutatingIndividual)
    return population

def doGenetic(population):

    newPopulation = population    
    for i in range(generationCount):
        time0= time.time()
        selectedIndividuals = selection(newPopulation)
        newPopulation = crossover(selectedIndividuals)
        if np.random.random() < mutationChance:
            newPopulation = mutate(newPopulation)
        time1 = time.time()
        print time1-time0
    finalSelection = selection(newPopulation)
    print "Doing final selection"
    finalAverages = []
    for individual in finalSelection:
        net._setParameters(individual)
        scores=[]
        for i in range(100):
            sc=game.runGame(play)
            scores.append(sc)
        finalAverages.append(sum(scores)/len(scores))
    
    print finalSelection
    fittestIndividual = finalSelection[finalAverages.index(max(finalAverages))]
    return fittestIndividual

net = FeedForwardNetwork()
inLayer = LinearLayer(16)
hiddenLayer = SigmoidLayer(10)
outLayer = SigmoidLayer(2)
net.addInputModule(inLayer)
net.addModule(hiddenLayer)
net.addOutputModule(outLayer)
in_to_hidden = FullConnection(inLayer, hiddenLayer)
hidden_to_out = FullConnection(hiddenLayer, outLayer)
net.addConnection(in_to_hidden)
net.addConnection(hidden_to_out)
net.sortModules()

'''Lernvariablen'''

gamesPerIndividual = 30 #Anzahl Spiele per Individuum um Fitness zu bestimmen (10-50 max.)
generationCount = 500 #Anzahl an Generationen
mutationChance = 0.2 #Chance des Mutierens eines Individuums

game = Game(None,4,4)
population = buildPopulation()
ultimateParams = doGenetic(population)


