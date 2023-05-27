import xml.etree.ElementTree as elemTree
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import os
from lmfit import Model
import warnings
import pandas as pd
from tkinter import *
import math
import functions as func
import TR_graph_plot_edit

def IV_graph_plot(A, X, Y, Z):
    for file_name in os.listdir(os.path.join('../dat', A, X, Y)):
        if Z in file_name and 'LMZ' in file_name:
            tree = elemTree.parse(os.path.join('../dat', A, X, Y, file_name))
            root = tree.getroot()
        else:
            continue
    for i in root.iter('Current'):  # IV 데이터 parsing
        I = np.array(list(map(float, i.text.split(','))))
        I = abs(I)  # absolute value of Current data
    for i in root.iter('Voltage'):
        V = np.array(list(map(float, i.text.split(','))))

    plt.plot(V,func.shockely_diode_IV_fit(V,I), 'k--', label='best-fit')  # 근사 데이터 그래프 검은색 점선으로 plot
    plt.plot(V, I, 'ro', label='data')  # 측정 데이터 그래프 빨간색 점으로 plot
    plt.yscale('logit')  # y축 scale logit으로 지정)

    # 그래프 label, 디자인 설정
    plt.xlabel('Voltage[V]', labelpad=4, fontdict={'weight': 'bold', 'size': 7})
    plt.ylabel('Current[A]', labelpad=4, fontdict={'weight': 'bold', 'size': 7})
    plt.title('IV analysis', fontdict={'weight': 'bold', 'size': 10})
    plt.grid(True)  # 그리드 추가
    plt.legend(loc='upper left', fontsize=7)  # show legend
    plt.xticks(fontsize=6)  # modulate axis label's fontsize
    plt.yticks(fontsize=6)
    # show particular data using text method in mathplotlib library
    plt.text(0.02, 0.8, 'R_square = {:.15f}'.format(func.shockely_diode_IV_fit_R(V,I)), fontsize=6, transform=plt.gca().transAxes)
    plt.text(0.02, 0.75, '-1V = {:.12f}[A]'.format(I[4]), fontsize=6, transform=plt.gca().transAxes)
    plt.text(0.02, 0.7, '+1V = {:.12f}[A]'.format(I[12]), fontsize=6, transform=plt.gca().transAxes)
    # plt.gca().transAxes -> help set up the position of text(x: 0~1, y:0~1) 0 4 12
    plt.text(-2, I[0], '{:.11f}A'.format(I[0]), fontsize=6)  # y좌표에 1.5를 곱해주는 이유 = text가 점과 겹쳐서 보이기 때문에 1.5를 곱해 text 위치를 상향조정
    plt.text(-1, I[4], '{:.11f}[A]'.format(I[4]), fontsize=6)
    plt.text(0, I[12], '{:.11f}[A]'.format(I[12]), fontsize=6)


    return 0


def transmission_spectra(A, X, Y, Z):
    for file_name in os.listdir(os.path.join('../dat', A,  X, Y)):
        if Z in file_name and 'LMZ' in file_name:
            tree = elemTree.parse(os.path.join('../dat', A, X, Y, file_name))
            root = tree.getroot()
        else:
            continue
    v = []  # 빈 리스트 생성
    for waveLengthSweep in root.findall('.//WavelengthSweep'):  # WavelengthSweep 태그 찾기
        waveValues = []  # 빈 리스트 생성
        for child in waveLengthSweep:  # WavelengthSweep의 자식 태그들을 찾기
            waveValues.append(
                list(map(float, child.text.split(','))))  # 자식 태그의 텍스트를 ,로 split해서 리스트로 변환하고, 모든 요소를 float으로 변환
        waveValues.append(waveLengthSweep.attrib['DCBias'])  # DCBias를 waveValues 리스트의 마지막에 추가
        v.append(waveValues)  # waveValues 리스트를 v 리스트에 추가

    # Spectrum graph of raw data
    plots = []  # 빈 리스트 생성
    for i in range(len(v) - 1):  # v 리스트의 마지막 요소는 REF로 제외하고 반복
        line, = plt.plot(v[i][0], v[i][1], label=str(v[i][2]) + 'V')  # plot을 그리고, 레이블을 설정
        plots.append(line)  # plot을 plots 리스트에 추가

    line, = plt.plot(v[6][0], v[6][1], color='gray', label="REF")  # REF data plot

    plt.gca().add_artist(plt.legend(handles=[line], loc='upper right', fontsize=7))  # REF 레이블을 추가
    plt.legend(handles=plots, ncol=3, loc="lower left", fontsize=5)  # 나머지 레이블을 추가
    plt.title("Transmission spectra", fontdict={'weight': 'bold', 'size': 10})  # 그래프 제목을 설정
    plt.xticks(fontsize=6)  # modulate axis label's fontsize
    plt.yticks(fontsize=6)
    plt.xlabel('Wavelength [nm]', labelpad=4, fontdict={'weight': 'bold', 'size': 7})  # x축 레이블을 설정
    plt.ylabel('Measured transmission [dB]', labelpad=4, fontdict={'weight': 'bold', 'size': 7})  # y축 레이블을 설정

    return 0


