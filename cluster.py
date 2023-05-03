from numpy import genfromtxt
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


'''
bring in all the csvs of the unlabeled nets, cluster the data
bring in all csvs of the labeled nets, cluster them, manually analyze the clustering results
maybe scatter plot with matplot if you have time
'''

net_csvs = ['s27.csv','s382.csv','s420.csv','s641.csv','s713.csv','s1238.csv']
Xs = np.empty((1,10))

for csv in net_csvs:
    X = genfromtxt('parsed_nets/' + csv, delimiter=',')

    X = np.delete(X, 0, 0)

    #print(X)

    X = [row[~np.isnan(row)] for row in X]

    X = np.array(X)

    Xs = np.concatenate((Xs, X), axis=0)


Xs = np.delete(Xs, (0), axis=0)

print(Xs)

km = KMeans(n_clusters=3, init='k-means++', n_init=10, random_state=0).fit(Xs)

print(np.shape(Xs))
print(len(km.labels_))

labeled_csvs = ['c482.csv','c1980.csv','c6288.csv']
Ys = np.empty((1,10))

for csv in labeled_csvs:
    Y = genfromtxt('parsed_nets/' + csv, delimiter=',')

    Y = np.delete(Y, 0, 0)

    #print(X)

    Y = [row[~np.isnan(row)] for row in Y]

    Y = np.array(Y)

    Ys = np.concatenate((Ys, Y), axis=0)

Ys = np.delete(Ys, (0), axis=0)
print(np.shape(Ys))

res = km.predict(Ys)

print(res)


Zs = np.empty((1,11))
for csv in labeled_csvs:
    Z = genfromtxt('parsed_nets/labeled/' + csv, delimiter=',')

    Z = np.delete(Z, 0, 0)

    #print(X)

    Z = [row[~np.isnan(row)] for row in Z]

    Z = np.array(Z)

    Zs = np.concatenate((Zs, Z), axis=0)

Zs = np.delete(Zs, (0), axis=0)

FP = 0
FN = 0

i = 0

for net in Zs:
    if(net[10] != res[i]):
        if(net[10] == 0 and res[i] > 0):
            FP += 1
        elif(net[10] > 0 and res[i] == 0):
            FN += 1

    i += 1

print("False pos: " + str(FP))
print("False neg: " + str(FN))