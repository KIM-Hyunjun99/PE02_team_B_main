import tkinter.messagebox as messagebox
import os
import numpy as np
import graph_show as gs
import shutil
import delete_code as dc
import produce_csv as prc
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk



def GUI():
  lot_list = []
  date_list = []
  filename_dict = {}  # 'lot이름_날짜파일':'(row,column) 형식으로 순회되며 저장될 딕셔너리
  filelist1 = []  # filename_dict가 만들어 지기 위해 임시적으로 row/column 을 저장.
  n = 0

  # data_file 디렉토리와 그 하위 디렉토리를 순회하면서 파일 경로를 검색
  for dirpath, dirnames, filenames in os.walk('../dat'):
    n += 1
    if n == 2:
      lot_list.append(dirnames)
    if n > 2 and dirnames != []:
      date_list.append(dirnames)

  for dirpath, dirnames, filenames in os.walk('../dat'):
    filelist1 = []
    for filename in filenames:
      if 'LMZ' in filename and filename.endswith('.xml'):
        filelist1.append(filename[filename.index('('): filename.index(')') + 1])
        filename_dict[dirpath.split('\\')[-2] + '_' + dirpath.split('\\')[-1]] = filelist1

  lot_date_dict = dict(zip(np.array(lot_list).flatten().tolist(), date_list))



  # 딕셔너리 정의
  data = lot_date_dict

  # Tkinter 창 생성
  root = tk.Tk()
  root.title("User Interface for Inspection Range")
  root.geometry("370x600+550+120")

  # 혹시 쓸일이 있을까 만들어 놓은거
  # keylist=[]
  # valuelist=[]

  frames = []
  labelblank1 = tk.Label(root, text='                                                   ')
  labelblank1.pack(side='top', anchor='w')
  for key in data:
    frame = tk.Frame(root)
    frame.pack(side='top', anchor='w')
    frames.append(frame)

    values = data[key]

    # 키와 값을 표시할 라벨 생성
    labelblank3 = tk.Label(frame, text='')
    labelblank3.pack(side='left', anchor='w')
    label = tk.Label(frame, text=key, font=("Helvetica", 14, "bold"))
    label.pack(side='left', anchor='w')
    labeldate = tk.Label(frame, text='  Date folder - {}:'.format(key))
    labeldate.pack(side='top', anchor='w')

    # 각 값을 체크박스로 추가
    for value1 in values:
      frame1 = tk.Frame(frame)
      frame1.pack(side='top', anchor='w')

      globals()['var{}'.format(value1)] = tk.BooleanVar()  # 상태를 True/Farse 형태로 저장한다는 말.
      globals()['checkbox{}'.format(value1)] = tk.Checkbutton(frame1, text=value1,
                                                              variable=globals()['var{}'.format(value1)])

      # 동적변수를 이용하여 각기 다른 이름의 체크박스 저장 변수를 형성하여 상태를 할당하고 위치를 지정한다.
      globals()['checkbox{}'.format(value1)].pack(side='left', anchor='w')  # 체크박스를 띄우고 위치를 지정
      result = ''.join([key for key, value in data.items() if value == values])
      # keylist.append(result)
      # valuelist.append(value1)
      try:  # try에 이전 형성해둔 딕셔너리 파일에 'lot이름_날짜'를 넣어보고 오류가 나는지 확인한다.
        filename_dict[key + '_' + value1]

      except KeyError:  # 만일 key error가 발생한다면 해당 딕셔너리에는 lmz,xml 파일 조건이 없으므로 할당 되지 않았고 row/column도 없다는 뜻
        globals()['combobox{}'.format(value1)] = tk.ttk.Combobox(frame1, values=['LMZ xml파일 없음'], state="readonly",foreground='red')
        globals()['combobox{}'.format(value1)].pack(side='left')  # 따라서 콤보박스의 기본값에는 선택불가, 콤보박스 내용에는 파일없음을 표함.
        globals()['combobox{}'.format(value1)].set('선택불가')
      else:
        list3 = filename_dict[key + '_' + value1]  # 만일 딕셔너리에 해당값이 존재한다면 row/column이 존재하니 선택가능
        list3.append('All')  # 선택지에 각각의 row/ column 외에 ALL이라는 것도 추가하기 위해 combobox에 들어갈 리스트에 ALL추가
        globals()['combobox{}'.format(value1)] = tk.ttk.Combobox(frame1, values=list3, state="readonly")
        globals()['combobox{}'.format(value1)].pack(side='left')
        globals()['combobox{}'.format(value1)].set('선택가능')  # 기본값은 선택가능, combobox의 list는 row/column 리스트
    labelblank1 = tk.Label(frame, text='                                                   ')
    labelblank1.pack(side='top', anchor='w')
  frame2 = tk.Frame(root)
  frame2.pack(side='top', anchor='w')
  labelblank2 = tk.Label(frame2, text='                 ')
  labelblank2.pack(side='left', anchor='w')
  for h in ['IV', 'TR', 'Ref_fit', 'Tr_flatten']:
    globals()['var_select{}'.format(h)] = tk.BooleanVar()  # 상태를 True/Farse 형태로 저장한다는 말.
    globals()['checkbox_select{}'.format(h)] = tk.Checkbutton(frame2, text=h,
                                                              variable=globals()['var_select{}'.format(h)])

    globals()['checkbox_select{}'.format(h)].pack(side='left', anchor='w')  # 체크박스를 띄우고 위치를 지정

  def show_selected():
    global selected
    d = 0
    which = 0
    csv = 0
    selected = []
    for key in data:
      values = data[key]
      for value1 in values:
        var = globals()['var{}'.format(value1)]
        c = globals()['combobox{}'.format(value1)]
        # 순회하며 특정 체크박스의 값이 True인지, combobox에서 선택된 값이 있는지 체크
        if var.get() == True and c.get() != '선택가능':
          d += 1
          # 체크 된 값이 있다면 유효한 선택이 있었다는 횟수 d를 1올리고 최종 선택 리스트에 key, value1, 콤보박스 설정값을 추가.
          selected.append((key, value1, c.get()))
        elif var.get() == True and c.get() == '선택가능':  # 날짜는 선택되었지만 콤보박스가 설정되지 않았다면 오류메시지 띄움
          d+=1
          messagebox.askokcancel("Warning", "선택된 날짜의 row/column 설정되지 않았습니다.")

          selected = []
    for h in ['IV', 'TR', 'Ref_fit', 'Tr_flatten']:
      if globals()['var_select{}'.format(h)].get() == True:
        which += 1
        # 체크 된 값이 있다면 유효한 선택이 있었다는 횟수 which를 1올리고 최종 선택 리스트에 key, value1, 콤보박스 설정값을 추가.
        selected.append(h)



    if d == 0 or which == 0:
      messagebox.askokcancel("Warning", "선택된 파일/ 그래프 형태가 없습니다.")
      selected = []

    elif d != 0 or which != 0:
      print(selected)
      #gs.graph(selected)
      #plt.show()



  # 확인 버튼 생성
  labelblank3 = tk.Label(root, text='    ')
  labelblank3.pack(side='top', anchor='w')
  #frame3 = tk.Frame(root)
  #frame3.pack(side='top', anchor='w')
  labelblank3 = tk.Label(root, text='    ')
  labelblank3.pack(side='left', anchor='w')
  button1 = tk.Button(root, text="confirm", command=show_selected,font=("Roboto", 10))
  button1.pack(side='left')
  labelblank3 = tk.Label(root, text='    ')
  labelblank3.pack(side='left', anchor='w')
  button2 = tk.Button(root, text="Exit", command=root.destroy,font=("Roboto", 10))
  button2.pack(side='left')
  labelblank3 = tk.Label(root, text='    ')
  labelblank3.pack(side='left', anchor='w')
  button3 = tk.Button(root, text="clear res", command=dc.delete,font=("Roboto", 10))
  button3.pack(side='left')
  labelblank3 = tk.Label(root, text='    ')
  labelblank3.pack(side='left', anchor='w')
  button4 = tk.Button(root, text="create_csv_file", command=prc.create_csv,font=("Roboto", 10))
  button4.pack(side='left')

  # Tkinter 창 실행
  root.mainloop()
  return


GUI()  # 일단 에프오 눌러서 실행은 되야하니깐! 나중에 모듈 호출할때는 제거?
