#Matthew Vierling
#GUI for my PyCryprer module using tkinter and my PyCrypter module

from PyCrypter import *


class PyCrypterGUI:

	def __init__(self, master):
		self.master = master

		self.cryptor = PyCrypter(self.master)

		
		frame = Frame(master)
		frame.pack()
		

		self.encrypt_button = Button(frame, text = "Encrypt File", command = self.encrypt_button_pressed, bg = "green")
		self.encrypt_button.pack(side = LEFT)

		self.decrypt_button = Button(frame, text = "Decrypt File", command = self.decrypt_button_pressed, bg = "blue")
		self.decrypt_button.pack(side = LEFT)

		self.secure_delete = Button(frame, text = "Delete File", command = self.secure_delete_button_pressed, bg = "red")
		self.secure_delete.pack(side = LEFT)

	def encrypt_button_pressed(self):
		self.cryptor.encryptFile()

	def decrypt_button_pressed(self):
		self.cryptor.decryptFile()

	def secure_delete_button_pressed(self):
		file = askopenfile(parent = self.master, title = "select file to delete")

		#handles a cancel in askopenfile
		if file == None:
			return

		file.close()
		self.cryptor.deleteFile(file.name, 5)




