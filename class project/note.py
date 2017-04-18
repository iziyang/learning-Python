# coding=utf-8
from Tkinter import *
from tkMessageBox import *
from tkFileDialog import *
import os

filename = ''
text = ''
# 关于
def author():
    showinfo('作者信息', '本软件由北子设计制作')


def about():
    showinfo('版权', '本软件版权归属于北子')
# 文件菜单
#打开
def openfile():
    global filename
    filename = askopenfilename(defaultextension='.txt')
    if filename == '':
        filename = None
    else:
        root.title('FileName:'+os.path.basename(filename))
        text_pad.delete(1.0, END)  # 1.0表示第一行的0列，即文本的开头
        f = open(filename, 'r+')
        text_pad.insert(1.0,f.read())
        f.close()

def save():
    global filename
    try:
        f = open(filename, 'w')
        msg = text_pad.get(1.0, END)
        f.write(msg)
        f.close()
    except:
        saveas()

# 新建
def newfile():
    global filename
    root.title('未命名文件')
    filename = None
    text_pad.delete(1.0, END)


def saveas():
    f = askopenfilename(initialfile="未命名.txt", defaultextension='.txt')
    global filename
    filename = f
    fh = open(f, 'w')
    msg = text_pad.get(1.0,END)
    fh.write(msg)
    fh.close()
    root.title('FileName:'+os.path.basename(f))


def cut():
    text_pad.event_generate('<<Cut>>')


def copy():
    text_pad.event_generate('<<Copy>>')


def paste():
    text_pad.event_generate('<<Paset>>')


def redo():
    text_pad.event_generate('<<Redo>>')


def undo():
    text_pad.event_generate('<<Undo>>')


def select_all():
    text_pad.tag_add('sel', '1.0', END)


def find():
    global text
    topsearch = Toplevel(root)
    topsearch.title('查找')
    topsearch.geometry('300x30+200+250')
    label1 = Label(topsearch,text='Find')
    label1.grid(row=0, column=0,padx=5)
    entry1 = Entry(topsearch,width=20)
    entry1.grid(row=0, column=1, padx=5)
    button1 = Button(topsearch, text="查找", command=search)
    button1.grid(row=0, column=2)
    text = entry1.get()


def search():
    global text
    start = 1.0
    # while True:
    pos = text_pad.search(text, start, stopindex=END)
    # if not pos:
    #         break
    text_pad.tag_add('sel', pos)
#    start = pos + "+1c"




root = Tk()
root.title('little note')
root.geometry("800x500+100+100")  # 构建矩形窗体（几何），500×500大小，初始位置100,100

# Creat Menu
menubar = Menu(root)
root.config(menu=menubar)

filemenu = Menu(menubar)
filemenu.add_command(label='新建', accelerator='Ctrl + N', command=newfile)
filemenu.add_command(label='打开', accelerator='Ctrl + O', command=openfile)
filemenu.add_command(label='保存', accelerator='Ctrl + S', command=save)
filemenu.add_command(label='另存为', accelerator='Ctrl + Shift + S', command=saveas)
menubar.add_cascade(label='文件', menu=filemenu)

editmenu = Menu(menubar)
editmenu.add_command(label='撤销', accelerator='Ctrl + Z', command=undo)
editmenu.add_command(label='重做', accelerator='Ctrl + Y', command=redo)
editmenu.add_separator()
editmenu.add_command(label='剪切', accelerator='Ctrl + X', command=cut)
editmenu.add_command(label='复制', accelerator='Ctrl + C', command=copy)
editmenu.add_command(label='粘贴', accelerator='Ctrl + V', command=paste)
editmenu.add_separator()
editmenu.add_command(label='查找', accelerator='Ctrl + F', command=find)
editmenu.add_command(label='全选', accelerator='Ctrl + A', command=select_all)
menubar.add_cascade(label='编辑', menu=editmenu)

aboutmenu = Menu(menubar)
aboutmenu.add_command(label='作者', command=author)
aboutmenu.add_command(label='版权', command=about)
menubar.add_cascade(label='关于', menu=aboutmenu)

toolbar = Frame(root, height=25, bg='light sea green')
short_button = Button(toolbar,text='打开', command=openfile)
short_button.pack(side=LEFT, padx=5, pady=5)
short_button = Button(toolbar,text='保存', command=save)
short_button.pack(side=LEFT)
toolbar.pack(expand=NO, fill=X)

status = Label(root, text='Ln20', bd=1, relief=GROOVE, anchor=W)
status.pack(side=BOTTOM, fill=X)

lnlaber = Label(root, width =2, bg='antique white')
lnlaber.pack(side=LEFT, fill=Y)

text_pad = Text(root, undo=True)
text_pad.pack(expand=YES, fill=BOTH)

scoll = Scrollbar(text_pad)
text_pad.config(yscrollcommand=scoll.set)
scoll.config(command=text_pad.yview)
scoll.pack(side=RIGHT, fill=Y)

root.mainloop()
