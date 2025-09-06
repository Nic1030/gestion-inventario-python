# -*- coding: utf-8 -*-
#
# Este archivo contiene el código completo para un Sistema de Gestión de
# Biblioteca Digital, implementado en Python.
#
# El sistema consta de tres clases principales:
# 1. Libro: Representa un libro con sus atributos.
# 2. Usuario: Representa un usuario registrado en la biblioteca.
# 3. Biblioteca: Gestiona la lógica central, incluyendo el catálogo de
#    libros, los usuarios y los préstamos.
#
# Se utilizan diccionarios, conjuntos y tuplas para optimizar el
# almacenamiento y la búsqueda de datos.

class Libro:
    """
    Clase que representa un libro en la biblioteca.

    Atributos:
        titulo_autor (tupla): Una tupla inmutable que contiene el título y el autor del libro.
        categoria (str): La categoría a la que pertenece el libro (e.g., 'Fantasía', 'Novela').
        isbn (str): El ISBN (Número Estándar Internacional de Libros) del libro, que sirve como identificador único.
    """
    def __init__(self, titulo, autor, categoria, isbn):
        # Utiliza una tupla para titulo y autor, ya que son datos inmutables.
        self.titulo_autor = (titulo, autor)
        self.categoria = categoria
        self.isbn = isbn

    def __str__(self):
        """Devuelve una representación en cadena del objeto Libro para su fácil visualización."""
        titulo, autor = self.titulo_autor
        return f"Título: '{titulo}', Autor: {autor}, Categoría: {self.categoria}, ISBN: {self.isbn}"

class Usuario:
    """
    Clase que representa un usuario de la biblioteca.

    Atributos:
        nombre (str): El nombre del usuario.
        user_id (str): Un identificador único para el usuario.
        libros_prestados (list): Una lista de objetos Libro que el usuario ha prestado.
    """
    def __init__(self, nombre, user_id):
        self.nombre = nombre
        self.user_id = user_id
        # La lista almacena los objetos de los libros actualmente prestados por este usuario.
        self.libros_prestados = []

    def __str__(self):
        """Devuelve una representación en cadena del objeto Usuario."""
        return f"Usuario: {self.nombre} (ID: {self.user_id})"

class Biblioteca:
    """
    Clase principal que gestiona las colecciones de libros, usuarios y préstamos.

    Atributos:
        libros_disponibles (dict): Diccionario donde la clave es el ISBN y el valor es el objeto Libro.
                                   Permite una búsqueda de libros O(1) por ISBN.
        usuarios_registrados (set): Conjunto que almacena los IDs de usuario para asegurar su unicidad y
                                    permitir verificaciones rápidas de pertenencia.
        usuarios (dict): Diccionario donde la clave es el ID de usuario y el valor es el objeto Usuario.
    """
    def __init__(self):
        self.libros_disponibles = {}
        self.usuarios_registrados = set()
        self.usuarios = {}

    def anadir_libro(self, libro):
        """Añade un libro al catálogo de la biblioteca."""
        if libro.isbn in self.libros_disponibles:
            print(f"Error: El libro con ISBN {libro.isbn} ya existe.")
        else:
            self.libros_disponibles[libro.isbn] = libro
            print(f"Libro '{libro.titulo_autor[0]}' añadido exitosamente.")

    def quitar_libro(self, isbn):
        """Quita un libro del catálogo de la biblioteca por su ISBN."""
        if isbn in self.libros_disponibles:
            del self.libros_disponibles[isbn]
            print(f"Libro con ISBN {isbn} quitado exitosamente.")
        else:
            print(f"Error: No se encontró el libro con ISBN {isbn}.")

    def registrar_usuario(self, usuario):
        """Registra un nuevo usuario en el sistema."""
        if usuario.user_id in self.usuarios_registrados:
            print(f"Error: El ID de usuario '{usuario.user_id}' ya está registrado.")
        else:
            self.usuarios_registrados.add(usuario.user_id)
            self.usuarios[usuario.user_id] = usuario
            print(f"Usuario '{usuario.nombre}' registrado exitosamente.")

    def dar_de_baja_usuario(self, user_id):
        """Da de baja a un usuario del sistema por su ID."""
        if user_id in self.usuarios:
            # Eliminar el usuario del conjunto y del diccionario de usuarios
            self.usuarios_registrados.remove(user_id)
            del self.usuarios[user_id]
            print(f"Usuario con ID '{user_id}' dado de baja exitosamente.")
        else:
            print(f"Error: El usuario con ID '{user_id}' no está registrado.")

    def prestar_libro(self, user_id, isbn):
        """
        Presta un libro a un usuario.
        Mueve el libro del diccionario de libros disponibles a la lista de libros prestados del usuario.
        """
        if user_id not in self.usuarios:
            print("Error: El usuario no está registrado.")
            return

        if isbn not in self.libros_disponibles:
            print("Error: El libro no está disponible para préstamo.")
            return

        libro_a_prestar = self.libros_disponibles.pop(isbn)
        self.usuarios[user_id].libros_prestados.append(libro_a_prestar)
        print(f"Libro '{libro_a_prestar.titulo_autor[0]}' prestado a '{self.usuarios[user_id].nombre}'.")

    def devolver_libro(self, user_id, isbn):
        """
        Permite a un usuario devolver un libro.
        Mueve el libro de la lista de libros prestados del usuario al diccionario de libros disponibles.
        """
        if user_id not in self.usuarios:
            print("Error: El usuario no está registrado.")
            return

        usuario = self.usuarios[user_id]
        libro_encontrado = None
        for libro in usuario.libros_prestados:
            if libro.isbn == isbn:
                libro_encontrado = libro
                break

        if libro_encontrado:
            usuario.libros_prestados.remove(libro_encontrado)
            self.libros_disponibles[isbn] = libro_encontrado
            print(f"Libro '{libro_encontrado.titulo_autor[0]}' devuelto exitosamente por '{usuario.nombre}'.")
        else:
            print(f"Error: El usuario '{usuario.nombre}' no tiene prestado el libro con ISBN '{isbn}'.")

    def buscar_libro(self, criterio, valor):
        """
        Busca libros en el catálogo de la biblioteca por título, autor o categoría.
        La búsqueda no distingue entre mayúsculas y minúsculas.
        """
        resultados = []
        criterio = criterio.lower()
        valor = valor.lower()

        # Combina los libros disponibles y los prestados para una búsqueda exhaustiva.
        catalogo_completo = list(self.libros_disponibles.values())
        for usuario in self.usuarios.values():
            catalogo_completo.extend(usuario.libros_prestados)

        for libro in catalogo_completo:
            if criterio == 'titulo' and valor in libro.titulo_autor[0].lower():
                resultados.append(libro)
            elif criterio == 'autor' and valor in libro.titulo_autor[1].lower():
                resultados.append(libro)
            elif criterio == 'categoria' and valor in libro.categoria.lower():
                resultados.append(libro)
        
        return resultados

    def listar_libros_prestados(self, user_id):
        """Muestra una lista de los libros que un usuario tiene prestados."""
        if user_id not in self.usuarios:
            print("Error: El usuario no está registrado.")
            return []
        
        return self.usuarios[user_id].libros_prestados

