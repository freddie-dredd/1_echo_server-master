import socket, time, datetime

sock = socket.socket()
data_volume = 1024
txtLogs = False

def print_info(string):
	if txtLogs:
		with open("server_log.txt", 'a') as logFile:
			logFile.write(f"{datetime.datetime.now()}    " + string + '\n')
	else:
		print(string)


def findPort():
	port = 9090
	print_info(f"Проверка порта {port}")
	try:
		sock.bind(('', port))
	except OSError:
		print_info(f"Ошибка: порт {port} занят, поиск свободного порта")
		sock.bind(('', 0))


def clientAuth(conn, addr):
	print_info(f"Попытка аутентификации клиента {addr[0]}")
	with open("clients.txt", 'r+') as clients:

		findClient = False

		for l in clients.readlines():
			if addr[0] == l:
				findClient = True

				conn.send("AuthTrue".encode())
				conn.send(f"Привет {addr[0]}".encode())
				print_info(f"Клиент {addr[0]} найден")
				return True

		if findClient == False:
			print_info(f"Запись клиента в whitelist {addr[0]}")
			clients.write(f"\n{addr[0]}")




def clientEcho():
	msg = ''

	try:
		print(sock.getsockname()[1])
		print_info(f"Начало прослушивания порта {sock.getsockname()[1]}")
		sock.listen(1)

		conn, addr = sock.accept()
		clientAuth(conn, addr)

		print_info(f"Подключение клиента {addr}")

		while True:
			data = conn.recv(data_volume)
			print_info(f"	Принято {data_volume} байт")

			if not data:
				print_info(f"Отключение клиента")
				conn.close()
				break


			msg += data.decode()
			conn.send(data.upper())
			print_info(f"	От клиента принято сообщение: {data.decode()}")

	except OSError:
		print_info(f"Клиент {addr} разорвал соединение")
		clientEcho()
		time.sleep(1)


print_info(f"Запуск севера")

findPort()
clientEcho()

print_info(f"Отключение сервера")





