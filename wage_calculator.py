# coding:utf-8
"""
背景：以前需要人为手动的计算每一个老师的点评条数，很是繁琐，所以开发此工具，提高工作效率。
功能：输入日期，老师姓名，自动计算时间段内的点评数目。
"""

from tkinter.messagebox import *
from tkinter.filedialog import *
import datetime
from bs4 import BeautifulSoup
import requests
import csv


def get_screen_size(master, window_x, window_y):  # 获取屏幕位置，使窗口居中
    screen_width = master.winfo_screenwidth()  # 获取屏幕 宽、高
    screen_height = master.winfo_screenheight()

    x = (screen_width // 2) - (window_x // 2)  # 计算 x, y 位置
    y = (screen_height // 2) - (window_y // 2)
    return x, y


def calculate_time():  # 计算日期
    today = datetime.datetime.now()  # 今天的日期
    delta1 = datetime.timedelta(days=0)  # 昨天的日期
    yesterday = today + delta1
    delta7 = datetime.timedelta(days=-7)
    last_monday = today + delta7
    yesterday_format = yesterday.strftime('%Y-%m-%d')
    last_monday_format = last_monday.strftime('%Y-%m-%d')
    return yesterday_format, last_monday_format


def select_path(path):  # 选择保存文件夹
    directory = askdirectory()
    path.set(directory)


def search_teacher(teacher_entry, path_entry, start_entry, stop_entry):  # 搜索某一个老师的所有点评记录
    teacher_name = teacher_entry.get()
    directory = path_entry.get()
    str_start_time = start_entry.get()
    str_stop_time = stop_entry.get()
    start_time = datetime.datetime.strptime(str_start_time, '%Y-%m-%d')
    stop_time = datetime.datetime.strptime(str_stop_time, '%Y-%m-%d')

    if teacher_name == '':
        showwarning('警告', '请输入老师名字！')
    elif directory == '':
        showwarning('警告', '请选择数据保存位置！')
    else:
        global content
        content = s.post('http://*****.taotaoenglish.com/Read/MemberIndex', {'teacherName': teacher_name})
        # global total_len
        # total_len = 0
        global review_dict
        review_dict = {}

        def next_page(next):

            bs = BeautifulSoup(next.text, 'lxml')

            for text in bs.find_all('a'):  # 获得下一页的链接
                if text.get_text() == '下一页':
                    link = text['href']
                    next = s.get('http://*****.taotaoenglish.com' + link)

            title = []

            for th in bs.find_all('th'):  # 获取所有的标题
                title.append(th.get_text())

            if bs.find_all('td'):  # 如果不为空，则执行。为空的情况是，例如一个新老师‘YIYI'，记录不多，有可能在时间段内无记录

                for tr in bs.find_all('tr'):  # 获取当页所有的点评记录

                    single_student = []  # 保存的只是一条记录

                    for td in tr.find_all('td'):  # 获取评论详情的链接或者点评记录，这只是一条记录
                        if td.get_text() == '评论详情':
                            a = td.find('a')
                            link = a['href']
                            single_student.append(link)
                        else:
                            single_student.append(td.get_text())

                    if single_student:  # 如果记录不为空，那么就判断点评时间是否在开始和截止时间内
                        review_time = datetime.datetime.strptime(single_student[3], '%Y-%m-%d %H:%M')
                        if start_time <= review_time <= stop_time:
                            # 如果在时间段内，就把这一条记录加入字典，以字典的形式可以保证，
                            # 每一条记录都独一无二，因为键不重复，而这里面的键是评论详情的链接
                            #
                            review_dict[single_student[4]] = single_student[0:4]

                if review_time < start_time:
                    pass
                else:
                    next_page(next)

        next_page(content)

        with open(directory + '/' + teacher_name + '.csv', 'a', encoding='GB18030',
                  newline='') as f:  # 每一位老师的点评记录
            everyone_writer = csv.writer(f)
            for key, value in review_dict.items():
                value.append(key)
                everyone_writer.writerow(value)
        with open(directory + '/' + str_start_time + ' ' + str_stop_time + '.csv', 'a', encoding='GB18030',
                  newline='') as total:
            total_writer = csv.writer(total)
            list = [teacher_name, len(review_dict)]
            total_writer.writerow(list)


def gui_main(x, y, start_time, stop_time, path):
    root.title('点评工资计算器')
    root.geometry('300x300+{}+{}'.format(x, y))

    start_frame = Frame(root)  # 开始日期
    start_label = Label(start_frame, text='开始日期')
    start_label.pack(side=LEFT, anchor=CENTER, padx=5, pady=5)
    start_entry = Entry(start_frame)  # 文本输入框
    start_entry.delete(0, END)
    start_entry.insert(0, start_time)
    start_entry.pack(side=LEFT)
    start_frame.pack(fill=X)

    stop_frame = Frame(root)  # 结束日期
    stop_label = Label(stop_frame, text='结束日期')
    stop_label.pack(side=LEFT, anchor=CENTER, padx=5, pady=5)
    stop_entry = Entry(stop_frame)  # 文本输入框
    stop_entry.delete(0, END)
    stop_entry.insert(0, stop_time)
    stop_entry.pack(side=LEFT)
    stop_frame.pack(fill=X)

    path_frame = Frame(root)  # 保存位置
    path_label = Label(path_frame, text='保存位置')  # 保存位置文本
    path_label.pack(side=LEFT, anchor=CENTER, padx=5, pady=5)
    path_entry = Entry(path_frame, textvariable=path)  # 文本输入框
    path_entry.pack(side=LEFT)
    path_button = Button(path_frame, text='选择', command=lambda: select_path(path))  # 选择按钮
    path_button.pack(side=LEFT, padx=10)
    path_frame.pack(fill=X)

    teacher_frame = Frame(root)
    teacher_label = Label(teacher_frame, text='老师姓名')
    teacher_label.pack(side=LEFT, anchor=CENTER, padx=5, pady=5)
    teacher_entry = Entry(teacher_frame)  # 文本输入框
    teacher_entry.pack(side=LEFT)

    teacher_frame.pack(fill=X)

    search_frame = Frame(root)
    search_frame.pack()
    search_button = Button(search_frame, text='搜索',
                           command=lambda: search_teacher(teacher_entry, path_entry, start_entry, stop_entry))  # 选择按钮
    search_button.pack(side=LEFT, padx=10)

    root.mainloop()


def main():
    global root
    global s
    root = Tk()
    xy = get_screen_size(root, 300, 300)  # 窗口初始化位置
    time = calculate_time()

    s = requests.session()
    params = {'UserName': '***', 'Password': '****'}
    login_page = 'http://*****.taotaoenglish.com/'
    s.post(login_page, params)

    path = StringVar()
    gui_main(xy[0], xy[1], time[1], time[0], path)


if __name__ == '__main__':
    main()
