import xml.etree.ElementTree as elemTree
import numpy as np
from datetime import datetime
import os
from lmfit import Model
import warnings
import pandas as pd
from src import graph_individual as gi
from tqdm import tqdm
from src import TR_graph_plot
import time
from src import functions as fc
from matplotlib.patches import Patch
import matplotlib.pyplot as plt
import xml.etree.ElementTree as elemTree


class csv_class:
    def __init__(self,Lot,Wafer,Date,Position):
        self.Lot = Lot
        self.Wafer = Wafer
        self.Date = Date
        self.Position = Position
        self.label_font_properties = {'size':7,'weight':'bold'}
        self.title_font_properties = {'size':10,'weight':'bold'}
        self.max_fit = []
        self.band_wave_len = 0
        self.I = np.array([])
        self.V = np.array([])
        self.Operator = ''
        self.R_square_IV = 0
        self.R_max_Ref = 0
        self.Lot_excel = ''
        self.column = ''
        self.Script_id = ''
        self.Name = ''
        self.wafer_name = ''
        self.Mask_name = ''
        self.Testsite = ''
        self.Date_csv = ''
        self.Analysis_WL = 0
        self.Max_TR_ref = 0
        self.I_n_1V = 0
        self.I_p_lV = 0
        self.I = np.array([])
        self.V = np.array([])
        self.Error_flag = 0
        self.Error_dsc = ''
        self.temp1 = 0
        self.temp2 = 0
        self.temp3 = 0
        self.temp4 = 0
        self.users = {'audwl': 'B1', "J Seo": 'B2', 'junjuns': 'B3', 'User': 'B4'}
        self.username = os.environ['USERNAME']
        self.name = ['Lot','Wafer','Mask','TestSite','Name','Date','Script ID','Scipt Version','Script Owner','Operator','Row','Column'
            ,'ErrorFlag','Error description','Analysis Wavelength[nm]','Rsq of Ref.spectrum(Nth)','Max_transmission of Ref.spec.(dB)','Rsq of IV','I at -1V[A]','I at 1V[A]','V_piL[V]','rsq of TR','n_eff']

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
        self.Intensity = []
        # smoothed_trans = np.array([])
        temp1 = 0
        temp2 = 0

        path = os.path.join('dat',self.Lot,self.Wafer,self.Date)
        self.file_name = [os.path.join(path, f) for f in os.listdir(path) if 'LMZ' in f and f.endswith('.xml') and self.Position in f]

        tree = elemTree.parse(self.file_name[0])
        root = tree.getroot()
        for current in root.iter('Current'):
            self.I = np.array(abs(np.array(list(map(float, current.text.split(','))))))
        for voltage in root.iter('Voltage'):
            self.V = np.array(list(map(float, voltage.text.split(','))))
        for modulator in root.iter('Modulator'):
            for WL_sweep in modulator.iter('WavelengthSweep'):
                if temp1 == 0:
                    self.Name = modulator.find('DeviceInfo').attrib['Name']
                elif temp1 == 1:
                    self.wave_len_ref = np.append(self.wave_len_ref, np.array(list(map(float, WL_sweep.find('L').text.split(',')))))
                    self.trans_ref = np.append(self.trans_ref, np.array(list(map(float, WL_sweep.find('IL').text.split(',')))))
                    continue
                self.wave_len.append(list(map(float, WL_sweep.find('L').text.split(','))))
                self.raw_trans.append(list(map(float, WL_sweep.find('IL').text.split(','))))
                self.bias.append(float(WL_sweep.attrib['DCBias']))
                temp2 += 1
            temp1 += 1
        self.Max_TR_ref = max(self.trans_ref)
        # TestSiteInfo에서 구할 수 있는 데이터 추출
        for i in root.iter('TestSiteInfo'):
            self.Lot_excel = i.attrib['Batch']
            self.wafer_name = i.attrib['Wafer']
            self.Mask_name = i.attrib['Maskset']
            self.Testsite = i.attrib['TestSite']
            self.column = i.attrib['DieColumn']
            self.row = i.attrib['DieRow']
        # Analysis_WL 데이터 추출
            for i in root.iter('DesignParameters'):
                if self.temp2 == 0:
                    for k in i.iter('DesignParameter'):
                        if self.temp3 == 1:
                            self.Analysis_WL = k.text
                        self.temp3 += 1
                self.temp2 += 1
        # 날짜 data 추출
        for i in root.iter('OIOMeasurement'):
            date_str = i.attrib['CreationDate']
            dt = datetime.strptime(date_str,'%a %b %d %H:%M:%S %Y')
            self.Date = dt.strftime('%Y%m%d-%H%M%S')
            self.Operator = i.attrib['Operator']

        # 데이터 추출하고 나서 만들어야 하는 데이터 생성
        self.R_square_IV = fc.shockely_diode_IV_fit_R(self.V, self.I)
        self.R_max_Ref = fc.Best_fit_R(np.array(self.wave_len_ref),np.array(self.trans_ref))
        self.I_n_1V = self.I[list(self.V).index(-1)]
        # print(self.I_n_1V)
        self.I_p_1V = self.I[list(self.V).index(1)]
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
            self.Intensity.append([10 ** (x / 10) / 1000 for x in self.minus_max_fit_trans[i]])
        # print(I)
        # for i in range(temp2):
        #     plt.plot(self.wave_len[i],self.I[i],marker='o',alpha=0.4,markersize=1)
        # 극댓값 정보를 찾기 -> 여러개 시도
        # print(I[bias.index(0.0)], wave_len[bias.index(0.0)])
        # print(bias)
        self.R_square_TR = []
        self.fit_raw_TR = []
        self.del_n_eff = []
        self.fitted_TR_data = []
        result_n_eff = fc.Transmission_fitting_n_eff(self.wave_len, self.Intensity, self.bias)
        self.n_eff = result_n_eff[0]
        for bia in self.bias:
            if bia == 0.0:
                self.del_n_eff.append(0.0)
                self.fitted_TR_data.append(result_n_eff[1])
                continue
            result_del_n_eff = fc.Transmission_fitting_n_eff_V(self.wave_len, self.Intensity, self.n_eff, self.bias, bia)
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
        # print(minimum_wave_len)
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
            self.R_square_TR.append(fc.R_square(np.array(self.wave_len[i][(self.ref_wave_len_index-self.index_range):(self.ref_wave_len_index+self.index_range)]),np.array(self.raw_trans[i][(self.ref_wave_len_index-self.index_range):(self.ref_wave_len_index+self.index_range)]),np.array(self.fit_raw_TR[i])))
        self.R_square_TR = np.mean(np.array(self.R_square_TR))
        self.V_piL = self.band_wave_len * 10 ** (-9) / (self.del_n_eff[self.bias.index(-2)])