def transmission_rsquare(A,X,Y,Z):
    for file_name in os.listdir(os.path.join('../dat', A, X, Y)):
        if Z in file_name and 'LMZ' in file_name:
            tree = elemTree.parse(os.path.join('../dat', A, X, Y, file_name))
            root = tree.getroot()
        else:
            continue
    v = []  # 빈 리스트 생성
    for waveLengthSweep in root.findall('.//WavelengthSweep'):  # WavelengthSweep 태그 찾기
        waveValues = []  # 빈 리스트 생성
        for child in waveLengthSweep:  # WavelengthSweep의 자식 태그들을 찾기
            waveValues.append(
                list(map(float, child.text.split(','))))  # 자식 태그의 텍스트를 ,로 split해서 리스트로 변환하고, 모든 요소를 float으로 변환
        waveValues.append(waveLengthSweep.attrib['DCBias'])  # DCBias를 waveValues 리스트의 마지막에 추가
        v.append(waveValues)  # waveValues 리스트를 v 리스트에 추가
    plots = []
    rs = []
    for i in range(1, 11):
        z = np.polyfit(v[6][0], v[6][1], i)
        p = np.poly1d(z)
        line, = plt.plot(v[6][0], p(v[6][0]), label=str(i) + 'deg')
        plots.append(line)
        a = np.array(v[6][0])
        b = np.array(v[6][1])
        rs1 = func.R_square(a, b, p(v[6][0]))
        rs.append(rs1)
    max_ind = rs.index(max(rs))

    a = list(a)
    b = list(b)
    maxwave = a[b.index(max(b))]
    minwave = a[b.index(min(b))]

    plt.text(0.2, 0.55, 'maximun wavelength = {:.4f}'.format(maxwave), fontsize=6, transform=plt.gca().transAxes)
    plt.text(0.2, 0.5, 'minimun wavelength = {:.4f}'.format(minwave), fontsize=6, transform=plt.gca().transAxes)
    if max_ind == 9:
        for i in range(-2,1):
            if i==0:
                plt.text(0.2, 0.45 + 0.05 * i, f'R\u00B2({max_ind + i + 1}deg)= {rs[max_ind + i]}', fontsize=5, transform=plt.gca().transAxes,color='red',weight='bold')
                continue
            plt.text(0.2, 0.45+0.05*i, f'R\u00B2({max_ind+i+1}deg)= {rs[max_ind+i]}', fontsize=5, transform=plt.gca().transAxes)
    else:
        for i in range(-1,2):
            if i==0:
                plt.text(0.2, 0.45 + 0.05 * (i-1), f'R\u00B2({max_ind + i + 1}deg)= {rs[max_ind + i]}', fontsize=5, transform=plt.gca().transAxes,color='red',weight='bold')
                continue
            plt.text(0.2, 0.45+0.05*(i-1), f'R\u00B2({max_ind+i+1}deg)= {rs[max_ind+i]}', fontsize=5, transform=plt.gca().transAxes)

    line, = plt.plot(v[6][0], v[6][1], color='gray', label="REF")
    plt.xticks(fontsize=6)  # modulate axis label's fontsize
    plt.yticks(fontsize=6)
    plt.xlabel('Wavelength [nm]', labelpad=4, fontdict={'weight': 'bold', 'size': 7})  # x축 레이블을 설정
    plt.ylabel('Measured transmission [dB]', labelpad=4, fontdict={'weight': 'bold', 'size': 7})  # y축 레이블을 설정
    plt.gca().add_artist(plt.legend(handles=[line], loc='upper right'))  # REF 레이블을 추가합니다.
    plt.legend(handles=plots, ncol=3, loc="lower left", fontsize=5)

    return 0

def intensity_spectra(A, X, Y, Z):
    test = TR_graph_plot_edit.plot_TR(A, X, Y, Z)
    test.data_parse()
    test.fitted_TR_graph_plot()

def del_n_eff_voltage(A, X, Y, Z):
    test = TR_graph_plot_edit.plot_TR(A, X, Y, Z)
    test.data_parse()
    test.del_n_eff_by_voltage()

# intensity_spectra('HY202103','D07','20190715_190855','(0,0)')
# del_n_eff_voltage('HY202103','D07','20190715_190855','(0,0)')
# plt.show()


