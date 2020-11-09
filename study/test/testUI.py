from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo
frameT = Tk()
frameT.geometry('500x200+400+200')
frameT.title('选择需要输入处理的文件')
frame = Frame(frameT)
frame.pack(padx=10, pady=10)  # 设置外边距
frame_1 = Frame(frameT)
frame_1.pack(padx=10, pady=10)  # 设置外边距
frame1 = Frame(frameT)
frame1.pack(padx=10, pady=10)
v1 = StringVar()
v2 = StringVar()
ent = Entry(frame, width=50, textvariable=v1).pack(fill=X, side=LEFT)  # x方向填充,靠左
ent = Entry(frame_1, width=50, textvariable=v2).pack(fill=X, side=LEFT)  # x方向填充,靠左


def fileopen():
    file_sql = askopenfilename()
    if file_sql:
        v1.set(file_sql)


def fileopen_1():
    file_YuD = askopenfilename()
    if file_YuD:
        v2.set(file_YuD)

def match():
    print(v1.get(), v2.get())
    pass

btn = Button(frame, width=20, text='总文件', font=("宋体", 14), command=fileopen).pack(fil=X, padx=10)
btn_1 = Button(frame_1, width=20, text='匹配文件', font=("宋体", 14), command=fileopen_1).pack(fil=X, padx=10)
ext = Button(frame1, width=10, text='运行', font=("宋体", 14), command=match).pack(fill=X, side=LEFT)
etb = Button(frame1, width=10, text='退出', font=("宋体", 14), command=frameT.quit).pack(fill=Y, padx=10)
frameT.mainloop()