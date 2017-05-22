import random
import time
from GAMENEW import Game,Dir
import numpy as np
from pybrain.structure import FeedForwardNetwork
from pybrain.structure.modules.linearlayer import LinearLayer
from pybrain.structure.modules.sigmoidlayer import SigmoidLayer
from pybrain.structure.connections.full import FullConnection
from numpy import average
from _ast import Param

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
    
    for i in range(populationSize):
        paramSet=[]
        for j in range(len(net.params)):
            paramSet.append(random.uniform(-10,10))
        population.insert(i, paramSet)
    return population

def selection(population):
    
    averageScores=[]
    selectedIndividuals = []
    bestAverages=[]
    for i in range(len(population)):
        scores = [] 
        net._setParameters(population[i])
        for j in range(gamesPerIndividual):
            sc = game.runGame(play)
            scores.append(sc)
        averageScores.append(sum(scores)/len(scores))
    for i in range(selectedIndividualSize):
        selectedIndividuals.append(population[averageScores.index(max(averageScores))])
        bestAverages.append(max(averageScores))
        averageScores.pop(averageScores.index(max(averageScores)))
    print sum(bestAverages)/len(bestAverages)
    return selectedIndividuals
    
def crossover(selectedIndividuals): 
    newPopulation = []
    
    for i in range(populationSize-selectedIndividualSize):
        parent1 = selectedIndividuals[random.randint(0,len(selectedIndividuals)-1)]
        parent2 = selectedIndividuals[random.randint(0,len(selectedIndividuals)-1)]
        child = parent1[len(parent1)/2:]+parent2[:len(parent2)/2]
        newPopulation.append(child)
    if np.random.random() < mutationChance:
        newPopulation = mutate(newPopulation)
    for entry in selectedIndividuals:
        newPopulation.append(entry)
    return newPopulation


def mutate(population):
    print "Mutation occurred!"
    mutationLoc= random.randint(0,len(population)-1)
    mutatingIndividual=population[mutationLoc]
    for i in range(len(mutatingIndividual)):
        mutatingIndividual.insert(i, random.uniform(-10,10))
    population[mutationLoc] = mutatingIndividual
    return population

def doGenetic(population):

    newPopulation = population    
    for i in range(generationCount):
        time0= time.time()
        selectedIndividuals = selection(newPopulation)
        newPopulation = crossover(selectedIndividuals)
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
populationSize = 100 #Anzahl der Individuuen
selectedIndividualSize = populationSize/5 #Anzahl an indiviuen, die an die naechste Generation weitergegeben wird
gamesPerIndividual = 20 #Anzahl Spiele per Individuum um Fitness zu bestimmen (10-50 max.)
generationCount = 100 #Anzahl an Generationen
mutationChance = 0.05 #Chance des Mutierens eines Individuums

game = Game(None,4,4)
population = buildPopulation()
ultimateParams = doGenetic(population)

print ultimateParams
paramFile = open("Best_Parameters.txt","w")
paramFile.write(ultimateParams)
paramFile.close()


