from pybrain.structure.networks import FeedForwardNetwork
from pybrain.structure.modules import LinearLayer, SigmoidLayer
from pybrain.structure.connections import FullConnection
from GAMELOGIC import Dir
import pickle

def createNetwork():
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
    
    return net

def load_best_individual():
    with open('best_individual.pkl', 'rb') as inp:
        # load individual
        individual = pickle.load(inp)
    return individual

# rectifies a value between 0 and 1
def rectify(value):
    return (0, 1)[value <= 0.5]

def do_turn(net, gamefield):
    field_arr = gamefield
    out1, out2 = map(rectify, net.activate(field_arr))

    if out1 and out2:
        return Dir.NORTH
    elif not out1 and out2:
        return Dir.EAST
    elif out1 and not out2:
        return Dir.WEST
    else:
        return Dir.SOUTH

net = createNetwork()
net._setParameters(load_best_individual())

def moveNN(gamefield):
    return do_turn(net, gamefield.getAs1DArray())
# print(game.runGame(net.activate))