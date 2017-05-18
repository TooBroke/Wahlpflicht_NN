import numpy as np
import pickle
import os
from pybrain.structure import FeedForwardNetwork, LinearLayer, SigmoidLayer, FullConnection
from GAMENEW import Dir, Game

net = FeedForwardNetwork()
in_layer = LinearLayer(16)
hid1_layer = SigmoidLayer(20)
hid2_layer = SigmoidLayer(20)
out_layer = SigmoidLayer(2)

net.addInputModule(in_layer)
net.addModule(hid1_layer)
net.addModule(hid2_layer)
net.addOutputModule(out_layer)

in_to_hid1 = FullConnection(in_layer, hid1_layer)
hid1_to_hid2 = FullConnection(hid1_layer, hid2_layer)
hid2_to_out = FullConnection(hid2_layer, out_layer)

net.addConnection(in_to_hid1)
net.addConnection(hid1_to_hid2)
net.addConnection(hid2_to_out)

net.sortModules()

def rectify(value):
    return (0, 1)[value <= 0.5]


def testalgo():
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

best_params = []
best_score = 0
game = Game(None, 4, 4)
running = False
amount = 100
while running:
    game.restart()
    score = 0
    for i in range(amount):
        score += game.runGame(testalgo)
    print score/amount
    if score/amount > best_score:
        print(score/amount)
        best_score = score/amount
        best_params = net.params
        with open('best_params.pkl', 'wb') as output:
            pickle.dump(net.params, output, pickle.HIGHEST_PROTOCOL)
    if score/amount > 100:
        running = False
    #if score > best_score:
    #    best_score = score
    #    best_params = net.params
    net.randomize()

#print "best score:", best_score

with open('best_params.pkl', 'rb') as inp:
    params = pickle.load(inp)
    net._setParameters(params)

results = [game.runGame(testalgo) for i in range(1000)]
print "average:", sum(results)/len(results)
print "max:", max(results)

#for i in range(10):
#    game.restart()
#    score = game.runGame(testTest)
#    print(score)
