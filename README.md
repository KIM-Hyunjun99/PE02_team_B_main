##
<h1 align="center">👋 PE2-team-B 👋</h1>
<h3 align="center">Visualize the information of the desired data</h3>


## Index
[Introduction](#Introduction)   
[Environment](#Environment)   
[skill](#skill)    
[Usage](#Usage)     
[Result](#Result)
***


## Introduction
- This tool is data analysis software using PyCharm. 

- Put the data file in the folder and choose the name of lots you want,
this program stores analyzed Dataframes and graphs and shows xml data customer give.
- Through the measurement data, you can compare and analyze the data of the desired part.

### -Team members 
1. Kim Hyunjun   - guswns9474@hanyang.ac.kr
2. Seo Jaeyun    - seojy06@hanyang.ac.kr
3. Lee Jonggeon  - dlwhdrjs020801@hanyang.ac.kr
4. Jung Myungjin - jmj3034@hanyang.ac.kr


***



## Environment

<p align="left">
  <a href="link_to_python_file.py">
    <img src="https://img.shields.io/badge/Python-%23217346.svg?&style=for-the-badge&logo=python&logoColor=white&color=lightgray" alt="python" height="40" />
</a>
  <a href="link_to_windows_file.exe">
    <img src="https://img.shields.io/badge/Windows-%230078D6.svg?&style=for-the-badge&logo=windows&logoColor=white" alt="windows" height="40" />
  </a>  
</a>
  <a href="link_to_excel_file.xlsx">
    <img src="https://img.shields.io/badge/Excel-%23217346.svg?&style=for-the-badge&logo=excel&logoColor=white" alt="excel" height="40" />
  </a>
</p>

***
  
## <h3 align="left">Skill:</h3>
- Select the information you want and it will visualize the data

1. Excel file
2. IV graph
3. Transmission spectra graph
4. transmission spectra Flat graph
5. Intensity fitted graph
6. Enlarged Transmission spectra fitted graph
7. Del_n_eff graph

***

## Usage

### Library function required to execute code
```python
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

import tkinter.messagebox as messagebox
import shutil
import tkinter as tk
from tkinter import ttk

import warnings
from tqdm import tqdm
import time
from matplotlib.patches import Patch

from limit import Parameters, minimize

import subprocess
```
### Execution code for executing the entire program

```python
import GUI
import install_module
with open('count.txt', 'r') as f:  # txt 파일에서 숫자 데이터(돌린 횟수) 읽기
    count = float(f.read())
if count == 0:
    install_module.install_all_library()
GUI.GUI()
```

**If you run 'run.py' , the GUI window appears as follows**

![GUI 0](https://github.com/PE2-team-B/PE02_team_B_main/assets/128004215/a5d0e352-335d-430c-9a09-9db125d16159)
1. **Lots** : You can get the data by selecting the desired Lots.
2. **Search All Lots** : You can choose the 'Search All Lots', Which is programmed for data for all Lots.
   * If you don't want to get information about all Lot, choose Lot above yourself
3. **create_csv_file** : Only csv files for data can be obtained.
4. **Clear res** :Delete all data in the res folder.

**if you click the 'Lots number',  the GUI will go to the following page.**

![GUI 3](https://github.com/PE2-team-B/PE02_team_B_main/assets/128004215/64d06d7a-7018-4d97-ab56-9eb3d8bb47b1)

5. **Date folder** : You can choose the data-folder you want.
   * You can select the coordinate of the wafer to the right of the selected wafer(e.g.,(1,1))
   *  if you want to check the entire coordinates, the input can be 'all'.
6. **Graph** : Desired graphs may be extracted by selecting a desired graph among IV graph, TR graph, Flat_TR graph, Intensity_fit graph, Enlarged_TR_fit graph, Del_n_eff graph.
7. **confirm** : Execute the code according to the conditions you choose.
8. **Exit** : Close the GUI.
9. **Previous Page** : Proceed to the previous page of the GUI.

***
## Result

![Graph1](https://github.com/PE2-team-B/PE02_team_B_main/assets/128004215/7a8c1df8-0e25-49ea-a487-8a476ce8ea80)
![CSV3](https://github.com/PE2-team-B/PE02_team_B_main/assets/128004215/52937c8e-979a-40fd-8a65-9498766bd7d0)
![CSV4](https://github.com/PE2-team-B/PE02_team_B_main/assets/128004215/4c314ca8-cfb5-455b-82c1-94c17213faf4)


