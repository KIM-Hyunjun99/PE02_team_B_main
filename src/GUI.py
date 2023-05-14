import tkinter.messagebox as messagebox
import os
import numpy as np

def GUI():
  lot_list = []
  date_list = []
  filename_dict = {}  # 'lot이름_날짜파일':'(row,column) 형식으로 순회되며 저장될 딕셔너리
  filelist1 = []  # filename_dict가 만들어 지기 위해 임시적으로 row/column 을 저장.
  n = 0

  # data_file 디렉토리와 그 하위 디렉토리를 순회하면서 파일 경로를 검색
  for dirpath, dirnames, filenames in os.walk('../dat'):
    n += 1
    if n == 1:
      lot_list.append(dirnames)
    if n > 1 and dirnames != []:
      date_list.append(dirnames)

  for dirpath, dirnames, filenames in os.walk('../dat'):
    filelist1 = []
    for filename in filenames:
      if 'LMZ' in filename and filename.endswith('.xml'):
        filelist1.append(filename[filename.index('('): filename.index(')') + 1])
        filename_dict[dirpath.split('\\')[-2] + '_' + dirpath.split('\\')[-1]] = filelist1

  lot_date_dict = dict(zip(np.array(lot_list).flatten().tolist(), date_list))
  print(lot_date_dict)
  print(filename_dict)
  import tkinter as tk
  from tkinter import ttk

  # 딕셔너리 정의
  data = lot_date_dict

  # Tkinter 창 생성
  root = tk.Tk()
  root.title("User Interface for Inspection Range")
  root.geometry("1300x200+150+250")

  # 혹시 쓸일이 있을까 만들어 놓은거
  # keylist=[]
  # valuelist=[]

  frames = []

  for key in data:
    frame = tk.Frame(root)
    frame.pack(side='top', anchor='w')
    frames.append(frame)

    values = data[key]

    # 키와 값을 표시할 라벨 생성
    label = tk.Label(frame, text=key)
    label.pack(side='left', anchor='w')

    # 각 값을 체크박스로 추가
    for value1 in values:
      globals()['var{}'.format(value1)] = tk.BooleanVar()
      globals()['checkbox{}'.format(value1)] = tk.Checkbutton(frame, text=value1,
                                                              variable=globals()['var{}'.format(value1)])
      globals()['checkbox{}'.format(value1)].pack(side='left', anchor='w')
      result = ''.join([key for key, value in data.items() if value == values])
      # keylist.append(result)
      # valuelist.append(value1)
      try:
        filename_dict[key + '_' + value1]

      except KeyError:
        globals()['combobox{}'.format(value1)] = tk.ttk.Combobox(frame, values=['LMZ xml파일 없음'], state="readonly")
        globals()['combobox{}'.format(value1)].pack(side='left')
        globals()['combobox{}'.format(value1)].set('선택불가')
      else:
        list3 = filename_dict[key + '_' + value1]
        list3.append('All')

        globals()['combobox{}'.format(value1)] = tk.ttk.Combobox(frame, values=list3, state="readonly")
        globals()['combobox{}'.format(value1)].pack(side='left')
        globals()['combobox{}'.format(value1)].set('선택가능')

  def show_selected():
    global selected
    d = 0
    selected = []
    for key in data:
      values = data[key]
      for value1 in values:
        var = globals()['var{}'.format(value1)]
        c = globals()['combobox{}'.format(value1)]
        if var.get() == True and c.get() != '선택가능':
          d += 1
          selected.append((key, value1, c.get()))
        elif var.get() == True and c.get() == '선택가능':
          messagebox.askokcancel("Warning", "선택된 날짜의 row/column 설정되지 않음")
          d += 1
          selected = []

    if selected == [] and d == 0:
      messagebox.askokcancel("Warning", "선택된 파일이 없습니다.")
      selected = []

    elif selected != []:
      print(selected),

  # 확인 버튼 생성
  button = tk.Button(root, text="confirm", command=show_selected)
  button.pack(side='bottom')
  button = tk.Button(root, text="Exit", command=root.destroy)
  button.pack(side='bottom')

  # Tkinter 창 실행
  root.mainloop()
  return

GUI()
