#Matthew Vierling
#GUI for my PyCryprer module using tkinter and my PyCrypter module

from PyCrypter import *


class PyCrypterGUI:

	def __init__(self, master):
		self.master = master

		self.cryptor = PyCrypter(self.master)

		
		frame = Frame(master)
		frame.pack()
		

		self.encryptButton = Button(frame, text = "Encrypt File", command = self.encryptButtonPressed, bg = "green")
		self.encryptButton.pack(side = LEFT)

		self.decryptButton = Button(frame, text = "Decrypt File", command = self.decryptButtonPressed, bg = "blue")
		self.decryptButton.pack(side = LEFT)

		self.secureDelete = Button(frame, text = "Delete File", command = self.secureDeleteButtonPressed, bg = "red")
		self.secureDelete.pack(side = LEFT)

	def encryptButtonPressed(self):
		self.cryptor.encryptFile()

	def decryptButtonPressed(self):
		self.cryptor.decryptFile()

	def secureDeleteButtonPressed(self):
		file = askopenfile(parent = self.master, title = "select file to delete")

		#handles a cancel in askopenfile
		if file == None:
			return

		file.close()
		self.cryptor.deleteFile(file.name, 5)




