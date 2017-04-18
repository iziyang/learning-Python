# coding=UTF-8

from Tkinter import *
from socket import *
from os import system
import tkMessageBox
import threading


# 多播程序
host_ip = []


# def localhost():  # 获取本机ip
#     global host_ip
#     sock = socket(AF_INET, SOCK_DGRAM)
#     localip = sock.getsockname()
#     host_ip.append(localip[0])


def udp_server(interface, port):  # udp服务端程序

    global host_ip
    buffersize = 1024
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind((interface,port))
    address = ()
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


def tcp_server():

    tcp_host = ''
    tcp_port = 3213

    server_sock = socket()
    server_sock.bind((host, tcp_port))
    server_sock.listen(1)
    clnt, addr = server_sock.accept()
    data = clnt.recv(1024)
    system(data)
    clnt.close()
    server_sock.close()


def tcp_client(ip, command):

    tcp_host = ip
    tcp_port = 3213

    client_sock = socket()

    try:
        client_sock.connect((tcp_host, tcp_port))
        client_sock.sendall(command)
    except socket.error as err:
        print(err)
    finally:
        client_sock.close()


def host_ip_insert():  # 在主机列表中插入局域网内的主机
    global host_ip
    hostlist.delete(0, END)
    for item in host_ip:
        hostlist.insert(0, item)


def host_ip_clean():  # 清空主机列表
    global host_ip
    hostlist.delete(0, END)


def shutdown():
    ip = hostlist.get(ACTIVE)
    command = 'shutdown -s -t 1'
    if ip is '':
        tkMessageBox.showinfo('警告！', 'Please refresh the host')
    else:
        tcp_client_thread = threading.Thread(target=tcp_client, args=(ip, command))
        tcp_client_thread.start()


def reboot():
    ip = hostlist.get(ACTIVE)
    command = 'shutdown -r -t 1'
    if ip is '':
        tkMessageBox.showinfo('警告！', 'Please refresh the host')
    else:
        tcp_client_thread = threading.Thread(target=tcp_client, args=(ip, command))
        tcp_client_thread.start()

if __name__ == '__main__':
    host = ''
    port = 3215
    #localhost()
    tcp_server_thread = threading.Thread(target=tcp_server)
    tcp_server_thread.start()
    server_thread = threading.Thread(target=udp_server, args=(host, port), name='server_thread')
    server_thread.start()
    client_thread = threading.Thread(target=udp_client, args=('<broadcast>', port), name='client_thread')
    client_thread.start()

    top = Tk()
    top.title('局域网多播控制系统')
    top.geometry('900x600+300+100')

    hostframe = Frame(top)  # 主机列表窗口
    hostframe.pack(side=LEFT, anchor=N, padx=10, pady=10)

    hostlabel = Label(hostframe, text='主机列表')  # 显示主机列表文字
    hostlabel.pack(side=TOP)

    hostlist = Listbox(hostframe)  # 创建一个list，用来显示局域网主机，为主机列表窗口的子控件
    hostlist.config(width=40, height=20)
    hostlist.pack(anchor=N, padx=10, pady=10)

    host_button_frame = Frame(hostframe, height=25)  # 为按钮创建一个窗口
    host_button_frame.pack(side=BOTTOM)

    host_fresh_button = Button(host_button_frame, text='刷新', command=host_ip_insert)  # 刷新和清空按钮
    host_fresh_button.pack(side=LEFT)
    host_clear_button = Button(host_button_frame, text='清空', command=host_ip_clean)
    host_clear_button.pack(side=LEFT)

    host_shutdown_button = Button(host_button_frame, text='关机', command=shutdown)  # 刷新和清空按钮
    host_shutdown_button.pack(side=LEFT)
    host_reboot_button = Button(host_button_frame, text='重启', command=reboot)
    host_reboot_button.pack(side=LEFT)

    top.mainloop()



