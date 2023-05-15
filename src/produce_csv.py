import xml.etree.ElementTree as elemTree
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import os
from lmfit import Model
import warnings
import pandas as pd
from tkinter import *
import functions as func
def create_csv():
    # poorly conditioned로 인한 에러 메세지 나타나지 않도록 하는 코드
    warnings.filterwarnings('ignore',category=np.RankWarning)

    # 변수 설정
    I = np.array([])
    V = np.array([])
    WL = []
    TR = []
    WL_ref = []
    TR_ref = []
    R_square_IV = np.array([])
    R_max_Ref = np.array([])
    data_length_WL = np.array([])
    data_length_TR = np.array([])
    Lot = np.array([])
    row = np.array([])
    column = np.array([])
    Operator = np.array([])
    Script_id = np.array([])
    Name = np.array([])
    Wafer_name = np.array([])
    Mask_name = np.array([])
    TestSite = np.array([])
    Operator = np.array([])
    Date = np.array([])
    Analysis_WL = np.array([])
    Max_TR_ref = np.array([])
    Script_version = np.array([])
    Script_owner = np.array([])
    DC_bias=[]  # 수정 필요 부분
    count = 0
    data_I_length = 0
    file_numbers = 0
    temp1 = 0
    temp2 = 0
    temp3 = 0
    temp4 = 0 # xml 파일 순회시 마다 카운트하는 변수
    users = {'audwl':'B1', "J Seo":'B2','junjuns':'B3','User':'B4'}
    username = os.environ['USERNAME']
    name = ['Lot','Wafer','Mask','TestSite','Name','Date','Script ID','Scipt Version','Script Owner','Operator','Row','Column'
            ,'ErrorFlag','Error description','Analysis Wavelength[nm]','Rsq of Ref.spectrum(Nth)','Max_transmission of Ref.spec.(dB)','Rsq of IV','I at -1V[A]','I at 1V[A]']

    # LMZ 파일만을 순회하기 위한 코드
    # start_dir = 'C:\\Users\\audwl\\PycharmProjects\\TeamB_main\\dat'
    start_dir = os.path.join('..','dat') # 제일 중요한 코드, '..'는 현재 디렉토리의 부모 디렉토리를 반환해주는 코드, 그걸 data_file과 연결
    file_paths = [] # 전체 파일 경로를 원소로 가지는 리스트 변수 초기화

    # dat 디렉토리와 그 하위 디렉토리를 순회하면서 파일 경로를 검색
    for dirpath, dirnames, filenames in os.walk(start_dir):
        for filename in filenames:
            if '_LMZ' in filename and filename.endswith('.xml'):
                file_paths.append(os.path.join(dirpath,filename))
    print(file_paths)
    file_numbers = len(file_paths)

    for file_name in file_paths:
        # xml 파일 파싱이 반복될 때마다 또 사용해야 되기 때문에 counting 변수 반복시마다 0으로 초기화
        temp1 = 0
        temp2 = 0
        temp3 = 0
        WL_temp = []
        TR_temp = []

        tree = elemTree.parse(file_name)
        root = tree.getroot()
    # 전류, 전압 데이터 추출
        for current in root.iter('Current'):
            I = np.append(I, abs(np.array(list(map(float, current.text.split(','))))))
        for voltage in root.iter('Voltage'):
            V = np.append(V, list(map(float, voltage.text.split(','))))
            data_I_length = np.array(list(map(float, voltage.text.split(',')))).size
        for MD in root.iter('Modulator'):
            if temp1 == 0:
                Name = np.append(Name, [MD.find('DeviceInfo').attrib['Name']])
    # WL, TR, DC bias 데이터 추출
            for WL_sweep in MD.iter('WavelengthSweep'):
                if temp1 == 1:
                    WL_ref.append(list(map(float, WL_sweep.find('L').text.split(','))))
                    TR_ref.append(list(map(float, WL_sweep.find('IL').text.split(','))))
                    Max_TR_ref = np.append(Max_TR_ref,np.array([max(list(map(float, WL_sweep.find('IL').text.split(','))))]))
                    data_WL_length = np.array(list(map(float, WL_sweep.find('L').text.split(',')))).size
                    WL.append([WL_temp])
                    TR.append([TR_temp])
                    continue
                WL_temp.append(list(map(float, WL_sweep.find('L').text.split(','))))
                TR_temp.append(list(map(float, WL_sweep.find('IL').text.split(','))))
                if temp4==0:
                    DC_bias.append(WL_sweep.attrib['DCBias'])
            temp1+=1
    # TestSiteInfo에서 구할 수 있는 데이터 추출
        for i in root.iter('TestSiteInfo'):
            Lot = np.append(Lot,[i.attrib['Batch']])
            Wafer_name = np.append(Wafer_name,[i.attrib['Wafer']])
            Mask_name = np.append(Mask_name,[i.attrib['Maskset']])
            TestSite = np.append(TestSite,[i.attrib['TestSite']])
            column = np.append(column,[i.attrib['DieColumn']])
            row = np.append(row,[i.attrib['DieRow']])
    # Analysis_WL 데이터 추출
        for i in root.iter('DesignParameters'):
            if temp2 == 0:
                for k in i.iter('DesignParameter'):
                    if temp3 == 1:
                        Analysis_WL = np.append(Analysis_WL,[k.text])
                    temp3 += 1
            temp2 += 1
    # 날짜 data 추출
        for i in root.iter('OIOMeasurement'):
            date_str = i.attrib['CreationDate']
            dt = datetime.strptime(date_str,'%a %b %d %H:%M:%S %Y')
            Date = np.append(Date, dt.strftime('%Y%m%d-%H%M%S'))
            Operator = np.append(Operator, i.attrib['Operator'])
        temp4+=1
    # 적절한 shape으로 데이터 행렬 변환
    I = I.reshape(len(file_paths),data_I_length)
    V = V.reshape(len(file_paths),data_I_length)
    # WL = WL.reshape(len(file_paths), int(WL.size/WL_ref.size), data_WL_length)
    # TR = TR.reshape(len(file_paths), int(WL.size/WL_ref.size), data_WL_length)
    # WL_ref = WL_ref.reshape(len(file_paths), data_WL_length)
    # TR_ref = TR_ref.reshape(len(file_paths), data_WL_length)
    I_n_1V = I[:,np.where(V == -1)[1][0]].reshape(file_numbers,1) # 1V에 대한 열 데이터 전체를 가져온 변수
    I_p_1V = I[:,np.where(V == 1)[1][0]].reshape(file_numbers,1) # -1V에 대한 열 데이터 전체를 가져온 변수
    Max_TR_ref = Max_TR_ref.reshape(file_numbers,1)
    Lot = Lot.reshape(file_numbers,1)
    Wafer_name = Wafer_name.reshape(file_numbers,1)
    Analysis_WL = Analysis_WL.reshape(file_numbers,1)
    TestSite = TestSite.reshape(file_numbers,1)
    Name = Name.reshape(file_numbers,1)
    Date = Date.reshape(file_numbers,1)
    Mask_name = Mask_name.reshape(file_numbers,1)
    Operator = Operator.reshape(file_numbers,1)
    Script_id = np.array(list('process '+row[0][-4:-1] for row in TestSite)).reshape(file_numbers,1)
    row = row.reshape(file_numbers,1)
    column = column.reshape(file_numbers,1)

    # 데이터 추출하고 나서 만들어야 하는 데이터 생성
    for i in range(I.shape[0]):
        R_square_IV = np.append(R_square_IV, func.shockely_diode_IV_fit_R(V[i],I[i]))
    R_square_IV = R_square_IV.reshape(file_numbers,1)

    for i in range(len(WL_ref)):
        R_max_Ref = np.append(R_max_Ref, func.Best_fit_R(np.array(WL_ref[i]),np.array(TR_ref[i])))
    R_max_Ref = R_max_Ref.reshape(file_numbers,1)

    Error_flag = np.array(list( 0 if x >= 0.95 else 1 for x in list(R_max_Ref))).reshape(file_numbers,1)
    Error_dsc = np.array(list( 'No Error' if x == 0 else 'Ref. spec. Error' for x in list(Error_flag))).reshape(file_numbers,1)

    # 코드를 돌린 횟수를 적립하는 코드
    try:
        with open('count.txt','r') as f: # txt 파일에서 숫자 데이터(돌린 횟수) 읽기
            count = float(f.read())
            count += 0.1
    except FileNotFoundError: # 처음에 아무 아무 숫자가 없어 생기는 오류 방지
        with open('count.txt','w') as f:
            f.write(str(count))

    with open('count.txt','w') as f: # +0.1이 된 횟수를 다시 작성(w는 원래 있던 데이터를 삭제하고 다시 씀)
        f.write(str(count))

    Script_version = np.full((file_numbers,1),count)
    Script_owner = np.full((file_numbers,1),users[username])

    # 모든 데이터를 통합하여 DataFrame을 만들고 이를 csv 파일로 만드는 코드
    # DataFrame은 2차원 배열 만을 입력인자로 받기 때문에 가로로 행렬을 더해주는 hstack을 이용해 (45,1) size의 행렬들을 합쳐 2차원 배열형태로 정리
    df = pd.DataFrame(np.hstack([Lot,Wafer_name,Mask_name,TestSite,Name,Date,Script_id,Script_version,Script_owner
                                 ,Operator,row,column,Error_flag,Error_dsc,Analysis_WL,R_max_Ref,Max_TR_ref,R_square_IV
                                 ,I_n_1V,I_p_1V]),columns=name)
    # res라는 폴더가 없다면 폴더를 만들고 그 안에 csv 파일 생성

    if not os.path.exists('../res'):
        os.makedirs('../res')

    df.to_csv(os.path.join('../res','PE02_LMZ_excel_data.csv'),index=False)
