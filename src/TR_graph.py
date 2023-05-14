# 라이브러리 import
with open('library.txt','r') as f:
    for library in f:
        exec(library)
import functions as fc
warnings.filterwarnings('ignore',category=np.RankWarning)
def plot_TR_graph(Wafer,Date,Position):

    wave_len = np.array([])
    wave_len_ref = np.array([])
    trans = np.array([])
    wave_len_half = []
    trans_half = []
    trans_ref = np.array([])
    wave_len_max = []
    trans_max = []
    smoothed_trans = np.array([])
    temp1 = 0
    temp2 = 0

    path = os.path.join('..','dat',Wafer,Date)
    file_name = [os.path.join(path,f) for f in os.listdir(path) if 'LMZ' in f and f.endswith('.xml') and Position in f]

    tree = elemTree.parse(file_name[0])
    root = tree.getroot()

    for modulator in root.iter('Modulator'):
        for WL_sweep in modulator.iter('WavelengthSweep'):
            if temp1 == 1:
                wave_len_ref = np.append(wave_len_ref, np.array(list(map(float, WL_sweep.find('L').text.split(',')))))
                trans_ref = np.append(trans_ref, np.array(list(map(float, WL_sweep.find('IL').text.split(',')))))
                continue
            wave_len = np.append(wave_len, np.array(list(map(float, WL_sweep.find('L').text.split(',')))))
            trans = np.append(trans, np.array(list(map(float, WL_sweep.find('IL').text.split(',')))))
            temp2 += 1
        temp1 += 1
    wave_len = wave_len.reshape(temp2,int(trans.size/temp2))
    trans = trans.reshape(temp2,int(trans.size/temp2))
    fit_trans_ref = fc.Ref_fitted_data(wave_len_ref,trans_ref)
    s = 150
    for i in range(wave_len.shape[0]):
        trans[i] = trans[i] - fit_trans_ref
        trans_half_temp = []
        wave_len_half_temp = []
        for k in range(wave_len.shape[1]):
            count = 0
            if k >= (wave_len.shape[1]-(s+1)):
                continue
            for g in range(1,(s+1)):
                if trans[i][k] > trans[i][k+g]:
                    count += 1
            if count >= s-4:
                trans_half_temp.append(trans[i][k])
                wave_len_half_temp.append(wave_len[i][k])
        wave_len_half.append(wave_len_half_temp)
        trans_half.append(trans_half_temp)

        # plt.plot(wave_len_half[i],trans_half[i],'ro',markersize=0.5)#######

    # for i in range(len(wave_len_half)):

    for i in range(len(wave_len_half)):
        wave_len_max_temp = []
        trans_max_temp = []
        for j in range(len(wave_len_half[i])):
            if j == 0:
                wave_len_max_temp.append(wave_len_half[i][j])
                trans_max_temp.append(trans_half[i][j])
                continue
            elif j >= len(wave_len_half[i]) - 3:
                continue
            if (wave_len_half[i][j + 2] - wave_len_half[i][j + 1]) >= (wave_len_half[i][j + 1] - wave_len_half[i][j] + 6):
                wave_len_max_temp.append(wave_len_half[i][j + 2])
                trans_max_temp.append(trans_half[i][j + 2])
        wave_len_max.append(wave_len_max_temp)
        trans_max.append(trans_max_temp)
        # print(wave_len_max_temp,trans_max_temp)
        # plt.plot(wave_len_max,trans_max,'ro')
        trans[i] = trans[i] - fc.flat_fit_function(np.array(wave_len_max[i]), np.array(trans_max[i]))(wave_len[i]) # flatten 한 데이터들로 다시 trans 변수를 할당
        plt.plot(wave_len[i],trans[i],'b-')
    # 극댓값 정보를 찾기 -> 여러개 시도
    plt.show()
plot_TR_graph('D07','20190715_190855','(0,0)')

  # -> 시도 방법 1 (극댓값 찾기)
'''
    trans_max=np.array([])
    wave_len_max=np.array([])
    for k in range(2, wave_len.shape[1]):
        if k == wave_len.shape[1] - 1:
            continue
        if trans[i][k] > trans[i][k - 1] and trans[i][k] < trans[i][k + 1]:
            trans_max = np.append(trans_max, trans[i][k])
            wave_len_max = np.append(wave_len_max, wave_len[i][k])
    print(trans_max.size, wave_len.shape[0])
    plt.plot(wave_len_max, trans_max, 'ro',markersize=0.5)
'''