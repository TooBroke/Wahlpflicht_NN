import random
from GAMENEW import Game,Dir
import numpy as np
from pybrain.structure import FeedForwardNetwork
from pybrain.structure.modules.linearlayer import LinearLayer
from pybrain.structure.modules.sigmoidlayer import SigmoidLayer
from pybrain.structure.connections.full import FullConnection



def play():
    
    val= net.activate(game.gamefield.getAs1DArray())
    if val <= 0.1:     
        return Dir.NORTH
    elif val <=0.5:
        return Dir.EAST
    elif val <=0.9:
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
    scores = [] 
    selectedIndividuals = []
    for i in range(len(population)):
        net._setParameters(population[i])
        sc = game.runGame(play)
        scores.append(sc)
    for i in range(20):
        selectedIndividuals.append(population[scores.index(max(scores))])
        scores.pop(scores.index(max(scores)))
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
    mutationChance = 0.1
    newPopulation = population    
    for i in range(1000):
        selectedIndividuals = selection(newPopulation)
        print "Selection No.", i
        newPopulation = crossover(selectedIndividuals)
        print "Crossover No.",i
        if np.random.random() < mutationChance:
            print "mutation occurred"
            newPopulation = mutate(newPopulation)
    
    for individual in newPopulation:
        scores=[]
        net._setParameters(individual)
        for i in range(100):
            sc=game.runGame(play)
            scores.append(sc)
        print "Average: ", sum(scores)/len(scores)

net = FeedForwardNetwork()
inLayer = LinearLayer(16)
hiddenLayer = SigmoidLayer(10)
outLayer = SigmoidLayer(1)
net.addInputModule(inLayer)
net.addModule(hiddenLayer)
net.addOutputModule(outLayer)
in_to_hidden = FullConnection(inLayer, hiddenLayer)
hidden_to_out = FullConnection(hiddenLayer, outLayer)
net.addConnection(in_to_hidden)
net.addConnection(hidden_to_out)
net.sortModules()

game = Game(None,4,4)
population = buildPopulation()
doGenetic(population)


