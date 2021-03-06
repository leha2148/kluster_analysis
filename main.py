# -*- coding: utf-8 -*-
from scipy.spatial.distance import cdist 
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.colors as pltc
import random

# get colors array
def get_cmap(n, name='hsv'):
    return plt.cm.get_cmap(name, n)

def read_datafile(file_name):
    data = pd.read_csv(file_name)
    return data


# read data from file into table
data = read_datafile('cars.csv')

klasses = np.unique(data['brand'])
print("klasses is ", klasses,len(klasses))

# create color palette
cmap = get_cmap(len(klasses)+1)

# create matrix of samples
X = np.zeros((261, 2))
X[:, 0] = data['hp']
X[:, 1] = data['cubicinches']

# show data
plt.plot(X[:, 0], X[:, 1], 'bo')
plt.show()


# set random centroids------------------------------------------------
np.random.seed(seed=48)

centroids = []
for i in range(len(klasses)):
    print([random.uniform(min(X[:, 0]), max(X[:, 0])),
           random.uniform(min(X[:, 1]), max(X[:, 1]))])

    centroids.append([random.uniform(min(X[:, 0]), max(X[:, 0])),
                      random.uniform(min(X[:, 1]), max(X[:, 1]))])
print(centroids)

centroids = np.asarray(centroids)

cent_history = []
cent_history.append(centroids)
# ----------------------------------------------------------------------
# plot with centerts
plt.plot(X[:, 0], X[:, 1], 'bo')

for j in range(len(klasses)):
    plt.scatter(cent_history[0][j, 0], cent_history[0][j, 1],s=220,c=cmap(j))

plt.show()


epsilon = 0.05
steps = 0

for i in range(100):
    steps = steps+1
    # Считаем расстояния от наблюдений до центроид
    distances = cdist(X, centroids)
    # Смотрим, до какой центроиде каждой точке ближе всего
    labels = distances.argmin(axis=1)

    # Положим в каждую новую центроиду геометрический центр её точек
    centroids = centroids.copy()

    for i in range(len(klasses)):
        centroids[i, :] = np.mean(X[labels == i, :], axis=0)

    cent_history.append(centroids)

    print("STEP NUMBER ", steps)
    print("centroids difference", cdist(cent_history[len(cent_history)-2], centroids))
    delta = cdist(cent_history[len(cent_history)-2], centroids)
    stop = True
    
    for i in range(len(delta)):
        if(delta[i, i] > epsilon):
            stop = False
        

    if(stop):
        break

# plot all steps
for i in range(steps):
    distances = cdist(X, cent_history[i])
    labels = distances.argmin(axis=1)

    #plt.subplot(2, 2, i + 1)
    for j in range(len(klasses)):
        
        plt.scatter(X[labels == j, 0], X[labels == j, 1],
                    c=cmap(j), label=('cluster #' + str(klasses[j])))
        plt.scatter(cent_history[i][j, 0], cent_history[i][j, 1],s=220,c=cmap(j))

    plt.legend(loc=0)

    
    print("i is",i)
    if(i == (steps-1)):
        plt.title('Step FINISH {:}'.format(i + 1))
    else:
        plt.title('Step {:}'.format(i + 1))

    plt.show()


raw_input("Press enter to continue")
