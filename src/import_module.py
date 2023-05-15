import subprocess

# pip 설치
subprocess.call(['python', '-m', 'ensurepip', '--default-pip'])
subprocess.call(['python', '-m', 'pip', 'install', '--upgrade', 'pip'])

# 필요한 라이브러리 설치
subprocess.call(['python', '-m', 'pip', 'install', 'matplotlib'])
subprocess.call(['python', '-m', 'pip', 'install', 'numpy'])
subprocess.call(['python', '-m', 'pip', 'install', 'lmfit'])
subprocess.call(['python', '-m', 'pip', 'install', 'pandas'])

# 필요한 라이브러리 설치 확인
import matplotlib
import numpy
import lmfit
import pandas

print(matplotlib.__version__)
print(numpy.__version__)
print(lmfit.__version__)
print(pandas.__version__)
