#Matthew Vierling 
#python file encrypter using python's cryptography module and tkinter

#this will work for what seems like all files I throw at it except big files (a momory error is thrown)
#I was able to encrypt short videos (120Mbs) picures and text documents with ease
#update: I found that encrypting a 500MB file will use roughly 5GB of Memory. I will have to encrypt and write smaller pieces of data.

#****************************************TO DO***********************************************
#fix memory error
#********************************************************************************************

import base64
import os
from tempfile import *
from cryptography.fernet import Fernet 
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from tkinter import *
from tkinter.filedialog import *
from tkinter.simpledialog import *

class PyCrypter:

	def __init__(self, master = None):
		if master is None:
			self.master = Tk()
			label = Label(self.master, text = "AwesomePyCryptor")
			label.pack()
		else:
			self.master = master

	#generates a more secure password from a weak user password
	def gen_password(self, password, salt = None):
		kdf = PBKDF2HMAC(algorithm = hashes.SHA256(), length = 32, salt = salt, iterations = 100000, backend = default_backend())
		return base64.urlsafe_b64encode(kdf.derive(password.encode()))

	#overwrites the actual data with random data and then deletes the file path
	#this will not work on SSD drives only HDD and even then it's not that secure
	def delete_file(self, filename, passes = 2):
		with open(filename, 'rb+') as df:
			info = os.stat(filename)
			length = info.st_size

			for i in range(passes):
				df.seek(0)
				#writes a string of size random bytes
				df.write(os.urandom(length))

		os.remove(df.name)

	def encrypt_file(self):

		file = askopenfile(parent = self.master, title = "select file to encrypt.")

		#handles a cancel in askopenfile
		if file == None:
			return

		password = askstring(title = "Password", parent = self.master, prompt = "Enter Password")
		
		#handles a cancel in askstring
		if password == None:
			return

		salt = os.urandom(16)
		#removes any new line escape sequences 
		#this was causing errors when it goes to read the line with the salt on it--it was only getting part of it because of the escape sequence
		salt = salt.replace('\n'.encode(), ''.encode())

		#gets the byte data from the original file
		with open(file.name, 'rb') as of:
			of.seek(0)
			original_bytes = of.read()

		#gets the original name of the file and encodes it
		original_name = self.get_name_end(file.name)
		original_name = original_name.rstrip('\r\n') + '\n'
		original_name_bytes = original_name.encode()

		#opens a temp file to add the name to the top of the file, then reads that data to encrypt
		with TemporaryFile(mode = 'rb+') as tf:
			print("Flag: encrypt, inside tempfile") #flag not needed ******************************************************************************************************
			tf.seek(0)
			tf.write(original_name_bytes + original_bytes)
			tf.seek(0)
			new_byte_data = tf.read()

		print("Flag: encrypt, after tempfile") #flag not needed ******************************************************************************************************

		#encrypts the data
		f = Fernet(self.gen_password(password, salt))
		encrypted_data = f.encrypt(new_byte_data)

		print("Flag: encrypt, after encrypted_data") #flag not needed ******************************************************************************************************

		fname = asksaveasfilename(parent = self.master, title = "give name to encrypted file.", defaultextension = ".enc", filetypes = [("Encrypted File", ".enc")])

		#handles cancel if cancel is pressed in asksaveasfile
		if fname == '':
			return

		#writes the encrypted data to a .awesome file
		with open(fname, 'wb') as awf:
			awf.write(salt + '\n'.encode() + encrypted_data)

		return

	def decrypt_file(self):

		file = askopenfile(parent = self.master, title = "select file to decrypt", filetypes = [("Encrypted File", ".enc")])

		#handles a cancel in askopenfile
		if file == None:
			return

		password = askstring(title = "Password", parent = self.master, prompt = "Enter Password")

		#handles a cancel in askstring
		if password == None:
			return

		#opens and reads the encrypted byte data
		with open(file.name, 'rb') as inf:
			inf.seek(0)
			#reads the salt that was used in the original password
			salt = inf.readline()
			#removes the escape sequence '\n'
			salt = salt.rstrip('\r\n'.encode())
			#gets the rest of the data
			encrypted_data = inf.read()

		#decrypts the data
		f = Fernet(self.gen_password(password, salt))
		byte_data = f.decrypt(encrypted_data)

		#writes decrypted bytes to temp file then reads the original name at the top and the data to put in the new file
		with TemporaryFile(mode = 'rb+') as tf:
			tf.seek(0)
			#writes the byte data to temp file
			tf.write(byte_data)
			tf.seek(0)
			#reads top line to get the original name
			original_name_bytes = tf.readline()
			#removes escape sequence '\n' from the line and decodes it to a string
			original_name = original_name_bytes.rstrip('\r\n'.encode()).decode()
			#reads remaining data
			data = tf.read()
		
		#we have an error here for some reason we can't get the extension added on tho the end
		fname = asksaveasfilename(parent = self.master, title = "choose name to decrypted file", defaultextension = self.get_file_type(original_name), filetypes = [("Original File Type", self.get_file_type(original_name))],initialfile = self.get_file_name(original_name))

		#handles cancel if cancel is pressed in asksaveasfile
		if fname == '':
			return

		#opens temp to read the first line and get the original name
		with open(fname, 'wb') as f:
			f.seek(0)
			f.write(data)

		return

	#gets the original name of the file and the extension
	def get_name_end(self, filename):
		split_list = filename.rsplit("/")
		split_list.reverse()
		return split_list[0]

	#returns the files original extension
	def get_file_type(self, filename):
		split_list = filename.rsplit(".")
		split_list.reverse()
		return "." + split_list[0]

	#returns the original file name without the file extension
	def get_file_name(self, filename):
		split_list = filename.rsplit(".")
		return split_list[0]


	











	    