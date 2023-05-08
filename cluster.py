from numpy import genfromtxt
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd

import glob
import os


'''
bring in all the csvs of the unlabeled nets, cluster the data
bring in all csvs of the labeled nets, cluster them, manually analyze the clustering results
maybe scatter plot with matplot if you have time
'''

def gen_elbow(values):
    wcss = []

    for k in range(1,21):
        km = KMeans(n_clusters=k, random_state=42, max_iter=5000, init = 'k-means++')
        km.fit(values)
        wcss.append(km.inertia_)

    wcss = pd.DataFrame(wcss, columns=['Value'])
    wcss.index += 1

    plot = px.line(wcss)
    plot.update_layout(
        title={'text': "Within Cluster Sum of Squares or 'Elbow Chart'",
            'xanchor': 'center',
            'yanchor': 'top',
            'x': 0.5},
        xaxis_title='Clusters',
        yaxis_title='WCSS')
    plot.update_layout(showlegend=False)
    plot.show()

net_csvs = ['s27.csv','s382.csv','s420.csv','s641.csv']
Xs = np.empty((1,9))


path = 'parsed_nets/real/'
all_files = glob.glob(os.path.join(path, "*.csv"))
df = pd.concat((pd.read_csv(f) for f in all_files), ignore_index=True)

print(df)

for csv in net_csvs:
    X = genfromtxt('parsed_nets/' + csv, delimiter=',')

    X = np.delete(X, 0, 0)

    #print(X)

    X = [row[~np.isnan(row)] for row in X]

    X = np.array(X)

    Xs = np.concatenate((Xs, X), axis=0)


Xs = np.delete(Xs, (0), axis=0)

print(Xs)

#gen_elbow(Xs)

km = KMeans(n_clusters=6, random_state=42, max_iter=5000, init = 'k-means++')
clusters = km.fit_predict(Xs)

labels = pd.DataFrame({'Cluster': clusters})
labeledDF = pd.concat((df, labels), axis=1)
labeledDF['Cluster'] = labeledDF['Cluster'].astype(str)

u_labels = np.unique(clusters)
 
for i in u_labels:
    plt.scatter(df[clusters == i , 'FanIn L1'] , df[clusters == i , 'FanOut L1'] , label = i)
plt.legend()
plt.show()

'''
plot = px.scatter(labeledDF, color="Cluster")
plot.update_yaxes(categoryorder='category ascending')
plot.update_layout(
    title={'text': "Clustered Data",
           'xanchor': 'center',
           'yanchor': 'top',
           'x': 0.5})
plot.show()
'''


#print(np.shape(Xs))
#print(len(km.labels_))

'''
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
'''