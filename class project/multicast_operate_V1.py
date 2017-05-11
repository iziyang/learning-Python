# coding=UTF-8

from Tkinter import *
from socket import *
from os import system
from SocketServer import StreamRequestHandler as SRH
import tkMessageBox, threading, wmi, platform, psutil, SocketServer, pythoncom, time, ctypes


def udp_server(interface, port):  # udp服务端程序
    buffersize = 1024
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind((interface,port))
    while True:
        data, address = sock.recvfrom(buffersize)
        if address[0] not in host_ip:
            host_ip.append(address[0])


def udp_client(network, port):  # udp客户端程序
    while True:
        client_sock = socket(AF_INET, SOCK_DGRAM)
        client_sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        client_text = 'Broadcast datagram!'
        client_sock.sendto(client_text.encode('utf-8'), (network, port))


def tcp_socket_server():
    ip = ''
    port = 5255
    addr = (ip, port)

    class Servers(SRH):
        def handle(self):
            # print 'got connection from ', self.client_address

            while True:
                command = self.request.recv(1024)
                if not command:
                    break
                elif 'var' in command:
                    match = re.findall('[0-9a-zA-Z\_]+', command)
                    match.sort()
                    for string in match:

                        if string == 'asys_var':
                            host_system()
                        elif string == 'bmem_var':
                            memory_info()
                        elif string == 'ccpu_var':
                            cpu_info()
                        elif string == 'ddisk_var':
                            disk_info()
                        elif string == 'eboot_var':
                            PID_info()

                    for item in host_info:
                        self.request.send(str(item))
                        time.sleep(0.5)

                else:
                    system(command)

    server = SocketServer.ThreadingTCPServer(addr, Servers)
    server.serve_forever()


def tcp_socket_client(ip, command):
    global tcp_info
    tcp_info = []
    tcp_host = ip
    tcp_port = 5255
    bufsize = 200
    client_sock = socket()
    client_sock.connect((tcp_host, tcp_port))
    client_sock.send(str(command))
    # print threading.current_thread().name
    while True:
        data = client_sock.recv(bufsize)
        # print data
        # print 'This is from data {}'.format(data.decode('utf-8'))
        if data:
            tcp_info.append(data)
        else:
            break
        host_info_display(tcp_info)
    client_sock.close()


def refresh():  # 刷新按钮，在主机列表中插入局域网内的主机

    hostlist.delete(0, END)
    for item in host_ip:
        hostlist.insert(0, item)


def clean():  # 清空按钮，清空主机列表
    global host_ip
    host_ip = []
    hostlist.delete(0, END)


def shutdown():  # 关机按钮
    ip = hostlist.get(ACTIVE)

    command = 'shutdown -s -t 1'
    if ip is '':
        tkMessageBox.showinfo('警告！', '没有选定主机！')
    else:
        if tkMessageBox.askyesno('警告！', '此电脑将会关机！'):

            tcp_client_thread = threading.Thread(target=tcp_socket_client, args=command)
            tcp_client_thread.setDaemon(True)
            tcp_client_thread.start()


def reboot():  # 重启按钮
    ip = hostlist.get(ACTIVE)
    command = 'shutdown -r -t 1'
    if ip is '':
        tkMessageBox.showinfo('警告！', '没有选定主机！')
    else:
        if tkMessageBox.askyesno('警告！', '此电脑将会重启！'):

            tcp_client_thread = threading.Thread(target=tcp_socket_client, args=command)
            tcp_client_thread.setDaemon(True)
            tcp_client_thread.start()


def host_system():
    pythoncom.CoInitialize()
    operate_system = platform.platform()
    cpu_type = platform.processor()
    host_name = platform.node()

    mem_info = psutil.virtual_memory()
    memory_capacity = mem_info.total

    c = wmi.WMI()

    disk_total = 0

    for disk in c.Win32_LogicalDisk(DriveType=3):
        disk_total += int(disk.Size)

    system_info = ('Host Name: ' + host_name, 'OS: ' + str(operate_system), 'CPU: ' + cpu_type,
                   'Memory: ' + str(memory_capacity / 10 ** 9) + 'G', 'Disk: ' + str(disk_total / 2 ** 30) + 'G')
    host_info.append(system_info)


def memory_info():
    mem_info = psutil.virtual_memory()
    mem_capacity = mem_info.total
    mem_used = mem_info.used
    mem_available = mem_info.available
    mem_percent = mem_info.percent
    host_memory_info = ('total: ' + str(mem_capacity / 10 ** 9) + 'G', 'used: ' + str(mem_used / 10 ** 9) + 'G',
                   'avaiable: ' + str(mem_available / 10 ** 9) + 'G', 'percent: ' + str(mem_percent))

    host_info.append(host_memory_info)


def cpu_info():
    cpu_info = psutil.cpu_percent(interval=1, percpu=True)
    cpu_percent = ('The utilization of each CPU: ', cpu_info)

    host_info.append(cpu_percent)


def disk_info():
    pythoncom.CoInitialize()
    c = wmi.WMI()
    host_disk_info = []
    for disk in c.Win32_LogicalDisk(DriveType=3):
        host_disk_info.append((str(disk.Caption), str(int(disk.Size) / 2 ** 30) + 'G',
                                "free %0.2f%%" % (100.0 * long(disk.FreeSpace) / long(disk.Size))))
    host_info.append(host_disk_info)


def PID_info():
    pythoncom.CoInitialize()
    c = wmi.WMI()
    process_info = []
    for process in c.Win32_Process():
        process_info.append((process.ProcessId, process.Name))
    for process in process_info:
        host_info.append(process)


