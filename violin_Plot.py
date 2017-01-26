import numpy as np
import random
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure,show
from scipy.stats import gaussian_kde
from numpy.random import normal
from numpy import arange
import csv
from sklearn import preprocessing

def violin_plot(ax,data,pos, bp=False):
    '''
    create violin plots on an axis
    '''
    dist = max(pos)-min(pos)
    w = min(0.15*max(dist,1.0),0.5)
    colorlabels={0 : 'y', 1 : 'r', 2 : 'b', 3 : 'g', 4 : 'm', 5 : 'k'}
    for d,p in zip(data,pos):
        k = gaussian_kde(d) #calculates the kernel density
        m = k.dataset.min() #lower bound of violin
        M = k.dataset.max() #upper bound of violin
        x = arange(m,M,(M-m)/100.) # support for violin
        v = k.evaluate(x) #violin profile (density curve)
        v = v/v.max()*w #scaling the violin to the available space
        ax.fill_betweenx(x,p,v+p,facecolor=colorlabels.get(p),alpha=0.3)
        ax.fill_betweenx(x,p,-v+p,facecolor=colorlabels.get(p),alpha=0.3)
        ax.get_xticklabels()
    if bp:
        ax.boxplot(data,notch=1,positions=pos,vert=1)


if __name__ == "__main__":
    ''' Define this range equivalent to the labels you have'''
    numlabel=7
    pos=range(7)
    LABELS=[]
    TIME=[]
    POINTS=[]
    labels = "Declare this variable as dictionary type and initialize it with your labels. See example below"
    '''labels={'Cannabis' : 1, 'Cannabis oil': 2, 'Edibles': 3, 'Marijuana concentrates': 4, 'Cannabis resin': 5, 'Synthetic cannabis': 6 }'''

    with open('Location of CSV File whose violin plot you need', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            if labels.get(row[2]) == None:
                continue
            else:
                LABELS.append(labels.get(row[2]))
                TIME.append(row[0])
                POINTS.append(row[1])
    data2=[]
    time=[]
    for j in range(7):
        x=[]
        t=[]
        for i in range(len(TIME)):
            if LABELS[i] == j:
                x.append(int(POINTS[i]))
                t.append((TIME[i].split('T')[0]))
        data2.append(x)
        time.append(t)
    mMscalar = preprocessing.MinMaxScaler()
    data=[mMscalar.fit_transform(np.asarray(data2[i], dtype='float64')) for i in range(1,numlabel)]
    print data
    fig=figure()
    ax=fig.add_subplot(111)
    ax.set_color_cycle(['red', 'black', 'yellow','cyan', 'magenta', 'pink'])
    ax.set_xticks([0,1,2,3,4,5])
    ax.set_xticklabels(['Mention your labels in list form here '])
    ax.set_ylabel('points')
    violin_plot(ax,data,pos,bp=0)
    show()