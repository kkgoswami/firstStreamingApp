from sgd import learn_coefficients
import numpy as np

print("Learning the coefficients for a single variable equation:")
print("True equation x = 2, input X = [1,1,1,1,1,1,1,1,1,1]")


X = np.array([[1,1,1,1,1,1,1,1,1,1]]).transpose()
y = np.array([[2,2,2,2,2,2,2,2,2,2]]).transpose()


print learn_coefficients(X, y, 0.01, 100)


print("Learning the coefficients for multiple variables:")
print("True equation 2x + 3y = 5");

X = np.array([[1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1]]).transpose()
y = np.array([[5,5,5,5,5,5,5,5,5,5]]).transpose();

print learn_coefficients(X, y, 0.01, 100)