def host_info_display(data):  # 主机信息显示

    info_list.delete(0, END)
    for item in data:
        info_list.insert(END, item)


def search():
    global host_info, tcp_info, a
    host_info = []  # 每次查询都要把主机信息list清空
    tcp_info = []
    ip = hostlist.get(ACTIVE)

    a += 1
    if ip is '':
        tkMessageBox.showinfo('警告！', '没有选定主机！')
    else:
        index = []
        info = {'asys_var':asys_var.get(), 'bmem_var':bmem_var.get(), 'ccpu_var':ccpu_var.get(), 'ddisk_var':ddisk_var.get(), 'eboot_var':eboot_var.get()}
        for value in info.keys():
            if info.get(value):
                index.append(value)

        command = index
        tcp_client_thread = threading.Thread(target=tcp_socket_client, args=(ip, command), name='thread{}'.format(a))
        tcp_client_thread.setDaemon(True)
        tcp_client_thread.start()




if __name__ == '__main__':

    top = Tk()
    top.title('局域网多播控制系统')
    top.geometry('800x400+300+100')

    hostframe = Frame(top)  # 主机列表窗口
    hostframe.pack(side=LEFT, anchor=N, padx=10, pady=10)

    hostlabel = Label(hostframe, text='主机列表')  # 显示主机列表文字
    hostlabel.pack(side=TOP)

    hostlist = Listbox(hostframe)  # 创建一个list，用来显示局域网主机，为主机列表窗口的子控件
    hostlist.config(width=30, height=15)
    hostlist.pack(anchor=N, padx=10, pady=10)

    host_button_frame = Frame(hostframe, height=25)  # 为按钮创建一个窗口
    host_button_frame.pack(side=BOTTOM)

    host_fresh_button = Button(host_button_frame, text='刷新', command=refresh)  # 刷新和清空按钮
    host_fresh_button.pack(side=LEFT)
    host_clear_button = Button(host_button_frame, text='清空', command=clean)
    host_clear_button.pack(side=LEFT)

    host_shutdown_button = Button(host_button_frame, text='关机', command=shutdown)  # 关机和重启按钮
    host_shutdown_button.pack(side=LEFT)
    host_reboot_button = Button(host_button_frame, text='重启', command=reboot)
    host_reboot_button.pack(side=LEFT)

    # 主机信息查询窗口

    info_frame = Frame(top)  # 信息父窗口
    info_frame.pack(side=RIGHT, anchor=N, padx=10, pady=10)

    host_info_frame = Frame(info_frame)  # 信息窗口
    host_info_frame.pack(side=TOP, expand=YES)

    host_display_frame = Frame(info_frame)  # 显示窗口
    host_display_frame.pack(side=TOP)

    info_label = Label(host_info_frame, text='主机信息')
    info_label.pack(side=TOP)

    asys_var = IntVar()
    bmem_var = IntVar()
    ccpu_var = IntVar()
    ddisk_var = IntVar()
    eboot_var = IntVar()

    query_button = Button(host_info_frame, text="查询", command=search)
    query_button.pack(side=BOTTOM)

    cpu_checkbutton = Checkbutton(host_info_frame, text="基本信息", variable=asys_var)
    cpu_checkbutton.pack(side=LEFT)
    mem_checkbutton = Checkbutton(host_info_frame, text="内存详情", variable=bmem_var)
    mem_checkbutton.pack(side=LEFT)
    store_checkbutton = Checkbutton(host_info_frame, text="CPU详情", variable=ccpu_var)
    store_checkbutton.pack(side=LEFT)
    network_checkbutton = Checkbutton(host_info_frame, text="硬盘详情", variable=ddisk_var)
    network_checkbutton.pack(side=LEFT)
    boot_checkbutton = Checkbutton(host_info_frame, text="进程详情", variable=eboot_var)
    boot_checkbutton.pack(side=LEFT)


    #  显示list
    info_list = Listbox(host_display_frame)  # 创建一个list，用来显示主机信息
    info_list_xscrollbar = Scrollbar(host_display_frame, orient=HORIZONTAL)
    info_list_yscrollbar = Scrollbar(host_display_frame)
    info_list_yscrollbar.pack(side=RIGHT, fill=Y)
    info_list.pack(padx=10, pady=10)
    info_list_xscrollbar.pack(side=BOTTOM, fill=X)
    info_list_xscrollbar.config(command=info_list.xview)
    info_list.config(width=70, height=10, yscrollcommand=info_list_yscrollbar.set, xscrollcommand=info_list_xscrollbar.set)
    info_list_yscrollbar.config(command=info_list.yview)

    host_ip = []
    host_info = []
    tcp_info = []
    host = ''
    port = 5000
    a = 0


    #  UDP
    server_thread = threading.Thread(target=udp_server, args=(host, port), name='server_thread')
    server_thread.setDaemon(True)
    server_thread.start()
    client_thread = threading.Thread(target=udp_client, args=('<broadcast>', port), name='client_thread')
    client_thread.setDaemon(True)
    client_thread.start()

    # tcp_socket_server()
    tcp_socket_server_thread = threading.Thread(target=tcp_socket_server, name='tcp_socket_server_thread')
    tcp_socket_server_thread.setDaemon(True)
    tcp_socket_server_thread.start()

    def callback():
        if tkMessageBox.askokcancel("Quit", "Do you really wish to quit?"):
            top.destroy()


    top.protocol("WM_DELETE_WINDOW", callback)

    top.mainloop()


