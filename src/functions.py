# 라이브러리 import
import os
with open('library.txt','r') as f:
    for library in f:
        exec(library)
from lmfit import Parameters, minimize

def fit_data(X,Y,N):
    coef = np.polyfit(X, Y, N)
    func = np.poly1d(coef)
    fit_data = func(X)
    return fit_data

def R_square(X,Y,Y_reg): # R square 값을 계산하는 함수
    Y_mean=sum(Y)/Y.size # 전류의 평균값
    SST=sum((Y-Y_mean)**2) # 전체 데이터와 평균값 간 차이 제곱의 합
    SSE=sum((Y_reg-Y_mean)**2) # 추정값과 평균값 간 차이 제곱의 합
    SSR=sum((Y-Y_reg)**2)
    return 1-SSR/SST # R square 값을 반환

def Ref_fit_func(X,Y,N):
    coef = np.polyfit(X, Y, N)
    func = np.poly1d(coef)
    return func

def Best_fit_R(X,Y): # 가장 R_sqaure가 1에 가까운 R_square 값을 반환하는 함수
    Rs = []
    for i in range(1,11):
        coef = np.polyfit(X,Y,i)
        func = np.poly1d(coef)
        fitted_data = func(X)
        Rs.append(R_square(X,Y,fitted_data))
    max_degree = Rs.index(max(Rs))+1
    return max(Rs)
def shockely_diode_IV_fit_R(V,I):
    def shockely_diode(voltage, rev_sat_I, n):
        k = 1.380649 * 10 ** (-23)
        q = 1.602 * 10 ** (-19)
        temp = 300
        return rev_sat_I * (np.exp(q * voltage / (n * k * temp)) - 1)

    # 모델 인스턴스 생성
    model = Model(shockely_diode)

    # 초기 매개 변수 설정
    params = model.make_params(
        rev_sat_I=1e-7,
        n=1
    )

    # 모델 피팅
    result = model.fit(I[10:], params, voltage=V[10:])
    # print(result.best_fit,'\n',result.best_values) # parameter 값과 근사된 데이터에 대한 값을 보여주는 코드
    coef = np.polyfit(V[:10],I[:10],9)
    func = np.poly1d(coef)
    fit_data = func(V[:10])
    fit_data = np.append(fit_data, result.best_fit)
    return float(str(R_square(V,I,fit_data))[:9])

def Ref_fitted_func(X,Y): # 가장 R_square가 클 때의 fitting data를 반환하는 함수
    Rs = []
    for i in range(1,11):
        coef = np.polyfit(X,Y,i)
        func = np.poly1d(coef)
        fitted_data = func(X)
        Rs.append(R_square(X,Y,fitted_data))
    max_degree = Rs.index(max(Rs))+1
    return Ref_fit_func(X,Y,max_degree)

def shockely_diode_IV_fit(V,I):
    def shockely_diode(voltage, rev_sat_I, n):
        k = 1.380649 * 10 ** (-23)
        q = 1.602 * 10 ** (-19)
        temp = 300
        return rev_sat_I * (np.exp(q * voltage / (n * k * temp)) - 1)

    # 모델 인스턴스 생성
    model = Model(shockely_diode)

    # 초기 매개 변수 설정
    params = model.make_params(
        rev_sat_I=1e-7,
        n=1
    )

    # 모델 피팅
    result = model.fit(I[10:], params, voltage=V[10:])
    # print(result.best_fit,'\n',result.best_values) # parameter 값과 근사된 데이터에 대한 값을 보여주는 코드
    coef = np.polyfit(V[:10],I[:10],9)
    func = np.poly1d(coef)
    fit_data = func(V[:10])
    fit_data = np.append(fit_data, result.best_fit)
    return fit_data

def flat_fit_function(X,Y): # R_square가 가장 클 때의 근사 함수를 반환하는 함수
    Rs = []
    for i in range(1, 11):
        coef = np.polyfit(X, Y, i)
        func = np.poly1d(coef)
        fitted_data = func(X)
        Rs.append(R_square(X, Y, fitted_data))
    max_degree = Rs.index(max(Rs)) + 1
    return np.poly1d(np.polyfit(X,Y,max_degree))

