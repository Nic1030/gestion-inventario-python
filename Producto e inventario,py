import json

class Producto:
    """
    Clase que representa un producto en el inventario.
    Contiene atributos para el ID, nombre, cantidad y precio del producto.
    """
    def __init__(self, producto_id, nombre, cantidad, precio):
        self._id = producto_id
        self._nombre = nombre
        self._cantidad = cantidad
        self._precio = precio

    # Propiedades (getters) para acceder a los atributos
    @property
    def id(self):
        return self._id

    @property
    def nombre(self):
        return self._nombre

    @property
    def cantidad(self):
        return self._cantidad

    @property
    def precio(self):
        return self._precio

    # Setters para modificar la cantidad y el precio
    @cantidad.setter
    def cantidad(self, nueva_cantidad):
        if nueva_cantidad >= 0:
            self._cantidad = nueva_cantidad
        else:
            print("La cantidad no puede ser negativa.")

    @precio.setter
    def precio(self, nuevo_precio):
        if nuevo_precio >= 0:
            self._precio = nuevo_precio
        else:
            print("El precio no puede ser negativo.")

    def __str__(self):
        """
        Método que devuelve una representación en cadena del objeto Producto.
        """
        return f"ID: {self._id} | Nombre: {self._nombre} | Cantidad: {self._cantidad} | Precio: ${self._precio:.2f}"

class Inventario:
    """
    Clase que gestiona la colección de productos en el inventario.
    Utiliza un diccionario para almacenar los productos.
    """
    def __init__(self, archivo="inventario.json"):
        self.archivo = archivo
        self.productos = self._cargar_inventario()

    def _cargar_inventario(self):
        """
        Carga los productos desde el archivo JSON al iniciar el programa.
        Maneja errores si el archivo no existe o está vacío.
        """
        try:
            with open(self.archivo, 'r') as f:
                data = json.load(f)
                inventario_cargado = {}
                for item_id, item_data in data.items():
                    inventario_cargado[item_id] = Producto(
                        item_id,
                        item_data['nombre'],
                        item_data['cantidad'],
                        item_data['precio']
                    )
                return inventario_cargado
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _guardar_inventario(self):
        """
        Guarda el inventario actual en el archivo JSON.
        Serializa los objetos Producto para que puedan ser almacenados.
        """
        try:
            data_to_save = {}
            for item_id, producto in self.productos.items():
                data_to_save[item_id] = {
                    'nombre': producto.nombre,
                    'cantidad': producto.cantidad,
                    'precio': producto.precio
                }
            with open(self.archivo, 'w') as f:
                json.dump(data_to_save, f, indent=4)
            print("Inventario guardado exitosamente.")
        except Exception as e:
            print(f"Error al guardar el inventario: {e}")

    def anadir_producto(self, producto_id, nombre, cantidad, precio):
        """
        Añade un nuevo producto al inventario.
        El ID es la clave del diccionario para una búsqueda eficiente.
        """
        if producto_id in self.productos:
            print("Error: Ya existe un producto con este ID.")
            return False
        
        nuevo_producto = Producto(producto_id, nombre, cantidad, precio)
        self.productos[producto_id] = nuevo_producto
        self._guardar_inventario()
        print("Producto añadido exitosamente.")
        return True

    def eliminar_producto(self, producto_id):
        """
        Elimina un producto del inventario por su ID.
        """
        if producto_id in self.productos:
            del self.productos[producto_id]
            self._guardar_inventario()
            print("Producto eliminado exitosamente.")
            return True
        else:
            print("Error: Producto no encontrado.")
            return False

    def actualizar_producto(self, producto_id, cantidad=None, precio=None):
        """
        Actualiza la cantidad o el precio de un producto existente.
        """
        if producto_id in self.productos:
            producto = self.productos[producto_id]
            if cantidad is not None:
                producto.cantidad = cantidad
            if precio is not None:
                producto.precio = precio
            self._guardar_inventario()
            print("Producto actualizado exitosamente.")
            return True
        else:
            print("Error: Producto no encontrado.")
            return False

    def buscar_producto(self, nombre):
        """
        Busca productos por nombre (búsqueda parcial, no sensible a mayúsculas).
        """
        resultados = [prod for prod in self.productos.values() if nombre.lower() in prod.nombre.lower()]
        if resultados:
            for prod in resultados:
                print(prod)
        else:
            print("No se encontraron productos con ese nombre.")

    def mostrar_inventario(self):
        """
        Muestra todos los productos en el inventario.
        """
        if not self.productos:
            print("El inventario está vacío.")
        else:
            print("\n--- Inventario Actual ---")
            for producto in self.productos.values():
                print(producto)
            print("-------------------------")