# ------------------------------------------------------------------------------------------------------------------------ Error flag, Error dsc 할당
        if self.R_max_Ref < 0.95:
            self.Error_flag += 1
            if self.Error_dsc == '':
                self.Error_dsc += 'IV_fit_error'
            else:
                self.Error_dsc += ',IV_fit_error'
        if self.R_square_TR < 0.9:
            self.Error_flag += 1
            if self.Error_dsc == '':
                self.Error_dsc += 'TR_fit_error'
            else:
                self.Error_dsc += ',TR_fit_error'
        if self.V_piL < 0:
            self.Error_flag += 1
            if 'TR_fit_error' not in self.Error_dsc:
                if self.Error_dsc == '':
                    self.Error_dsc += 'device_error'
                else:
                    self.Error_dsc += ',device_error'
            else:
                if self.Error_dsc == '':
                    self.Error_dsc += 'V_piL_error by TR_fit'
                else:
                    self.Error_dsc += ',V_piL_error by TR_fit'
        if self.Error_flag == 0:
            self.Error_dsc += 'No error'
class csv:
    def __init__(self):
        start_dir = os.path.join('dat')  # 제일 중요한 코드, '..'는 현재 디렉토리의 부모 디렉토리를 반환해주는 코드, 그걸 data_file과 연결
        self.file_paths = []  # 전체 파일 경로를 원소로 가지는 리스트 변수 초기화
        self.name = ['Lot', 'Wafer', 'Mask', 'TestSite', 'Name', 'Date', 'Script ID', 'Scipt Version', 'Script Owner',
                     'Operator', 'Row', 'Column'
            , 'ErrorFlag', 'Error description', 'Analysis Wavelength[nm]', 'Rsq of Ref.spectrum(Nth)',
                     'Max_transmission of Ref.spec.(dB)', 'Rsq of IV', 'I at -1V[A]', 'I at 1V[A]', 'V_piL[V]','rsq of TR','n_eff']

        # dat 디렉토리와 그 하위 디렉토리를 순회하면서 파일 경로를 수집
        for dirpath, dirnames, filenames in os.walk(start_dir):
            for filename in filenames:
                if '_LMZ' in filename and filename.endswith('.xml'):
                    self.file_paths.append(os.path.join(dirpath, filename))

        def convert_list(file_names):
            converted_list = []
            for file_name in file_names:
                lot_data = file_name.split('\\')[2]
                folder_name = file_name.split('\\')[3]
                timestamp = file_name.split('\\')[4]
                coordinates = file_name.split('\\')[-1].split('_')[2]
                converted_list.append((lot_data, folder_name, timestamp, coordinates))
            return converted_list

        self.default_list = convert_list(self.file_paths)
    def run_csv(self):
        Lot = np.array([])
        Wafer_name = np.array([])
        Mask_name = np.array([])
        TestSite = np.array([])
        Date = np.array([])
        Script_id = np.array([])
        Script_version = np.array([])
        Script_owner = np.array([])
        Operator = np.array([])
        Name = np.array([])
        row = np.array([])
        column = np.array([])
        Error_flag = np.array([])
        Error_dsc = np.array([])
        Analysis_WL = np.array([])
        R_max_Ref = np.array([])
        Max_TR_ref = np.array([])
        R_square_IV = np.array([])
        I_n_1V = np.array([])
        I_p_1V = np.array([])
        progress_bar = tqdm(total=len(self.file_paths))
        V_piL = np.array([])
        R_square_TR = np.array([])
        users = np.array([])
        n_eff = np.array([])

        for file_name in self.default_list:
            # print(self.file_name)
            object = csv_class(*file_name)
            object.data_parse()
            Lot = np.append(Lot, object.Lot_excel)
            Wafer_name = np.append(Wafer_name, object.wafer_name)
            Mask_name = np.append(Mask_name, object.Mask_name)
            TestSite = np.append(TestSite, object.Testsite)
            Date = np.append(Date,object.Date)
            Script_id = np.append(Script_id,'process ' + object.Testsite[-4:-1])
            Operator = np.append(Operator,object.Operator)
            row = np.append(row,object.row)
            column = np.append(column,object.column)
            Error_flag = np.append(Error_flag,object.Error_flag)
            Error_dsc = np.append(Error_dsc,object.Error_dsc)
            Name = np.append(Name,object.Name)
            Analysis_WL = np.append(Analysis_WL,object.Analysis_WL)
            R_max_Ref = np.append(R_max_Ref, object.R_max_Ref)
            Max_TR_ref = np.append(Max_TR_ref,object.Max_TR_ref)
            R_square_IV = np.append(R_square_IV,object.R_square_IV)
            I_n_1V = np.append(I_n_1V,object.I_n_1V)
            I_p_1V = np.append(I_p_1V,object.I_p_1V)
            V_piL = np.append(V_piL,object.V_piL)
            R_square_TR = np.append(R_square_TR,object.R_square_TR)
            users = np.append(users,object.users[object.username])
            n_eff = np.append(n_eff,object.n_eff)
            progress_bar.update(1)

        data_len = len(self.default_list)
        Lot = Lot.reshape(data_len,1)
        Wafer_name = Wafer_name.reshape(data_len,1)
        Mask_name = Mask_name.reshape(data_len,1)
        TestSite = TestSite.reshape(data_len,1)
        Date = Date.reshape(data_len,1)
        Name = Name.reshape(data_len,1)
        Operator = Operator.reshape(data_len,1)
        row = row.reshape(data_len,1)
        column = column.reshape(data_len,1)
        Script_id = Script_id.reshape(data_len,1)
        Error_flag = Error_flag.reshape(data_len,1)
        Error_dsc = Error_dsc.reshape(data_len,1)
        Analysis_WL = Analysis_WL.reshape(data_len,1)
        R_max_Ref = R_max_Ref.reshape(data_len,1)
        Max_TR_ref = Max_TR_ref.reshape(data_len,1)
        R_square_IV = R_square_IV.reshape(data_len,1)
        I_n_1V = I_n_1V.reshape(data_len,1)
        I_p_1V = I_p_1V.reshape(data_len,1)
        V_piL = V_piL.reshape(data_len,1)
        R_square_TR = R_square_TR.reshape(data_len,1)
        n_eff = n_eff.reshape(data_len,1)
        users = users.reshape(data_len,1)

        # 엑셀 파일을 만드는 코드
        try:
            with open('src/count.txt','r') as f: # txt 파일에서 숫자 데이터(돌린 횟수) 읽기
                count = float(f.read())
                count += 0.1
        except FileNotFoundError: # 처음에 아무 아무 숫자가 없어 생기는 오류 방지
            with open('src/count.txt','w') as f:
                f.write(str(count))

        with open('src/count.txt','w') as f: # +0.1이 된 횟수를 다시 작성(w는 원래 있던 데이터를 삭제하고 다시 씀)
            f.write(str(count))

        Script_version = np.full((data_len, 1), count)
        Script_owner = users

        df = pd.DataFrame(
            np.hstack([Lot, Wafer_name, Mask_name, TestSite, Name, Date, Script_id, Script_version, Script_owner
                          , Operator, row, column, Error_flag, Error_dsc, Analysis_WL, R_max_Ref, Max_TR_ref,
                       R_square_IV, I_n_1V, I_p_1V,V_piL,R_square_TR,n_eff]), columns=self.name)
        df.to_csv(os.path.join('res', 'PE02_LMZ_excel_data.csv'), index=False)
        progress_bar.close()
def csv_prc_exe():
    main_object = csv()
    main_object.run_csv()

# csv_prc_exe()

