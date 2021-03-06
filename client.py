import socket
import sys
import os
import time
from time import sleep
from os import walk

s = socket.socket()

def send(mes=''):
	s.send(bytes(mes + ("\r\n"), "UTF-8"))
def recieve():
	rec = s.recv(1024)
	return (rec)
	    
def action(mes=''):
	send(mes)
	return recieve()
def local_dir(path=''):
	for (dirpath, dirnames, filenames) in walk(path):
		print ('"'+dirpath+'"')
		break
def browse_local(path=''):
	for (dirpath, dirnames, filenames) in walk(path):
		print (dirnames)
		print (filenames)
		print ('\n')
		break
def pasv():
	while True:
		mes = ('PASV')
		send(mes)
		mes = (s.recv(1024))
		mes = mes.decode()
		nmsg = mes.split('(')
		nmsg = nmsg[-1].split(')')
		p = nmsg[0].split(',')
		newip = '.'.join(p[:4])
		newport = int(p[4])*256 + int(p[5])
		return (newip,newport)
		break
		
def sendfile(file=''):
	newip, newport = pasv()
	p = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	p.connect((newip, newport))
	send('STOR '+file)
	f = open(file, 'rb')
	size = os.stat(file)[6]
	opened = True
	pos = 0
	buff = 1024
	packs = size/1024
	timeb = 100/packs
	i=0
	while opened:
		i=i+timeb
		if i>100:
			i=100
		time.sleep(.05)
		sys.stdout.write("\r%d%%" %i)
		sys.stdout.flush()
		f.seek(pos)
		pos += buff
		if pos >= size:
			piece = f.read(-1)
			opened = False
		else:
			piece = f.read(buff) 
		p.send(piece)
		
		f.seek(pos)
	f.close()
	p.close
	recieve()

def recievefile(file=''):
	newip, newport = pasv()
	p = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	p.connect((newip, newport))
	action('RETR '+file)
	newfile = open (file, 'w')
	aux=':)'
	while aux != "":
		time.sleep(.05)
		sys.stdout.write("\r" "wait")
		sys.stdout.flush()
		aux = p.recv(1024)
		aux=aux.decode(errors='ignore')
		newfile.write(aux)
	newfile.close()
	p.close


def listar():
	newip, newport = pasv()
	p = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	p.connect((newip, newport))
	mes = ('NLST')
	action (mes)
	rec = p.recv(1024)
	rec = rec.decode()
	rec.split('\r\n')
	print(rec)
	mes = ('ABOR')
	p.send(bytes(mes + ("\r\n"), "UTF-8"))
	p.close
	recieve()


s.connect((input("Enter FTP Address: "), 21))
s.recv(1024)		
		
usern = input("Enter user: ")
action('USER '+usern)


passw = input("Enter password: ")
action('PASS '+passw)

path = ('/')
buff=1024
while True:
	os.system('cls' if os.name == 'nt' else 'clear')
	print ('1 - Print Local and Remote Directory')
	print ('2 - Change Directory')
	print ('3 - Send Files')
	print ('4 - Recieve Files')
	print ('5 - change permission')
	print ('6 - exit')
	opc = input(' opcion: ')
	if opc == '1':
		while True:
			directory = ''
			os.system('cls' if os.name == 'nt' else 'clear')
			print('Remote Directory')
			mes = ('PWD')
			send(mes)
			directory = s.recv(1024)
			directory = directory.decode()
			vali = directory.split('i')
			vali = vali[0].split(' ')
			vali = vali[0]
			if vali == '257':
				directory = directory.split('"')
				directory = directory[1]
				print('"'+directory+'"')
			else:
				print('"'+directory+'"')
			listar()
			print('\nLocal Directory')
			local_dir(path)
			browse_local(path)
			print(input('Hit Return'))
			break
	if opc == '2':
		while True:
			os.system('cls' if os.name == 'nt' else 'clear')
			print ('1 - Change Local Directory')
			print ('2 - Change Remote Directory')
			print ('3 - Return')
			opc2 = input('opcion: ')
			if opc2 == '1':
				path2 = input('Change local directory (write home to return to home directory): ')
				if path2 == 'home':
					path = 'C:/Users/Lenovo/Desktop'
				else: 
					path = (path2)
				browse_local(path)
				print(input('Hit Return'))
			if opc2 == '2':
				print('Change remote directory (write up to go one directory up)')
				rd = input("Enter directory: ")
				if rd == 'up':
					action('CDUP')
				else:
					action('CWD '+rd)
				listar()
				print(input('\nHit Return'))
			if opc2 == '3':
				break
	if opc == '3':
		while True:
			os.system('cls' if os.name == 'nt' else 'clear')
			print ('File type')
			print ('1 - ASCII')
			print ('2 - Image')
			print ('3 - Return')
			opc2 = input(' opcion: ')
			if opc2 == '1':
				os.path = path
				file = input('File Name: ')
				mes = ('TYPE A')
				send(mes)
				while True:
					vali = recieve()
					vali = vali.decode()
					vali = vali.split("'")
					vali = vali[0].split(' ')
					vali = vali[0]
					if vali == '226':
						mes = ('ABOR')
						action(mes)
						recieve()
						break
					else:
						break
				action(mes)
				sendfile(file)
				print(input('Hit Return'))
			if opc2 == '2':
				os.path = path
				file = input('File Name: ')
				mes = ('TYPE I')
				send(mes)
				
				while True:
					vali = recieve()
					vali = vali.decode()
					vali = vali.split("'")
					vali = vali[0].split(' ')
					vali = vali[0]
					if vali == '226':
						mes = ('ABOR')
						action(mes)
						recieve()
						break
					else:
						break
				sendfile(file)
				print(input('Hit Return'))
			if opc2 == '3':
				break
	if opc == '4':
		while True:
			os.system('cls' if os.name == 'nt' else 'clear')
			print ('File type')
			print ('1 - ASCII')
			print ('2 - Image')
			print ('3 - Return')
			opc2 = input(' opcion: ')
			if opc2 == '1':
				os.path = path
				file = input('File Name: ')
				mes = ('TYPE A')
				send(mes)
				while True:
					vali = recieve()
					vali = vali.decode()
					vali = vali.split("'")
					vali = vali[0].split(' ')
					vali = vali[0]
					if vali == '226':
						mes = ('ABOR')
						action(mes)
						recieve()
						break
					else:
						break
				recievefile(file)
				print(input('Hit Return'))
				
			if opc2 == '2':
				os.path = path
				file = input('File Name: ')
				mes = ('TYPE I')
				send(mes)
				while True:
					vali = recieve()
					vali = vali.decode()
					vali = vali.split("'")
					vali = vali[0].split(' ')
					vali = vali[0]
					if vali == '226':
						mes = ('ABOR')
						action(mes)
						recieve()
						break
					else:
						break
				recievefile(file)
				print(input('Hit Return'))
				
			if opc2 == '3':
				break
				
	if opc == '5':
		os.system('cls' if os.name == 'nt' else 'clear')
		file=input('File name: ')
		perm=input('Write permissions, Example (742) :')
		action('SITE CHMOD '+perm + ' ' + file)
		print('the permissions of '+file+' has been updated to '+perm)
		print(input('\nHit Return'))
	if opc == '6':
		os.system('cls' if os.name == 'nt' else 'clear')
		print('FTP client by eddie.')
		print(input('\nHit return to exit'))
		break

s.close                  
