#!/usr/bin/python
# -*- coding: utf-8 -*-

#dependencias
#sudo apt update -y && sudo apt install zip python python-pip -y && pip install pyfiglet


import socket
import thread
import threading
import random
import string
import pyfiglet


HOST = ''
PORT = 4444

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

orig = (HOST, PORT)

s.bind(orig)
s.listen(1)



def broadcast_udp():
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	server_address = ('', 34658)
	sock.bind(server_address)

	while True:
		data, address = sock.recvfrom(4096)
		sent = sock.sendto('', address)




def forca(erros):
	if erros == 0: return '''
         _ _ _ _
       |/       |
       |        |
       |        |
       |
       |
       |
       |
       |
       |
       |
_ _ _ _|_ _ _ _ _

'''

	if erros == 1: return '''
         _ _ _ _
       |/       |
       |        |
       |       _|_
       |      (___)
       |
       |
       |
       |
       |
       |
_ _ _ _|_ _ _ _ _

'''
	if erros == 2: return '''
         _ _ _ _
       |/       |
       |        |
       |       _|_
       |      (___)
       |        |
       |        |
       |        |
       |
       |
       |
_ _ _ _|_ _ _ _ _

'''
	if erros == 3: return '''
         _ _ _ _
       |/       |
       |        |
       |       _|_
       |      (___)
       |       /|
       |      / |
       |        |
       |
       |
       |
_ _ _ _|_ _ _ _ _

'''
	if erros == 4: return '''
         _ _ _ _
       |/       |
       |        |
       |       _|_
       |      (___)
       |       /|\\
       |      / | \\
       |        |
       |
       |
       |
_ _ _ _|_ _ _ _ _

'''
	if erros == 5: return '''
         _ _ _ _
       |/       |
       |        |
       |       _|_
       |      (___)
       |       /|\\
       |      / | \\
       |        |
       |       /
       |      /
       |
_ _ _ _|_ _ _ _ _

'''
	if erros == 6: return '''
         _ _ _ _
       |/       |
       |        |
       |       _|_
       |      (___)
       |       /|\\
       |      / | \\
       |        |
       |       / \\
       |      /   \\
       |
_ _ _ _|_ _ _ _ _

'''





def conectado(con, cliente):

	def receber():
		return con.recv(1024)

	def enviar(msg):
		con.send(msg)


	def espaco():
  		for x in range(60):
			enviar("\n")


	def game():
		lista = ['Fruta','País','Nome','Cidade']
		dica = random.choice(lista)
		lines = open(dica).read().splitlines()
		secreta = random.choice(lines)

		espaco()
		enviar('[*] JOGO INICIADO [*]')
		enviar(forca(0))

		digitadas = []
		acertos = []
		erros = 0


		while True:
			senha = ''
			for letra in secreta:
				if letra in acertos:
					senha += letra
				elif letra == ' ':
					senha += ' '
				else:
					senha += '-'


			enviar(pyfiglet.figlet_format(senha, font = "standard"))
			enviar("Dica: "+dica.upper()+"\n\n")
			enviar("Tentativas: "+str(digitadas)+"\n")


			if senha == secreta:
				enviar('\n[*] JOGO FINALIZADO [*]')
				enviar("\nVOCÊ GANHOU =)\n\n\n\n\n")
				break


			while True:
				enviar("Digite uma letra: ")

				tentativa = receber().lower().strip()

				if len(tentativa) == 1:
					if tentativa in string.letters:
						break
					enviar('\n[!] APENAS LETRAS SÃO PERMITIDAS [!]\n\n')
				else:
					enviar('\n[!] APENAS UM CARACTERE É PERMITIDO [!]\n\n')


			if tentativa in digitadas:
				espaco()
				enviar(forca(erros))
				enviar("[!] VOCÊ JÁ TENTOU ESSA LETRA [!]\n")
				continue
			else:
				digitadas += tentativa
				if tentativa in secreta:
					espaco()
				  	enviar(forca(erros))
			  		enviar("[+] ACERTOU [+]\n")
			  		acertos += tentativa
				else:
			  		erros += 1
			  		espaco()
			  		enviar(forca(erros))
			  		enviar("[-] ERROU [-]\n")


			if erros == 6:
				enviar("\nPalavra secreta: "+secreta+"\n")
				enviar("Tentativas: "+str(digitadas)+"\n")
				enviar('\n[*] JOGO FINALIZADO [*]')
				enviar("\nVOCÊ PERDEU =(\n\n\n\n\n")
				break


	def menu():

		enviar('''
--MENU--
1 - [JOGAR]
2 - [SAIR, ou ctrl + c]

OPÇÃO: ''')

		opcao = receber().strip()
		if opcao == '1':
			game()
		elif opcao == '2':
			con.close()
		else:
			enviar("\n[!] OPÇÃO INVÁLIDA [!]\n")


	print 'Conectado por', cliente

	while True:
		try:
			enviar(pyfiglet.figlet_format("Jogo Da Forca", font = "big"))
			menu()

		except:
			print 'Finalizando conexao do cliente', cliente
			con.close()
			thread.exit()


th = threading.Thread(target=broadcast_udp)
th.daemon = True
th.start()

try:
	while True:
		con, cliente = s.accept()
		thread.start_new_thread(conectado, tuple([con, cliente]))
except:
	s.close()