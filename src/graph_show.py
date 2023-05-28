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
from tqdm import tqdm

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
        for file_name in os.listdir(os.path.join('../dat', data_elements[x][0], data_elements[x][1], data_elements[x][2])):
            if data_elements[x][3] in file_name and 'LMZ' in file_name:
                if not os.path.exists("../res/" + data_elements[x][0] +'/'+data_elements[x][1]+'/'+data_elements[x][2]):
                    os.makedirs("../res/" + data_elements[x][0] +'/'+data_elements[x][1]+'/'+data_elements[x][2])
                if k == 5:
                    plt.savefig('../res/' + data_elements[x][0] +'/'+data_elements[x][1]+'/'+data_elements[x][2]+'/'+ file_name + '.png', dpi = 300)
                else:
                    plt.savefig('../res/' + data_elements[x][0] +'/'+data_elements[x][1]+'/'+data_elements[x][2]+'/'+ file_name + str({",".join(graph_elements)}) + '.png', dpi = 300)
    def graph_select(x,y): # 'IV', 'TR', 'Flat_TR', 'Intensity_fit','Enlarged_TR_fit','Del_n_eff'
        if graph_elements[x] == 'IV':
            gi.IV_graph_plot(*data_elements[y])
        elif graph_elements[x] == 'TR':
            gi.transmission_spectra(*data_elements[y])
        elif graph_elements[x] == 'Flat_TR':
            gi.flat_TR_graph_plot(*data_elements[y])
        elif graph_elements[x] == 'Intensity_fit':
            gi.intensity_spectra(*data_elements[y])
        elif graph_elements[x] == 'Enlarged_TR_fit':
            gi.enlarged_fitted_TR_graph(*data_elements[y])
        elif graph_elements[x] == 'Del_n_eff':
            gi.del_n_eff_voltage(*data_elements[y])

        # tqdm 객체 생성
    progress_bar = tqdm(total=len(data_elements))

    for i in range(0,len(data_elements)):

        if k == 1:
            plt.clf()
            graph_select(0,i)
            graph_saving(i)
            plt.show()
        elif k == 2:
            plt.clf()
            plt.subplot(1,2,1)
            graph_select(0,i)
            plt.subplot(1,2,2)
            graph_select(1,i)
            plt.subplots_adjust(top=0.9, bottom=0.1, left=0.1, right=0.9, hspace=0.4, wspace=0.4)
            graph_saving(i)
            plt.show()
        elif k == 3:
            plt.clf()
            plt.subplot(1,3,1)
            graph_select(0,i)
            plt.subplot(1,3,2)
            graph_select(1,i)
            plt.subplot(1, 3, 3)
            graph_select(2, i)
            plt.subplots_adjust(top=0.9, bottom=0.1, left=0.1, right=0.9, hspace=0.4, wspace=0.4)
            graph_saving(i)
            plt.show()
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
            plt.subplots_adjust(top=0.9, bottom=0.1, left=0.1, right=0.9, hspace=0.4, wspace=0.4)
            graph_saving(i)
            plt.show()
        elif k == 5:
            plt.clf()
            fig = plt.figure(figsize=(16, 9))
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
            plt.subplots_adjust(top=0.9, bottom=0.1, left=0.1, right=0.9, hspace=0.4, wspace=0.4)
            graph_saving(i)
            plt.show()
        elif k == 6:
            plt.clf()
            fig = plt.figure(figsize=(16, 9))
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
            plt.subplot(2, 3, 6)
            graph_select(5, i)
            plt.subplots_adjust(top=0.9, bottom=0.1, left=0.1, right=0.9, hspace=0.4, wspace=0.4)
            graph_saving(i)
            plt.show()
        progress_bar.update(1)

    progress_bar.close()

