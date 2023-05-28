import xml.etree.ElementTree as elemTree
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import os
from lmfit import Model
import warnings
import pandas as pd
import graph_individual as gi
from tqdm import tqdm
import time

def default():

    start_dir = os.path.join('..', 'dat')  # 제일 중요한 코드, '..'는 현재 디렉토리의 부모 디렉토리를 반환해주는 코드, 그걸 data_file과 연결
    file_paths = []  # 전체 파일 경로를 원소로 가지는 리스트 변수 초기화

    # dat 디렉토리와 그 하위 디렉토리를 순회하면서 파일 경로를 수집
    for dirpath, dirnames, filenames in os.walk(start_dir):
        for filename in filenames:
            if '_LMZ' in filename and filename.endswith('.xml'):
                file_paths.append(os.path.join(dirpath, filename))

    def convert_list(file_names):
        converted_list = []
        for file_name in file_names:
            lot_data = file_name.split('\\')[2]
            folder_name = file_name.split('\\')[3]
            timestamp = file_name.split('\\')[4]
            coordinates = file_name.split('\\')[-1].split('_')[2]
            converted_list.append((lot_data, folder_name, timestamp, coordinates))
        return converted_list

    default_list = convert_list(file_paths)
    default_list.append('IV')
    default_list.append('TR')
    default_list.append('Flat_TR')
    default_list.append('Intensity_fit')
    default_list.append('Enlarged_TR_fit')
    default_list.append('Del_n_eff')

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
            for file_name in os.listdir(
                    os.path.join('../dat', data_elements[x][0], data_elements[x][1], data_elements[x][2])):
                if data_elements[x][3] in file_name and 'LMZ' in file_name:
                    if not os.path.exists(
                            "../res/" + data_elements[x][0] + '/' + data_elements[x][1] + '/' + data_elements[x][2]):
                        os.makedirs(
                            "../res/" + data_elements[x][0] + '/' + data_elements[x][1] + '/' + data_elements[x][2])
                    if k == 5:
                        plt.savefig(
                            '../res/' + data_elements[x][0] + '/' + data_elements[x][1] + '/' + data_elements[x][2] + '/' + file_name + '.png', dpi=300)
                    else:
                        plt.savefig(
                            '../res/' + data_elements[x][0] + '/' + data_elements[x][1] + '/' + data_elements[x][2] + '/' + file_name + str({",".join(graph_elements)}) + '.png', dpi=300)
                    plt.close()
        def graph_select(x, y):
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

        for i in range(0, len(data_elements)):
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

            progress_bar.update(1)

        progress_bar.close()

    graph(default_list)

# default()