# --- PRUEBA DEL SISTEMA ---
if __name__ == "__main__":
    print("--- Inicializando la Biblioteca Digital ---")
    biblioteca = Biblioteca()

    # 1. Crear y añadir libros
    libro1 = Libro("Cien años de soledad", "Gabriel García Márquez", "Novela", "978-0307474476")
    libro2 = Libro("El señor de los anillos", "J.R.R. Tolkien", "Fantasía", "978-0618640157")
    libro3 = Libro("1984", "George Orwell", "Ciencia Ficción", "978-0451524935")
    libro4 = Libro("El amor en los tiempos del cólera", "Gabriel García Márquez", "Novela", "978-0307474483")

    biblioteca.anadir_libro(libro1)
    biblioteca.anadir_libro(libro2)
    biblioteca.anadir_libro(libro3)
    biblioteca.anadir_libro(libro4)

    print("\n--- Catálogo de libros inicial ---")
    for libro in biblioteca.libros_disponibles.values():
        print(libro)

    # 2. Registrar usuarios
    print("\n--- Registrando usuarios ---")
    usuario1 = Usuario("Ana Pérez", "ana_perez_1")
    usuario2 = Usuario("Juan Gómez", "juan_gomez_2")
    biblioteca.registrar_usuario(usuario1)
    biblioteca.registrar_usuario(usuario2)
    print(f"IDs de usuarios registrados: {biblioteca.usuarios_registrados}")

    # Intentar registrar un usuario con un ID duplicado
    print("\n--- Intentando registrar usuario duplicado ---")
    biblioteca.registrar_usuario(Usuario("Ana Duplicada", "ana_perez_1"))

    # 3. Prestar y devolver libros
    print("\n--- Prestamos y devoluciones ---")
    biblioteca.prestar_libro("ana_perez_1", "978-0307474476")  # Prestar Cien años de soledad a Ana
    biblioteca.prestar_libro("juan_gomez_2", "978-0618640157")  # Prestar El señor de los anillos a Juan

    # Verificar los libros prestados a Ana
    print("\n--- Libros prestados a Ana ---")
    libros_de_ana = biblioteca.listar_libros_prestados("ana_perez_1")
    for libro in libros_de_ana:
        print(libro)
    print(f"Libros disponibles: {len(biblioteca.libros_disponibles)}")

    # Devolver un libro
    print("\n--- Devolviendo un libro ---")
    biblioteca.devolver_libro("ana_perez_1", "978-0307474476")
    print("\n--- Catálogo de libros después de la devolución ---")
    for libro in biblioteca.libros_disponibles.values():
        print(libro)
    print(f"\nLibros disponibles: {len(biblioteca.libros_disponibles)}")

    # 4. Buscar libros
    print("\n--- Buscando libros ---")
    print("Buscando por título '1984':")
    resultados_titulo = biblioteca.buscar_libro("titulo", "1984")
    for libro in resultados_titulo:
        print(libro)

    print("\nBuscando por autor 'García Márquez':")
    resultados_autor = biblioteca.buscar_libro("autor", "García Márquez")
    for libro in resultados_autor:
        print(libro)
    
    print("\nBuscando por categoría 'novela':")
    resultados_categoria = biblioteca.buscar_libro("categoria", "Novela")
    for libro in resultados_categoria:
        print(libro)

    # 5. Eliminar un libro
    print("\n--- Eliminando un libro ---")
    biblioteca.quitar_libro("978-0451524935")
    print(f"Libros disponibles después de la eliminación: {len(biblioteca.libros_disponibles)}")

    # 6. Dar de baja a un usuario
    print("\n--- Dando de baja a un usuario ---")
    biblioteca.dar_de_baja_usuario("juan_gomez_2")
    print(f"IDs de usuarios registrados: {biblioteca.usuarios_registrados}")
