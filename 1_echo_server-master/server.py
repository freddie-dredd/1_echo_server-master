import socket, time, datetime

sock = socket.socket()
port = 9090
data_volume = 1024
txtLogs = True


def print_info(string):
	if txtLogs:
		with open("server_log.txt", 'a') as logFile:
			logFile.write(f'[{datetime.datetime}]' + string + '\n')
	else:
		print(string)


def clientEcho():
	msg = ''

	try:
		print_info(f"Начало прослушивания порта {port}")
		sock.listen(1)

		conn, addr = sock.accept()
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

	except:
		print_info(f"Клиент разорвал соединение")
		clientEcho()
		time.sleep(1)


print_info(f"Запуск севера")
sock.bind(('', port))

clientEcho()

print_info(f"Отключение сервера")





