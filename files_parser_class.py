import os,glob,_thread as thread

class FilesParser:
	'''Una clase que sirve como base para pasarle funciones a un arhivo, chequea si la carpeta para enviar los resultados existe o crearla, y luego pasando una funcion a un archivo o varios de una carpeta segun la direccion'''
	
	def __init__(self, path):
		self.results = []
		self.main_path = (os.path.split(path)[0]) + os.sep + 'Results'
		#levanta un thread de fondo:
		thread.start_new_thread(self.check_folder, ())
		
	#chequea si la carpeta existe o la crea:
	def check_folder(self):
		if not os.path.isdir(self.main_path):
			os.mkdir(self.main_path)
	
	#chequea si es un archivo o una carpeta, y mediante un loop le pasa Una func a cada uno de los archivos, que mediante el patron de busqueda del glob se asegura de solo escoger los del tipo de archivos correctos.
	def main(self,func,files_path,type):
		if os.path.isfile(files_path):
			self.results.append(func(files_path,self.main_path))
		else:
			try:
				os.chdir(files_path)
				for x in glob.glob('*.'+type):
					self.results.append(func(files_path + os.sep + x,self.main_path))
			except FileNotFoundError:
				print('\nNo encuentro el archivo')
				exit()
	
	#Func para mostrar los resultados.
	def show_results(self):
		for result in self.results:
			print(result)


		
				
		
		
		


	
	



