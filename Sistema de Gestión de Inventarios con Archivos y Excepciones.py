import os

class Producto:
    """Representa un producto individual con sus atributos."""
    def __init__(self, id_producto, nombre, cantidad, precio):
        self.id_producto = id_producto
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    def __str__(self):
        """Devuelve una representación en cadena del objeto Producto."""
        return f"ID: {self.id_producto}, Nombre: {self.nombre}, Cantidad: {self.cantidad}, Precio: ${self.precio:.2f}"

    def to_csv(self):
        """Convierte los datos del producto a una cadena CSV para guardar en archivo."""
        return f"{self.id_producto},{self.nombre},{self.cantidad},{self.precio}\n"

    @staticmethod
    def from_csv(linea):
        """Crea un objeto Producto a partir de una línea de texto CSV."""
        try:
            partes = linea.strip().split(',')
            if len(partes) == 4:
                return Producto(partes[0], partes[1], int(partes[2]), float(partes[3]))
        except (ValueError, IndexError) as e:
            # Manejo de líneas corruptas en el archivo
            print(f"❌ Error al procesar la línea del archivo: '{linea.strip()}'. Error: {e}")
            return None
        return None

class Inventario:
    """
    Gestiona la colección de productos, el almacenamiento en archivo
    y el manejo de excepciones.
    """
    def __init__(self, nombre_archivo='inventario.txt'):
        self.nombre_archivo = nombre_archivo
        self.productos = {}
        # Cargar el inventario automáticamente al iniciar
        self.cargar_inventario()

    def _guardar_inventario(self):
        """
        Método privado para guardar el inventario en el archivo.
        Implementa manejo de excepciones para escritura.
        """
        try:
            with open(self.nombre_archivo, 'w') as f:
                for producto in self.productos.values():
                    f.write(producto.to_csv())
            print(f"✔️ Inventario guardado exitosamente en '{self.nombre_archivo}'.")
        except PermissionError:
            print(f"❌ Error: Permiso denegado para escribir en el archivo '{self.nombre_archivo}'.")
        except Exception as e:
            print(f"❌ Ocurrió un error inesperado al guardar el inventario: {e}")

    def cargar_inventario(self):
        """
        Carga el inventario desde el archivo. Si el archivo no existe, lo crea.
        Implementa manejo de excepciones para lectura.
        """
        if not os.path.exists(self.nombre_archivo):
            print(f"⚠️ Archivo '{self.nombre_archivo}' no encontrado. Creando nuevo archivo.")
            self._guardar_inventario() # Esto crea un archivo vacío y con permisos
            return

        try:
            with open(self.nombre_archivo, 'r') as f:
                for linea in f:
                    producto = Producto.from_csv(linea)
                    if producto:
                        self.productos[producto.id_producto] = producto
            print(f"✔️ Inventario cargado exitosamente desde '{self.nombre_archivo}'.")
        except PermissionError:
            print(f"❌ Error: Permiso denegado para leer el archivo '{self.nombre_archivo}'.")
        except Exception as e:
            print(f"❌ Ocurrió un error inesperado al leer el inventario: {e}")

    def agregar_producto(self, producto):
        """Agrega un producto al inventario y guarda los cambios."""
        if producto.id_producto in self.productos:
            print(f"❌ Error: El producto con ID '{producto.id_producto}' ya existe.")
            return False
        self.productos[producto.id_producto] = producto
        self._guardar_inventario()
        return True

    def actualizar_producto(self, id_producto, nueva_cantidad=None, nuevo_precio=None):
        """Actualiza la cantidad y/o el precio de un producto existente."""
        if id_producto not in self.productos:
            print(f"❌ Error: No se encontró un producto con ID '{id_producto}'.")
            return False
        producto = self.productos[id_producto]
        if nueva_cantidad is not None:
            producto.cantidad = nueva_cantidad
        if nuevo_precio is not None:
            producto.precio = nuevo_precio
        self._guardar_inventario()
        print(f"✔️ Producto '{id_producto}' actualizado exitosamente.")
        return True

    def eliminar_producto(self, id_producto):
        """Elimina un producto del inventario y guarda los cambios."""
        if id_producto in self.productos:
            del self.productos[id_producto]
            self._guardar_inventario()
            print(f"✔️ Producto con ID '{id_producto}' eliminado exitosamente.")
            return True
        else:
            print(f"❌ Error: No se encontró un producto con ID '{id_producto}'.")
            return False

    def buscar_producto(self, id_producto):
        """Busca y devuelve un producto por su ID."""
        return self.productos.get(id_producto)

    def mostrar_inventario(self):
        """Muestra todos los productos en el inventario."""
        if not self.productos:
            print("El inventario está vacío.")
            return
        print("\n--- INVENTARIO ACTUAL ---")
        for producto in self.productos.values():
            print(producto)
        print("------------------------\n")

