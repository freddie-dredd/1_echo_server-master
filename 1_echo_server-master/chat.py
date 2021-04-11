import socket
import threading
import queue
import sys
import random
import os

d = '000'

#Client Code
def ReceiveData(sock):
    global d
    while True:
        try:
            data,addr = sock.recvfrom(1024)
            print(data.decode('utf-8'))
            d = data.decode()
        except:
            pass

def RunClient(serverIP):
    global d
    host = socket.gethostbyname(socket.gethostname())
    port = random.randint(6000,10000)
    print('Client IP->'+str(host)+' Port->'+str(port))
    server = (str(serverIP),5000)
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.bind((host,port))

    name = input('Please write your name here: ')
    if name == '':
        name = 'Guest'+str(random.randint(1000,9999))
        print('Your name is:'+name)
    s.sendto(name.encode('utf-8'),server)
    threading.Thread(target=ReceiveData,args=(s,)).start()
    while True:
        if d == 'cstop':
            break
        data = input()
        if data == 'qqq' or data == 'sstop':
            break
        elif data=='':
            continue
        data = '['+name+']' + '->'+ data
        s.sendto(data.encode('utf-8'),server)
    s.sendto(data.encode('utf-8'),server)
    s.close()
    os._exit(1)
#Client Code Ends Here


#Server Code
def RecvData(sock,recvPackets):
    while True:
        data,addr = sock.recvfrom(1024)
        recvPackets.put((data,addr))

def RunServer():
    host = socket.gethostbyname(socket.gethostname())
    port = 5000
    print('Server hosting on IP-> '+str(host))
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.bind((host,port))
    clients = set()
    recvPackets = queue.Queue()

    print('Server Running...')

    threading.Thread(target=RecvData,args=(s,recvPackets)).start()

    while True:
        while not recvPackets.empty():
            data,addr = recvPackets.get()
            if addr not in clients:
                clients.add(addr)
                continue
            clients.add(addr)
            data = data.decode('utf-8')
            if 'sstop' in data:
                for c in clients:
                    if c!=addr:
                        s.sendto('cstop'.encode('utf-8'),c)
                s.close()
                os._exit(1)
            if data.endswith('qqq'):
                clients.remove(addr)
                continue
            print(str(addr)+data)
            for c in clients:
                if c!=addr:
                    s.sendto(data.encode('utf-8'),c)
    s.close()
#Serevr Code Ends Here

if __name__ == '__main__':
    if len(sys.argv)==1:
        RunServer()
    elif len(sys.argv)==2:
        RunClient(sys.argv[1])
    else:
        print('Run Serevr:-> python Chat.py')
        print('Run Client:-> python Chat.py <ServerIP>')