'''
def flat_fit_function(X,Y): # R_square가 가장 클 때의 근사 함수를 반환하는 함수
    coef = np.polyfit(X, Y, 1)
    func = np.poly1d(coef)
    return func
'''
'''
def Transmission_fitting_n_eff(wave_length,intensity,bias):
    def modulator_TR_model(wave_length,I_0,n_eff,b):
        delta_l = 40 * 10**(-9)
        pi = math.pi
        return I_0 * np.array(list(map(math.sin,pi*delta_l*n_eff/wave_length/10**(-9))))**2+b

    model = Model(modulator_TR_model)

    # 초기 매개 변수 설정
    params = model.make_params(
        I_0 = 1,
        n_eff = 2.6,
        b = 0
    )
    # 모델 피팅
    # print(wave_length.shape,intensity.shape)
    result = model.fit(intensity[bias.index(0.0)], params, wave_length=wave_length[bias.index(0.0)])
    print(result.best_values)
    plt.plot(wave_length[bias.index(0.0)],intensity[bias.index(0.0)],'r')
    plt.plot(wave_length[bias.index(0.0)],result.best_fit,'b')
    # 결과 출력
    # print(result.fit_report())
    return 0
'''

def Transmission_fitting_n_eff(wave_length,intensity,bias):
    def modulator_TR_model(wave_length,n_eff):
        delta_l = 40*10**(-6)
        # delta_l = 1200 * 10 ** (-6)
        pi = math.pi
        I_0 = 0.001
        return I_0 * np.array(list(map(math.sin,pi*delta_l*n_eff/(wave_length*10**(-9)))))**2

    model = Model(modulator_TR_model)

    # 초기 매개 변수 설정
    params = model.make_params(
        n_eff = 4.2
        # n_eff=0.14
    )
    # 모델 피팅
    # print(wave_length.shape,intensity.shape)
    result = model.fit(intensity[bias.index(0.0)], params, wave_length=wave_length[bias.index(0.0)])
    # print(result.best_values)
    # plt.plot(wave_length[bias.index(0.0)],intensity[bias.index(0.0)],'r')
    # plt.plot(wave_length[bias.index(0.0)],result.best_fit,'b')
    # 결과 출력wave_length[bias.index(0.0)]
    # print(result.fit_report())
    return (float(result.best_values['n_eff']),result.best_fit)

'''
def Transmission_fitting_n_eff(frequency,intensity,bias,n_eff):
    def modulator_TR_model(freq,I_0,n_eff):
        delta_l = 40 * 10**(-9)
        pi = math.pi
        c = 3*10**8
        return I_0 * np.array(list(map(math.sin,pi*delta_l*n_eff*freq/c/10**(-9))))**2

    model = Model(modulator_TR_model)

    # 초기 매개 변수 설정
    params = model.make_params(
        I_0 = 1,
        n_eff = 2.6
    )
    # 모델 피팅
    # print(wave_length.shape,intensity.shape)
    result = model.fit(intensity[bias.index(0.0)], params, freq=frequency[bias.index(0.0)])
    print(result.best_values)
    plt.plot(frequency[bias.index(0.0)],intensity[bias.index(0.0)],'r')
    plt.plot(frequency[bias.index(0.0)],result.best_fit,'b')
    # 결과 출력
    # print(result.fit_report())
    return 0
'''

def Transmission_fitting_n_eff_V(wave_length,intensity,n_eff,bias,bia):
    def modulator_TR_model_total(wave_length,del_n_eff):
        delta_l = 40*10**(-6)
        pi = math.pi
        I_0 = 0.001
        l = 500*10**(-6)
        return I_0 * np.sin(pi*delta_l*n_eff/(wave_length*10**(-9))+pi * del_n_eff * l / (wave_length*10**(-9)))**2
        # return I_0 * np.array(list(map(math.sin,(pi*delta_l*n_eff/(wave_length*10**(-9)))+(pi * del_n_eff * l / (wave_length*10**(-9))))))**2

    model = Model(modulator_TR_model_total)

    # 초기 매개 변수 설정
    params = model.make_params(
        del_n_eff = 0.001
    )
    # 모델 피팅
    result = model.fit(intensity[bias.index(bia)], params, wave_length=wave_length[bias.index(bia)])
    # plt.plot(wave_length[bias.index(bia)],intensity[bias.index(bia)])
    # plt.plot(wave_length[bias.index(bia)],result.best_fit)
    # plt.show()
    # print(bia,result.best_values)
    # print(result.fit_report())
    return (result.best_values['del_n_eff'],result.best_fit)
