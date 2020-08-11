#!/usr/bin/python
# -*- coding: utf-8 -*-


import thread
import threading
import socket
import os


def broadcast_udp():
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	sock.settimeout(5)

	server_address = ('255.255.255.255', 34658)

	try:
		print '[*] Buscando servidor na rede local... [*]'
		sent = sock.sendto('', server_address)
		data, server = sock.recvfrom(4096)
		print 'Conectado em:',server[0]
		return str(server[0])
	except socket.timeout:
		print "[!] Servidor na rede local não encontrado [!] \n[*] Conectando-se em: 'jogodaforca.ddns.net' [*]"
		return 'jogodaforca.ddns.net'
	finally:
		sock.close()



def receber(socket):
    while True:
        msg = socket.recv(1024)
        if not msg:
        	os._exit(1)
        	break
        print msg


host = broadcast_udp()
port = 4444


try:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host, port))

	receiver = threading.Thread(target=receber, args=[s])
	receiver.daemon = True
	receiver.start()

	while True:
	    msg = raw_input()
	    s.send(msg)

except KeyboardInterrupt:
	s.close()
