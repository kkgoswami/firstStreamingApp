import numpy as np
#import pdb 
#pdb.set_trace()

def sgd(W, X, y, index, learning_rate, num_iterations):
    """
        This function works as the equation solver. It is essentially Stochastic
        Gradient descent, but works similar to a classifier. The weight update
        stops when the error is less than some epsilon.

        Overview: 

        Given an equation ax + by + cz + dw = l, given the values of x,y,z,w and
        l, learn the coefficients a,b,c and d. 
        
        Arguments: 

        X - A matrix with the size m x n, where m is the number of data points
        and n is either the number of classifiers/number of features depending
        on the application
        
        y - The column vector with the true labels. Only compatible with binary
        labels as of now. 

        W - A vector with n elements, each element corresponding to a particular
        weight. 

        index - the index of the weight which is to be updated. 

        learning_rate - the starting learning rate value for the gradient
        descent

        num_iterations - the number of times the weight needs to be updated

        X - a multidimensional numpy array
        W, y - a one dimensional numpy array 
        index - integer 
        learning_rate - real value
        num_iterations - integer

        Returns: 
        
        W' - The updated weight vector, with only the weight value updated as
        indicated by the index. That is, Only W[index] is changed, the other
        values in W remain constant. 
    """
    #decay_rate = 0.001
    epsilon = 0.0001
    num_points = X.shape[0]
    for j in xrange(0, num_iterations):
        for i in xrange(0, num_points):
            temp_output = linear_function(W, X[i])
            update_value = learning_rate * (temp_output - y[i]) * X[i][index]
            #print update_value
            W[index] -= update_value

    return W  
        

def l1_error(a,b):
    return abs(a-b)

def overall_error(W, X, y):
    pass
    

def linear_function(w,x):
    """
        The function ax + by + cz and returns the output l. 
          
        Arguments: 
        w, x - one dimensional vectors
        w is the set of coefficients 
        x is the set of data points

        returns: 
        l - the output of the function(dot product between the two vectors)
    """
    return np.dot(w,x)


def learn_coefficients(X, y, learning_rate, num_iterations):
    """
        Check which weight to update next. 
    """

    num_weights = X.shape[1]

    W = np.random.uniform(0, 1, num_weights)
    
    for i in xrange(num_weights):
        W = sgd(W, X, y, i, learning_rate, num_iterations)


    return W

