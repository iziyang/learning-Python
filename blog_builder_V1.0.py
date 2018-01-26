# coding:utf-8

from tkinter.messagebox import *
from tkinter.filedialog import *
import os
from os import system


def get_screen_size(master, window_x, window_y):
    screen_width = master.winfo_screenwidth()  # 获取屏幕 宽、高
    screen_height = master.winfo_screenheight()

    x = (screen_width // 2) - (window_x // 2)  # 计算 x, y 位置
    y = (screen_height // 2) - (window_y // 2)
    return x, y


def build_article():
    article_name = entry.get()
    # os.chdir('G:\\blog')

    new_command = 'cd G:\\blog && hexo new "{}"'.format(article_name)
    system(new_command)
    open_command = 'cd G:\\blog\\source\\_posts && {}.md'.format(article_name)
    system(open_command)
    # os.chdir('G:\\blog\\source\\_posts')
    # system('cd G:\\blog\\source\\_posts && {}.md'.format(article_name))


def publish_article():
    os.chdir('G:\\blog')
    system('hexo g -d')


if __name__ == '__main__':
    try:
        root = Tk()
        root.title('博客发表')
        xy = get_screen_size(root, 300, 50)  # 窗口初始化位置
        root.geometry('300x50+{}+{}'.format(xy[0], xy[1]))

        frame = Frame(root)
        label = Label(frame, text='文章')
        label.pack(side=LEFT, anchor=CENTER, padx=5, pady=5)
        entry = Entry(frame)  # 文本输入框
        # entry.delete(0, END)
        # entry.insert(0, frame)
        entry.pack(side=LEFT)

        build_button = Button(frame, text='生成', command=build_article)
        build_button.pack(side=LEFT, padx=10)

        publish_button = Button(frame, text='部署', command=publish_article)
        publish_button.pack(side=BOTTOM, pady=10)
        frame.pack(fill=X)

        root.mainloop()
    except EXCEPTION:
        showinfo('异常', EXCEPTION)
    finally:
        sys.exit()
