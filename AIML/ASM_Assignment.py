from ad import *

def convnet(x):
#initialise parameters and inputs
    def relu(u):
        return max(dual(0,0),u)
# x as list of five numerical inputs
    x1, x2, x3, x4, x5 = [dual(val, 0) for val in x]
    w1 = dual(1.2, 1)
    w2 = dual(-0.2,0)
    v1 = dual(-0.3, 0)
    v2 = dual(0.6, 0)
    v3 = dual(1.3, 0)
    v4 = dual(-1.5, 0)
# compute inputs of hidden layer and apply ReLU
    z1 = relu(w1*x1 + w2*x2)
    z2 = relu(w1*x2 + w2*x3)
    z3 = relu(w1*x3 + w2*x4)
    z4 = relu(w1*x4 + w2*x5)
# initiate z as a list to be returned
    z = [z1, z2, z3, z4]
# apply ReLU function to output layer
    y = relu(v1 * z1 + v2 * z2 + v3 * z3 + z4 *v4)
    return y , z
