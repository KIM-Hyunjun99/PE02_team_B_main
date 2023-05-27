import xml.etree.ElementTree as elemTree
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import os
from lmfit import Model
import warnings
import pandas as pd
import graph_individual as gi
import graph_show as gs
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
    default_list.append('Ref_fit')
    default_list.append('TR_fit')
    default_list.append('del_n_eff')

    gs.graph(default_list)
