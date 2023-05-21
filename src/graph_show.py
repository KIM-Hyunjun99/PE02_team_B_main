import xml.etree.ElementTree as elemTree
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import os
from lmfit import Model
import warnings
import pandas as pd
import graph_individual as gi
import produce_csv as pc

def graph(x):
    insert = x
    data_elements = []
    graph_elements = []

    for element in insert:
        if isinstance(element, list) or isinstance(element, tuple):
            data_elements.append(element)
        else:
            graph_elements.append(element)

    k = len(graph_elements)

    def graph_saving(x):
        if not os.path.exists("../res/" + data_elements[x][0] +'/'+data_elements[x][1]+'/'+data_elements[x][2]):
            os.makedirs("../res/" + data_elements[x][0] +'/'+data_elements[x][1]+'/'+data_elements[x][2])
        if k == 5:
            plt.savefig('../res/' + data_elements[x][0] +'/'+data_elements[x][1]+'/'+data_elements[x][2]+'/'+'{}.{}.{}.{}'.format(*data_elements[x]) + '.png')
        else:
            plt.savefig('../res/' + data_elements[x][0] +'/'+data_elements[x][1]+'/'+data_elements[x][2]+'/'+'{}.{}.{}.{}'.format(*data_elements[x]) + str({",".join(graph_elements)}) + '.png')
    def graph_select(x,y):
        if graph_elements[x] == 'IV':
            gi.IV_graph_plot(*data_elements[y])
        elif graph_elements[x] == 'TR':
            gi.transmission_spectra(*data_elements[y])
        elif graph_elements[x] == 'Ref_fit':
            gi.transmission_rsquare(*data_elements[y])
        elif graph_elements[x] == 'flat1':
            gi.intensity_spectra(*data_elements[y])
        elif graph_elements[x] == 'flat2':
            gi.del_n_eff_voltage(*data_elements[y])

    for i in range(0,len(data_elements)):

        if k == 1:
            plt.clf()
            graph_select(0,i)
            graph_saving(i)

        elif k == 2:
            plt.clf()
            plt.subplot(1,2,1)
            graph_select(0,i)
            plt.subplot(1,2,2)
            graph_select(1,i)
            graph_saving(i)

        elif k == 3:
            plt.clf()
            plt.subplot(1,3,1)
            graph_select(0,i)
            plt.subplot(1,3,2)
            graph_select(1,i)
            plt.subplot(1, 3, 3)
            graph_select(2, i)
            graph_saving(i)

        elif k == 4:
            plt.clf()
            plt.subplot(2,2,1)
            graph_select(0,i)
            plt.subplot(2,2,2)
            graph_select(1,i)
            plt.subplot(2,2,3)
            graph_select(2,i)
            plt.subplot(2,2,4)
            graph_select(3,i)
            graph_saving(i)

        elif k == 5:
            plt.clf()
            plt.subplot(2, 3, 1)
            graph_select(0, i)
            plt.subplot(2, 3, 2)
            graph_select(1, i)
            plt.subplot(2, 3, 3)
            graph_select(2, i)
            plt.subplot(2, 3, 4)
            graph_select(3, i)
            plt.subplot(2, 3, 5)
            graph_select(4, i)
            graph_saving(i)