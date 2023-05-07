# 라이브러리 import
with open('library.txt','r') as f:
    for library in f:
        exec(library)
import os
from tkinter import *
from tkinter.ttk import *

root = Tk()
root.geometry("400x400")

# wafer and date combobox widgets
wafer_cb = Combobox(root)
date_cb = Combobox(root)

# function to update date combobox based on selected wafer
def update_date(*args):
    wafer_path = os.path.join("dat", wafer_cb.get())
    date_list = [f for f in os.listdir(wafer_path) if os.path.isdir(os.path.join(wafer_path, f))]
    date_cb['values'] = date_list

# set wafer combobox values
wafer_path = os.path.join('..','dat')
wafer_list = [f for f in os.listdir(wafer_path) if os.path.isdir(os.path.join(wafer_path, f))]
wafer_cb['values'] = wafer_list
print(wafer_list)
wafer_cb.current(0)

# bind update_date function to wafer combobox selection
wafer_cb.bind("<<ComboboxSelected>>", update_date)

# pack widgets
wafer_cb.pack()
date_cb.pack()

root.mainloop()