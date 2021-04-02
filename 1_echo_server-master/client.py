import socket, time

port = 9090
host = 'localhost'
attempts_to_connect = 1
sock = socket.socket()

check = False
print("Введите порт (Введите пустую строку: 9090 - по умолчанию)")
while not check:
    port = input(" --> ")
    if port:
        if int(port) <= 1023 or int(port) > 65535:
            print("Укажите верный номер порта")
        else:
            check = True
    else:
        check = True
        port = 9090

check = False
print("Введите хост (Введите пустую строку: localhost - по умолчанию)")
while not check:
    host = input(" --> ")
    if host:
        if type(host) != str:
            print("Укажите верный номер порта")
        else:
            check = True
    else:
        check = True
        host = 'localhost'






print(f"Соединение с сервером, {port}")


while attempts_to_connect < 10:
    try:
        sock.connect((host, int(port)))
        print("Успешное подключение")
        attempts_to_connect = 10
        massage = ''
        while massage != "exit":
            try:
                massage = input("Сообщение серверу --> ")
                print(f"Отправка данных серверу, порт {port}")
                sock.send(massage.encode())
            except:
                print("ConnectionResetError: [WinError 10054] Удаленный хост принудительно разорвал существующее подключение")

        print(f"Приём данных от сервера, порт {port}")
        data = sock.recv(1024)

        print("Разрыв соединения с сервером")
        sock.close()

        print(data.decode())

    except ConnectionRefusedError:
        print(f"Попытка соединения {attempts_to_connect}/10")
        print("Подключение не установлено, т.к. конечный компьютер отверг запрос на подключение")
        time.sleep(1)
        attempts_to_connect += 1






