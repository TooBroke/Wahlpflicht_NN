import random
import pickle
import os.path
import operator
import time
import numpy as np

from pybrain.structure.networks import FeedForwardNetwork
from pybrain.structure.modules import LinearLayer, SigmoidLayer
from pybrain.structure.connections import FullConnection
from GAMENEW import Dir, Game

# constants
POPULATION_SIZE = 50
INDIVIDUALS_TO_KEEP = 20
MUTATED_BEST = 5
FITNESS_ITERATIONS = 50
MUTATE_INDIVIDUAL_CHANCE = 0.65
MUTATE_WEIGHT_CHANCE = 0.3
TEXT_SPACER = '-'*40

# rectifies a value between 0 and 1
def rectify(value):
    return (0, 1)[value <= 0.5]

# function that is used to determine the next move
def do_turn():
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

# evaluates the fitness of an individual
def get_fitness(individual):
    net._setParameters(individual)
    score_sum = 0
    for i in range(FITNESS_ITERATIONS):
        score_sum += game.runGame(do_turn)
    return score_sum/FITNESS_ITERATIONS

# creates two crossover childs from two individuals
def get_crossovers(indi1, indi2):
    # create list from ndarray
    indi1 = indi1.tolist()
    indi2 = indi2.tolist()

    # crossover 1
    cross1 = indi1[::2]+indi2[1::2]
    cross1[::2] = indi1[::2]
    cross1[1::2] = indi2[1::2]
    # mutate crossover 1 by random
    if random.random() < MUTATE_INDIVIDUAL_CHANCE:
        cross1 = mutate(cross1)

    # crossover 2
    cross2 = indi1[1::2]+indi2[::2]
    cross2[1::2] = indi1[1::2]
    cross2[::2] = indi2[::2]
    # mutate crossover 2 by random
    if random.random() < MUTATE_INDIVIDUAL_CHANCE:
        cross2 = mutate(cross2)

    return np.asarray(cross1), np.asarray(cross2)

# mutates an individual by randomly inserting random weights
def mutate(indi):
    for i in range(len(indi)):
        if random.random() < MUTATE_WEIGHT_CHANCE:
            # insert random weight
            indi[i] = random.uniform(-10, 10)
    return indi

# creates a population with random weights
def create_population():
    pop_list = []
    for i in range(POPULATION_SIZE):
        # create network with random weights
        net.randomize()
        pop_list.append((get_fitness(net.params), net.params))
    return pop_list

# saves a population to a pickle file
def save_population(gen_number, pop_list):
    with open('population.pkl', 'wb') as output:
        # save generation number
        pickle.dump(gen_number, output, pickle.HIGHEST_PROTOCOL)
        # save each individual
        for i in pop_list:
            # save individual
            pickle.dump(i[1], output, pickle.HIGHEST_PROTOCOL)

# loads a population from a pickle file
def load_population():
    pop_list = []
    with open('population.pkl', 'rb') as inp:
        # load generation number
        gen_number = pickle.load(inp)
        # load each individual
        for i in range(POPULATION_SIZE):
            individual = pickle.load(inp)
            pop_list.append((get_fitness(individual), individual))
    return pop_list, gen_number

# saves an individual to a pickle file
def save_best_individual(individual):
    with open('best_individual.pkl', 'wb') as output:
        # save individual
        pickle.dump(individual, output, pickle.HIGHEST_PROTOCOL)

# loads an individual from a pickle file
def load_best_individual():
    with open('best_individual.pkl', 'rb') as inp:
        # load individual
        individual = pickle.load(inp)
    return individual

# create network and layers
net = FeedForwardNetwork()
in_layer = LinearLayer(16)
hid1_layer = SigmoidLayer(20)
hid2_layer = SigmoidLayer(20)
out_layer = SigmoidLayer(2)

# add layers to network
net.addInputModule(in_layer)
net.addModule(hid1_layer)
net.addModule(hid2_layer)
net.addOutputModule(out_layer)

# create connections between layers
in_to_hid1 = FullConnection(in_layer, hid1_layer)
hid1_to_hid2 = FullConnection(hid1_layer, hid2_layer)
hid2_to_out = FullConnection(hid2_layer, out_layer)

# add connections to network
net.addConnection(in_to_hid1)
net.addConnection(hid1_to_hid2)
net.addConnection(hid2_to_out)

# sort modules
net.sortModules()

# set up game
game = Game(None, 4, 4)
generation_number = 1
amount_of_generations = 0
population = []
time_spent = ''
best_individual = []
best_individual_fitness = 0

print TEXT_SPACER
print '2048 NN genetic algorithm training'

# load population if population file exists
print TEXT_SPACER
if os.path.isfile('population.pkl'):
    print 'Loading population from population file...'
    population, generation_number = load_population()
else:
    print 'Populaton file not found. Generating new population...'
    start_time = time.time()
    population = create_population()
    time_spent = str(int(time.time() - start_time))+'s'
    save_population(generation_number, population)
# sort population by fitness
population.sort(key=operator.itemgetter(0), reverse=True)

# load best individual if best individual file exists
if os.path.isfile('best_individual.pkl'):
    best_individual = load_best_individual()
    best_individual_fitness = get_fitness(best_individual)
else:
    best_individual = population[0][1]
    best_individual_fitness = population[0][0]
    save_best_individual(best_individual)

# determine how many generations shall be created
while amount_of_generations == 0:
    print TEXT_SPACER
    print 'How many generations shall be created?'
    try:
        temp_amount = int(raw_input("Amount: "))
        if temp_amount < 1:
            raise ValueError()
    except ValueError:
        print 'Invalid input, please insert a number above 0.'
    else:
        amount_of_generations = temp_amount

# start training
print TEXT_SPACER
print 'Training started.'
print TEXT_SPACER
print '{:^10s} | {:^10s} | {:^10s}'.format('gen. number', 'max. fitness', 'time spent')
for i in range(amount_of_generations):
    # start generating new generation
    start_time = time.time()
    generation_number += 1
    # replace individual 21 to 40 with crossovers of the first 20 individuals
    for j in range(0, INDIVIDUALS_TO_KEEP, 2):
        cross1, cross2 = get_crossovers(population[j][1], population[j+1][1])
        population[INDIVIDUALS_TO_KEEP+j] = (get_fitness(cross1), cross1)
        population[INDIVIDUALS_TO_KEEP+j+1] = (get_fitness(cross2), cross2)
    # replace individual 41 to 50 with mutated versions of the 2 best individuals
    for j in range(MUTATED_BEST):
        mutated1 = mutate(population[0][1])
        mutated2 = mutate(population[1][1])
        population[(INDIVIDUALS_TO_KEEP*2)+j] = (get_fitness(mutated1), mutated1)
        population[(INDIVIDUALS_TO_KEEP*2)+MUTATED_BEST+j] = (get_fitness(mutated2), mutated2)
    time_spent = str(int(time.time() - start_time))+'s'
    # sort population by fitness
    population.sort(key=operator.itemgetter(0), reverse=True)
    # save population
    save_population(generation_number, population)
    # save best individual if there is one better
    if population[0][0] > best_individual_fitness:
        best_individual = population[0][1]
        best_individual_fitness = population[0][0]
        save_best_individual(best_individual)
    # print training information
    max_fitness = population[0][0]
    print '{:^11d} | {:^12d} | {:^10s}'.format(generation_number, max_fitness, time_spent)
    print ''.join(str(i[0])+' ' for i in population)
print TEXT_SPACER
print 'Training finished.'