def limpiar_consola():
    """Función para limpiar la consola."""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    """
    Función principal que ejecuta la interfaz de usuario.
    """
    inventario = Inventario()
    
    while True:
        limpiar_consola()
        print("========================================")
        print("  Sistema Avanzado de Gestión de Inventario")
        print("========================================")
        print("1. Añadir nuevo producto")
        print("2. Eliminar producto")
        print("3. Actualizar cantidad/precio de producto")
        print("4. Buscar producto por nombre")
        print("5. Mostrar todo el inventario")
        print("6. Salir")
        print("========================================")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            limpiar_consola()
            print("--- Añadir Nuevo Producto ---")
            try:
                prod_id = input("Ingrese el ID único del producto: ")
                nombre = input("Ingrese el nombre del producto: ")
                cantidad = int(input("Ingrese la cantidad: "))
                precio = float(input("Ingrese el precio: "))
                inventario.anadir_producto(prod_id, nombre, cantidad, precio)
            except ValueError:
                print("Entrada inválida. Asegúrese de ingresar números válidos para cantidad y precio.")
            input("\nPresione Enter para continuar...")
        
        elif opcion == '2':
            limpiar_consola()
            print("--- Eliminar Producto ---")
            prod_id = input("Ingrese el ID del producto a eliminar: ")
            inventario.eliminar_producto(prod_id)
            input("\nPresione Enter para continuar...")
            
        elif opcion == '3':
            limpiar_consola()
            print("--- Actualizar Producto ---")
            prod_id = input("Ingrese el ID del producto a actualizar: ")
            opcion_actualizar = input("¿Qué desea actualizar? (C)antidad, (P)recio o (A)mbos: ").upper()
            try:
                if opcion_actualizar == 'C':
                    cantidad = int(input("Ingrese la nueva cantidad: "))
                    inventario.actualizar_producto(prod_id, cantidad=cantidad)
                elif opcion_actualizar == 'P':
                    precio = float(input("Ingrese el nuevo precio: "))
                    inventario.actualizar_producto(prod_id, precio=precio)
                elif opcion_actualizar == 'A':
                    cantidad = int(input("Ingrese la nueva cantidad: "))
                    precio = float(input("Ingrese el nuevo precio: "))
                    inventario.actualizar_producto(prod_id, cantidad=cantidad, precio=precio)
                else:
                    print("Opción no válida.")
            except ValueError:
                print("Entrada inválida. Ingrese un número válido.")
            input("\nPresione Enter para continuar...")
            
        elif opcion == '4':
            limpiar_consola()
            print("--- Buscar Producto ---")
            nombre = input("Ingrese el nombre del producto a buscar: ")
            inventario.buscar_producto(nombre)
            input("\nPresione Enter para continuar...")
            
        elif opcion == '5':
            limpiar_consola()
            inventario.mostrar_inventario()
            input("\nPresione Enter para continuar...")
            
        elif opcion == '6':
            print("Saliendo del programa...")
            break
            
        else:
            print("Opción inválida. Por favor, intente de nuevo.")
            input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    main()
