from numpy import genfromtxt
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

X = genfromtxt('test.csv', delimiter=',')

X = np.delete(X, 0, 0)

#print(X)

X = [row[~np.isnan(row)] for row in X]

#print(X)

km = KMeans(n_clusters=3, init='k-means++', n_init=10, random_state=0)

y_km = km.fit_predict(X)

print(km.labels_)
