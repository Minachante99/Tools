import os,glob,_thread as thread

class FilesParser:
	'''Una clase que sirve como base para pasarle funciones a un arhivo, aca su principal tarea e idea fundamental es como "convertidor", chequeando si la carpeta para enviar los resultados existe o crearla, y luego pasando una funcion (delegando a las subclases que creen el respectivo metodo "_conversor")a un archivo o varios archivos de una carpeta segun la direccion'''
	
	def __init__(self, path):
		self.results = []
		self.main_path = (os.path.split(path)[0]) + os.sep + 'Results'
		#levanta un thread de fondo:
		thread.start_new_thread(self.check_folder, ())
		
	#chequea si la carpeta existe o la crea:
	def check_folder(self):
		if not os.path.isdir(self.main_path):
			os.mkdir(self.main_path)
	
	#chequea si es un archivo o una carpeta, y mediante un loop le pasa el metodo _conversor(creado en subclases) a cada uno de los archivos, que mediante el patron de busqueda del glob se asegura de solo escoger los del tipo de archivos correctos	
	def main(self,files_path,type):
		if os.path.isfile(files_path):
			self.files_parser(files_path)
		else:
			try:
				os.chdir(files_path)
				for x in glob.glob('*.'+type):
					self.files_parser(files_path + os.sep + x)
			except FileNotFoundError:
				print('\nNo encuentro el archivo')
				exit()

#subclass
class Txt(FilesParser):
	'''Subclase que especializa un metodo conversor que acepta txts de la forma estandar en la que guardo notas, los parsea y crea un diccionario guardandolo en un json'''
	
	#delegando, pasandole el tipo al glob
	def main(self,files_path,type='txt'):
		FilesParser.main(self,files_path,type)
	
	#crea un archivo, separa las notas pescando las lineas en blanco como separador, guarda en un diccionario y dumpea a un json, y finalmente agregando cada resultado a la lista que puede, a gusto, ser printeada 
	def files_parser(self,files_path):
		import json
		dictio = {}
		with open(files_path) as new_files:
			new_files = new_files.read()
			lista = new_files.split('\n\n')
		for x in lista:
			marca = x.find('-')
			clave = x[:(marca - 1)]
			valor = x[marca + 2:]
			dictio[clave] = valor
		name = os.path.split(files_path)[1]
		name = name[:name.find('.')+1] + 'json'
		with open(self.main_path + os.sep + name,'w') as result:
			json.dump([dictio],result)
		self.results.append(name)
		
#subclass
class Json_Fixer(FilesParser):
		'''Subclase que especializa el _conversor para parsear los viejos jsones que contenian muchos dictionarios con una sola clave para unirlos todos en un solo dict y guardarlo en un json'''
		
		#pasa el type al main(glob)
		def main(self,files_path,type='json'):
			FilesParser.main(self,files_path,type)
		
		#carga el json, le pasa un loop a la lista guardando el contenido(dicts)dentro de un diccionario, guardandolo en un json y añadiendo los resultados a una lista	
		def files_parser(self,files_path):
			import json
			dictio = {}
			with open(files_path) as new_file:
				paciente = json.load(new_file)
			for dic in paciente:
				for clave in dic:
					dictio[clave] = dic[clave]
			name = os.path.split(files_path)[1]
			with open(self.main_path + os.sep + name, 'w') as result:
				json.dump([dictio], result)
			self.results.append(name)
		
				
		
		
		


	
	



