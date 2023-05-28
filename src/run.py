import GUI
import install_module
with open('count.txt', 'r') as f:  # txt 파일에서 숫자 데이터(돌린 횟수) 읽기
    count = float(f.read())
if count == 0:
    install_module.install_all_library()