def menu_principal():
    """Función para mostrar el menú y manejar la interacción con el usuario."""
    inventario = Inventario()
    
    while True:
        print("\n--- SISTEMA DE GESTIÓN DE INVENTARIOS ---")
        print("1. Añadir nuevo producto")
        print("2. Actualizar producto")
        print("3. Eliminar producto")
        print("4. Buscar producto")
        print("5. Mostrar todo el inventario")
        print("6. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            id_producto = input("Ingrese el ID del producto: ")
            nombre = input("Ingrese el nombre del producto: ")
            try:
                cantidad = int(input("Ingrese la cantidad: "))
                precio = float(input("Ingrese el precio: "))
                if cantidad < 0 or precio < 0:
                    print("❌ Error: La cantidad y el precio no pueden ser negativos.")
                    continue
                nuevo_producto = Producto(id_producto, nombre, cantidad, precio)
                inventario.agregar_producto(nuevo_producto)
            except ValueError:
                print("❌ Entrada inválida. Asegúrese de ingresar un número para la cantidad y el precio.")
        
        elif opcion == '2':
            id_producto = input("Ingrese el ID del producto a actualizar: ")
            if inventario.buscar_producto(id_producto):
                try:
                    nueva_cantidad_str = input("Ingrese la nueva cantidad (deje en blanco para no cambiar): ")
                    nuevo_precio_str = input("Ingrese el nuevo precio (deje en blanco para no cambiar): ")
                    
                    nueva_cantidad = int(nueva_cantidad_str) if nueva_cantidad_str else None
                    nuevo_precio = float(nuevo_precio_str) if nuevo_precio_str else None
                    
                    if (nueva_cantidad is not None and nueva_cantidad < 0) or \
                       (nuevo_precio is not None and nuevo_precio < 0):
                        print("❌ Error: La cantidad y el precio no pueden ser negativos.")
                        continue
                    
                    inventario.actualizar_producto(id_producto, nueva_cantidad, nuevo_precio)
                except ValueError:
                    print("❌ Entrada inválida. Asegúrese de ingresar un número para la cantidad y el precio.")
            else:
                print(f"❌ Producto con ID '{id_producto}' no encontrado.")
        
        elif opcion == '3':
            id_producto = input("Ingrese el ID del producto a eliminar: ")
            inventario.eliminar_producto(id_producto)
            
        elif opcion == '4':
            id_producto = input("Ingrese el ID del producto a buscar: ")
            producto = inventario.buscar_producto(id_producto)
            if producto:
                print("\n--- PRODUCTO ENCONTRADO ---")
                print(producto)
                print("----------------------------")
            else:
                print(f"❌ No se encontró el producto con ID '{id_producto}'.")
                
        elif opcion == '5':
            inventario.mostrar_inventario()
            
        elif opcion == '6':
            print("Saliendo del sistema...")
            break
            
        else:
            print("❌ Opción no válida. Por favor, intente de nuevo.")

if __name__ == "__main__":
    menu_principal()
