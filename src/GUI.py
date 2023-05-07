# 라이브러리 import
with open('library.txt','r') as f:
    for library in f:
        exec(library)
# import * -> tkinter module에 있는 모든 변수화 함수를 현재 네임 스페이스로 가져옮

# wafer = ''
# date = ''
# position = ''
# sort_graph = ''
# wafer_options = ''
date_dict = ''
def on_wafer_change(*args): # 기본적으로 trace로 함수를 호출하는 경우 인자로 3개 인자(변수 이름, 이전 값, 변경 값)
    global date_dict
    label = Label(root, text = 'choose date')
    wafer_path = os.path.join('..','dat',selected_wafer.get())
    dates = [f for f in os.listdir(wafer_path) if os.path.isdir(os.path.join(wafer_path,f))]
    date_options = [f.split('_')[0] for f in dates]
    date_dict = dict(zip(date_options,dates))
    print(date_dict)
    selected_date.set(date_options[0])
    option_menu_date = OptionMenu(root, selected_date, *date_options)
    option_menu_date.pack()
    label.pack()
    selected_date.trace('w',on_date_changes)
def on_date_changes(*args):
    label = Label(root, text = 'choose position')
    position_path = os.path.join('..','dat',selected_wafer.get(),date_dict[selected_date.get()])
    position_options = [f.split('_')[2] for f in os.listdir(position_path) if '_LMZ' in f and f.endswith('xml')]
    selected_position.set(position_options[0])
    option_menu_position = OptionMenu(root, selected_position, *position_options)
    option_menu_position.pack()
    label.pack()

def get_date(*args):
    global date
    date = selected_date.get()
    print(date)
def get_position(*args):
    global position
    position = selected_position.get()
def get_graph_chosen():
    global sort_graph
    selected_graph = lb.curselection()
    for index in selected_graph:
        sort_graph.append(lb.get(index))
def get_date_options():
    global wafer_options
    selected_wafer = wafer
    date_options = [f for f in os.listdir(os.path.join('..', 'dat', selected_wafer)) if
                    os.path.isdir(os.path.join('..', 'dat', selected_wafer, f))]
    return date_options

root = Tk() # Tk() class를 호출하여 빈 윈도우를 생성
root.title('Python-based data analysis software')
root.geometry('800x600+500+200')

# 사용자로부터 입력 받은 값을 넣을 var 변수 -> get을 이용하여 변수에 접근
selected_wafer = StringVar()
selected_date = StringVar()
selected_position = StringVar()
selected_graph = StringVar()
# 각 변수에 변화가 생길 때 마다 trace로 함수를 실행하여 변수에 접근하여 값 계속 최신화

selected_date.trace('w',get_date)
selected_position.trace('w',get_position)
selected_graph.trace('w',get_graph_chosen)
#---------------------------------------------------------------------------------------------------------------------------
label = Label(root, text='choose wafer')

wafer_options = [f for f in os.listdir(os.path.join('..','dat')) if os.path.isdir(os.path.join('..','dat',f))]
selected_wafer.set(wafer_options[0])
selected_wafer.trace('w',on_wafer_change)
option_menu = OptionMenu(root,selected_wafer,*wafer_options)
label.pack()
option_menu.pack()
#-----------------------------------------------------------------------------------------------------------------------------
'''
# 날짜 메뉴
label = Label(root, text='choose date')
date_options = ['QEW','123','143']
option_menu = OptionMenu(root, selected_date, *date_options)
label.pack()
option_menu.pack()
'''
# label = Label(root, text='choose date')
#
# date_options = [f for f in os.listdir(os.path.join('..','dat',wafer)) if os.path.isdir(os.path.join('..','dat',wafer,f))]
# option_menu = OptionMenu(root,selected_date,*date_options)
# label.pack()
# option_menu.pack()
#
#
# label = Label(root, text = 'Optical modulator')
# label.pack()

button = Button(root, text='확인', command = get_date)
button.pack()

label = Label(root, text = 'choose graph')
lb = Listbox(root, selectmode='multiple', width=20, height=4)
lb.pack()

lb.insert(END,'IV')
lb.insert(END,'IV_fitted')
lb.insert(END,'Transmission')
lb.insert(END,'Transmission_fitted')

root.mainloop() # GUI를 보여주는 코드
# print(wafer)

# print(wafer)

# 변수에 접근한 시점이 var 변수가 변경되는 시점 -> 사용자 액션에 의해 값을 가져오는 게 좋음( 선택한 값을 즉시 반영하지 못할 수 있음)