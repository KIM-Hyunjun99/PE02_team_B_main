import xml.etree.ElementTree as elemTree
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import os
from lmfit import Model
import warnings
import pandas as pd
from tkinter import *
from src import functions as fc
import math
from matplotlib.lines import Line2D
from scipy.signal import argrelextrema
from matplotlib.patches import Patch
warnings.filterwarnings('ignore',category=np.RankWarning)
class plot_TR:
    def __init__(self,Lot,Wafer,Date,Position):
        self.Lot = Lot
        self.Wafer = Wafer
        self.Date = Date
        self.Position = Position
        self.label_font_properties = {'size':7,'weight':'bold'}
        self.title_font_properties = {'size':10,'weight':'bold'}
        self.max_fit = []
        self.band_wave_len = 0
    def data_parse(self):
        self.wave_len = []
        self.wave_len_ref = np.array([])
        self.raw_trans = []
        self.minus_ref_trans = []
        self.minus_max_fit_trans = []
        wave_len_half = []
        trans_half = []
        self.trans_ref = np.array([])
        self.wave_len_max = []
        self.trans_max = []
        self.fit_trans_ref = []
        self.bias = []
        self.I = []
        # smoothed_trans = np.array([])
        temp1 = 0
        temp2 = 0

        path = os.path.join('dat',self.Lot ,self.Wafer, self.Date)
        self.file_name = [os.path.join(path, f) for f in os.listdir(path) if
                     'LMZ' in f and f.endswith('.xml') and self.Position in f]

        tree = elemTree.parse(self.file_name[0])
        root = tree.getroot()

        for modulator in root.iter('Modulator'):
            for WL_sweep in modulator.iter('WavelengthSweep'):
                if temp1 == 1:
                    self.wave_len_ref = np.append(self.wave_len_ref, np.array(list(map(float, WL_sweep.find('L').text.split(',')))))
                    self.trans_ref = np.append(self.trans_ref, np.array(list(map(float, WL_sweep.find('IL').text.split(',')))))
                    continue
                self.wave_len.append(list(map(float, WL_sweep.find('L').text.split(','))))
                self.raw_trans.append(list(map(float, WL_sweep.find('IL').text.split(','))))
                self.bias.append(float(WL_sweep.attrib['DCBias']))
                temp2 += 1
            temp1 += 1
        s = 150
        self.fit_trans_ref_real = fc.Ref_fitted_func(self.wave_len_ref, self.trans_ref)(self.wave_len_ref)
        for i in range(len(self.wave_len)):
            self.fit_trans_ref.append(fc.Ref_fitted_func(self.wave_len_ref, self.trans_ref)(self.wave_len[i]))
            self.minus_ref_trans.append([(x - y) for x,y in zip(self.raw_trans[i],self.fit_trans_ref[i])])
            # plt.plot(wave_len[i],trans[i])
            # print(len(self.minus_ref_trans[i][0]),len(self.wave_len[0]))
            trans_half_temp = []
            wave_len_half_temp = []
            for k in range(len(self.wave_len[i])):
                count = 0
                if k >= (len(self.wave_len[i]) - (s + 1)):
                    continue
                for g in range(1, (s + 1)):
                    if self.minus_ref_trans[i][k] > self.minus_ref_trans[i][k + g]:
                        count += 1
                if count >= s - 3:
                    trans_half_temp.append(self.minus_ref_trans[i][k])
                    wave_len_half_temp.append(self.wave_len[i][k])
            wave_len_half.append(wave_len_half_temp)
            trans_half.append(trans_half_temp)
            # plt.plot(wave_len_half[i],trans_half[i],'ro',markersize=0.5)#######
        # plt.show()

        for i in range(len(wave_len_half)):
            wave_len_max_temp = []
            trans_max_temp = []
            for j in range(len(wave_len_half[i])):
                if j == 0:
                    wave_len_max_temp.append(wave_len_half[i][j])
                    trans_max_temp.append(trans_half[i][j])
                    continue
                elif j >= len(wave_len_half[i]) - 4:
                    continue
                if (wave_len_half[i][j + 2] - wave_len_half[i][j + 1]) >= (
                        wave_len_half[i][j + 1] - wave_len_half[i][j] + 4):
                    wave_len_max_temp.append(wave_len_half[i][j + 2])
                    trans_max_temp.append(trans_half[i][j + 2])

            if trans_max_temp[0] < trans_max_temp[1] + 0.5:
                self.wave_len_max.append(wave_len_max_temp[1:])
                self.trans_max.append(trans_max_temp[1:])
            else:
                self.wave_len_max.append(wave_len_max_temp)
                self.trans_max.append(trans_max_temp)

            # print(wave_len_max_temp,trans_max_temp)
            # plt.plot(wave_len_max[i],trans_max[i],'ro')
            # plt.plot(wave_len[i],fc.flat_fit_function(np.array(wave_len_max[i]), np.array(trans_max[i]))(wave_len[i]))
            self.max_fit.append(fc.flat_fit_function(np.array(self.wave_len_max[i]), np.array(self.trans_max[i]))(self.wave_len[i]))
            self.minus_max_fit_trans.append([x-y for x,y in zip(self.minus_ref_trans[i],self.max_fit[i])])  # flatten 한 데이터들로 다시 trans 변수를 할당
            # plt.plot(wave_len[i],trans[i],'b-')
            self.I.append([10 ** (x / 10) / 1000 for x in self.minus_max_fit_trans[i]])
        # print(I)
        # for i in range(temp2):
        #     plt.plot(self.wave_len[i],self.I[i],marker='o',alpha=0.4,markersize=1)
        # 극댓값 정보를 찾기 -> 여러개 시도
        # print(I[bias.index(0.0)], wave_len[bias.index(0.0)])
        # print(bias)

        self.R_square_TR = []
        self.del_n_eff = []
        self.fitted_TR_data = []
        self.fit_raw_TR = []
        result_n_eff = fc.Transmission_fitting_n_eff(self.wave_len, self.I, self.bias)
        self.n_eff = result_n_eff[0]
        for bia in self.bias:
            if bia == 0.0:
                self.del_n_eff.append(0.0)
                self.fitted_TR_data.append(result_n_eff[1])
                continue
            result_del_n_eff = fc.Transmission_fitting_n_eff_V(self.wave_len, self.I, self.n_eff, self.bias, bia)
            self.del_n_eff.append(result_del_n_eff[0])
            self.fitted_TR_data.append(result_del_n_eff[1])
            # plt.plot(self.wave_len[self.bias.index(bia)],self.fitted_TR_data[self.bias.index(bia)],linestyle='dashed')
        self.colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
        self.colors = self.colors[:len(self.bias)]
        self.legend_name = [bia for bia in [str(bia_s) + '[V]' for bia_s in self.bias]]
        self.legend_elements = [Patch(facecolor=color, edgecolor=color, label=label, linewidth=0.01) for color, label in
                                zip(self.colors, self.legend_name)]

        self.ref_index = self.bias.index(0.0)
        self.minimum = fc.find_minimum_index(self.wave_len[self.ref_index], self.raw_trans[self.ref_index])
        self.minimum_wave_len = [self.wave_len[self.ref_index][i] for i in self.minimum]
        self.index_range = int(
            (self.wave_len[0].index(self.wave_len_max[0][1]) - self.wave_len[0].index(self.wave_len_max[0][0])) / 4)
        if 'LMZC' in self.file_name[0]:
            self.band_wave_len = 1550
            self.ref_wave_len_index = self.wave_len[self.ref_index].index(fc.closest_data(1550, self.minimum_wave_len))
        elif 'LMZO' in self.file_name[0]:
            self.band_wave_len = 1310
            self.ref_wave_len_index = self.wave_len[self.ref_index].index(fc.closest_data(1310, self.minimum_wave_len))
        for bia in self.bias:
            i = self.bias.index(bia)
            dB_fitted_TR_data = 10 * np.log10([data * 1000 for data in self.fitted_TR_data[i]])
            self.fit_raw_TR.append([x + y + z for x, y, z in zip(dB_fitted_TR_data[(self.ref_wave_len_index - self.index_range):(self.ref_wave_len_index + self.index_range)],self.max_fit[i][(self.ref_wave_len_index - self.index_range):(self.ref_wave_len_index + self.index_range)],self.fit_trans_ref[i][
                            (self.ref_wave_len_index - self.index_range):(self.ref_wave_len_index + self.index_range)])])
            self.R_square_TR.append(fc.R_square(np.array(self.wave_len[i][(self.ref_wave_len_index - self.index_range):(self.ref_wave_len_index + self.index_range)]), np.array(self.raw_trans[i][(self.ref_wave_len_index - self.index_range):(
                                    self.ref_wave_len_index + self.index_range)]),np.array(self.fit_raw_TR[i])))
        self.R_square_TR = np.mean(np.array(self.R_square_TR))
        self.V_piL = self.band_wave_len*10**(-9)/(self.del_n_eff[self.bias.index(-2)])

    def flat_TR_graph_plot(self):
        x_list = [self.wave_len,self.wave_len_max,self.wave_len]
        rep_len = len(self.bias)
        y_data_type1 = [self.minus_max_fit_trans[i] for i in range(rep_len)]
        y_data_type2 = [self.trans_max[i] for i in range(rep_len)]
        y_data_type3 = [self.max_fit[i] for i in range(rep_len)]
        y_data_type4 = [self.fitted_TR_data[i] for i in range(rep_len)]
        # dB_fitted_TR_data = 10 * np.log10([data * 1000 for data in self.fitted_TR_data[i]])
        labels = ['fit_ref','max_data','fit_flat_TR']

        for y,color in zip(y_data_type1, self.colors):
            plt.plot(x_list[0][self.colors.index(color)],y,color=color,marker='o',alpha=0.5,label='trans_ref',markersize=0.3,linestyle='none')
        for y,color in zip(y_data_type2, self.colors):
            plt.plot(x_list[1][self.colors.index(color)],y,color=color,marker='o',alpha=1,markersize=3,linestyle='none')
        for y,color in zip(y_data_type3, self.colors):
            plt.plot(x_list[2][self.colors.index(color)],y,color=color,linestyle='dashed',linewidth=1)
        for y,color in zip(y_data_type4, self.colors):
            plt.plot(x_list[2][self.colors.index(color)],10 * np.log10([data * 1000 for data in y]),color=color,linestyle='dashed',linewidth=1)
        plt.title('flat_TR_graph',fontdict=self.title_font_properties)
        plt.xlabel('wave length[nm]', fontdict=self.label_font_properties)
        plt.ylabel('transmission[dB]', fontdict=self.label_font_properties)
        plt.xticks(fontsize=6)  # modulate axis label's fontsize
        plt.yticks(fontsize=6)
        plt.plot(self.wave_len_ref,self.trans_ref,marker='o',alpha=0.5,label='trans_ref',markersize=0.5)
        plt.plot(self.wave_len_ref,self.fit_trans_ref_real,linestyle='dashed',label='ref_fit',linewidth=1)
        legend1 = plt.legend(handles=self.legend_elements, fontsize=6, ncol=2, loc='upper right')
        plt.gca().add_artist(legend1)
        legend2 = plt.legend([labels[0]], fontsize=5, ncol=2, loc=(0.02, 0.777),handlelength=0)
        legend3 = plt.legend([labels[1]],fontsize=5, ncol=2, loc=(0.02, 0.94),handlelength=0)
        legend4 = plt.legend([labels[2]],fontsize=5, ncol=2, loc=(0.02, 0.90),handlelength=0)
        plt.gca().add_artist(legend2)
        plt.gca().add_artist(legend3)
        plt.gca().add_artist(legend4)
        font_props = {'weight': 'bold', 'size': 6}
        plt.legend(['o : raw data', '-- : fitted graph'], fontsize=5, ncol=1, loc='lower right',
                             handlelength=0, prop=font_props)

    def fitted_TR_graph_plot(self):
        for bia in self.bias:
            i = self.bias.index(bia)
            plt.plot(self.wave_len[i], self.I[i], alpha=0.8, marker='o', markersize=0.3, linestyle='none',
                     color=self.colors[i])
            plt.plot(self.wave_len[i], self.fitted_TR_data[i], linewidth=0.8, color=self.colors[i], label=f'{bia}V')
        plt.xlabel('wavelength[nm]', fontdict=self.label_font_properties)
        plt.ylabel('intensity[W]', fontdict=self.label_font_properties)
        plt.xticks(fontsize=6)  # modulate axis label's fontsize
        plt.yticks(fontsize=6)
        plt.title('Fitted Intensity Graph', fontdict=self.title_font_properties)
        legend1 = plt.legend(loc='upper right', fontsize=6, ncol=2)
        plt.gca().add_artist(legend1)
        font_props = {'weight': 'bold', 'size': 6}
        plt.legend(['o : raw data', '-- : fitted graph'], fontsize=5, ncol=1, loc=(0.01, 0.92), handlelength=0,prop=font_props)
        plt.grid()
    def del_n_eff_by_voltage(self):
        plt.plot(self.bias, self.del_n_eff, marker='o',alpha=0.5,markersize=3,color='red',linestyle='none',label='raw data')
        plt.plot(np.linspace(self.bias[0],self.bias[-1],10), np.poly1d(np.polyfit(self.bias, self.del_n_eff, 2))(np.linspace(self.bias[0],self.bias[-1],10)),linestyle='dashed', linewidth=1,color='blue',label='fit(2_deg)')
        plt.axhline(0, color='black',linestyle='dashed',linewidth=1)  # x축에 대한 수평선
        plt.axvline(0, color='black',linestyle='dashed',linewidth=1)  # y축에 대한 수직선
        plt.xticks(fontsize=6)  # modulate axis label's fontsize
        plt.yticks(fontsize=6)
        plt.text(0.5, 0.8, 'V_piL = {:.8f}'.format(self.V_piL), fontweight = 'bold', fontsize=7,transform=plt.gca().transAxes)
        plt.xlabel('voltage[V]', fontdict=self.label_font_properties)
        plt.ylabel(r'$\Delta$'+'n_eff', fontdict=self.label_font_properties)
        plt.title(r'$\Delta$'+'n_eff - Voltage Graph', fontdict=self.title_font_properties)
        plt.legend(loc='upper right',fontsize=6, ncol=2)
        plt.grid()
    def enlarged_fitted_TR_graph(self):
        # print(minimum_wave_len)
        for bia in self.bias:
            i = self.bias.index(bia)
            plt.plot(self.wave_len[i][(self.ref_wave_len_index-self.index_range):(self.ref_wave_len_index+self.index_range)], self.fit_raw_TR[i], linestyle='dashed', linewidth=1,color=self.colors[i])
            plt.plot(self.wave_len[i][(self.ref_wave_len_index-self.index_range):(self.ref_wave_len_index+self.index_range)],self.raw_trans[i][(self.ref_wave_len_index-self.index_range):(self.ref_wave_len_index+self.index_range)],marker='o',alpha=1,label='trans_ref',markersize=0.25,color=self.colors[i],linestyle='none')
        plt.xticks(fontsize=6)  # modulate axis label's fontsize
        plt.yticks(fontsize=6)
        plt.title('Enlarged Transmission graph (raw & fit)', fontdict=self.title_font_properties)
        plt.xlabel('wavelength[nm]', fontdict=self.label_font_properties)
        plt.ylabel('transmission[dB]', fontdict=self.label_font_properties)
        plt.text(0.1, 0.5, 'R_square = {:.8f}'.format(self.R_square_TR), fontweight = 'bold', fontsize=7,transform=plt.gca().transAxes)
        # plt.legend(handles=self.legend_elements, fontsize=5, ncol=2, loc='upper right')
        font_props = {'weight': 'bold','size':6}
        legend1 = plt.legend(['o : raw data','-- : fitted graph'], fontsize=5, ncol=1, loc=(0.01, 0.89), handlelength=0, prop=font_props)
        plt.gca().add_artist(legend1)
        plt.legend(handles=self.legend_elements, fontsize=6, ncol=2, loc='upper right')

# 예시 사용 방법
# test = plot_TR('HY202103','D08','20190712_113254','(-1,-1)')
# test.data_parse()
# # test.fitted_TR_graph_plot()
# # test.flat_TR_graph_plot()
# # test.enlarged_fitted_TR_graph()
# # plt.show()
# test.del_n_eff_by_voltage()
# plt.show()
