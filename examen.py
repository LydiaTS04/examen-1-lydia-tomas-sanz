# esto sirve para que cuando el usuario estcriba el nombre de la estanteria no importe si esta en mayusculas o minusculas 
import unicodedata

def normalizar_nombre(nombre):
    nombre = nombre.lower()  # Convertir a minúsculas
    nombre = unicodedata.normalize('NFD', nombre)  # Descomponer caracteres con tildes
    nombre = ''.join(char for char in nombre if unicodedata.category(char) != 'Mn')  # Eliminar tildes
    return nombre


# Creamos Clase Producto para definir el nombre, precio... de cada producto
class Producto:
    def __init__(self, nombre, cantidad, precio):
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    def __str__(self):
        return f"{self.nombre} - {self.cantidad} unidades a {self.precio}€ cada una"


# Clase Estantería representa las estanterias que hay y los productos que hay en cada estanteria con sus datos
class Estanteria:
    def __init__(self, nombre):
        self.nombre = nombre
        self.productos = [] #lista para guardar los productos
#agregar producto es una opcion que le damos al usuario para modificar la estanteria
    def agregar_producto(self, producto):
        # Busca si el producto ya existe en la estantería para actualizar su cantidad
        for p in self.productos:
            if p.nombre.lower() == producto.nombre.lower():
                p.cantidad += producto.cantidad
                print(f"Actualizado: {producto.cantidad} unidades de '{producto.nombre}' en {self.nombre}")
                return
        # Si el producto no existe, lo agrega
        self.productos.append(producto)
        print(f"Agregado: {producto} en {self.nombre}")
#retirar producto es una opcion que le damos al usuario para modificar la estanteria
    def retirar_producto(self, nombre, cantidad):
        for producto in self.productos:
            if producto.nombre.lower() == nombre.lower():
                if producto.cantidad >= cantidad:
                    producto.cantidad -= cantidad
                    print(f"Retirado: {cantidad} unidades de '{nombre}' en {self.nombre}")
                    # Elimina el producto si la cantidad llega a cero
                    if producto.cantidad == 0:
                        self.productos.remove(producto)
                        print(f"'{nombre}' eliminado de {self.nombre} por cantidad cero.")
                    return True
                else:
                    print(f"Error: Cantidad insuficiente de '{nombre}' en {self.nombre}")
                    return False
        print(f"Error: Producto '{nombre}' no encontrado en {self.nombre}")
        return False
#buscar producto es una opcion que le damos al usuario para buscar un producto
    def buscar_producto(self, nombre):
        for producto in self.productos:
            if producto.nombre.lower() == nombre.lower():
                return producto
        return None

    def total_valor(self):#para ver el valor del total
        return sum(p.cantidad * p.precio for p in self.productos)

    def __str__(self):
        return f"{self.nombre} - {len(self.productos)} productos"


# Clase Almacén gestiona todas las estanteras
class Almacen:
    def __init__(self):
        self.estanterias = {}

    def agregar_estanteria(self, nombre):
        nombre_normalizado = normalizar_nombre(nombre)
        if nombre_normalizado not in self.estanterias:
            self.estanterias[nombre_normalizado] = Estanteria(nombre)
            print(f"Estantería '{nombre}' creada.")
        else:
            print(f"La estantería '{nombre}' ya existe.")
#EJERCICIO EXTRA
    def optimizar_inventario(self):
        # Verificar si el almacén tiene estanterías
        if not self.estanterias:
            print("No hay estanterías en el almacén.")
            return
        
        # Variables para almacenar los resultados
        estanteria_mayor_valor = None
        mayor_valor = -1
        
        estanteria_menos_productos = None
        menor_cantidad_productos = float('inf')

        # Recorrer cada estantería para calcular los valores requeridos
        for estanteria in self.estanterias.values():
            total_valor = estanteria.total_valor()  # Calcular valor acumulado de la estantería
            cantidad_productos = len(estanteria.productos)  # Calcular cantidad de productos
            
            # Verificar si esta estantería tiene el mayor valor acumulado
            if total_valor > mayor_valor:
                mayor_valor = total_valor
                estanteria_mayor_valor = estanteria.nombre

            # Verificar si esta estantería tiene menos productos
            if cantidad_productos < menor_cantidad_productos:
                menor_cantidad_productos = cantidad_productos
                estanteria_menos_productos = estanteria.nombre

        # Mostrar resultados
        print("\n=== Optimización del Inventario ===")
        if estanteria_mayor_valor:
            print(f"Estantería con mayor valor acumulado: {estanteria_mayor_valor} (${mayor_valor})")
        if estanteria_menos_productos is not None:
            print(f"Estantería con menos productos: {estanteria_menos_productos} ({menor_cantidad_productos} productos)")


#le damos la opcion al usuario de agregar un producto a una estanteria
    def agregar_producto(self, estanteria, nombre, cantidad, precio):
        estanteria_normalizada = normalizar_nombre(estanteria)
        if estanteria_normalizada not in self.estanterias:
            self.agregar_estanteria(estanteria)
        producto = Producto(nombre, cantidad, precio)
        self.estanterias[estanteria_normalizada].agregar_producto(producto)
#le damos la opcion al usuario de retirar un producto a una estanteria
    def retirar_producto(self, nombre, cantidad):
        for estanteria in self.estanterias.values():
            producto = estanteria.buscar_producto(nombre)
            if producto:
                if estanteria.retirar_producto(nombre, cantidad):
                    return
        print(f"Error: Producto '{nombre}' no encontrado en el almacén.")
#el usuario puede ver la disponibilidad
    def verificar_disponibilidad(self, nombre):
        encontrado = False
        for estanteria in self.estanterias.values():
            producto = estanteria.buscar_producto(nombre)
            if producto:
                print(f"Producto '{nombre}' disponible en {estanteria.nombre} con {producto.cantidad} unidades.")
                encontrado = True
        if not encontrado:
            print(f"Producto '{nombre}' no encontrado en el almacén.")
#el usuario puede ver el estado del almacen con las modificacion que ha hecho 
    def estado_almacen(self):
        total_valor = 0
        print("\n=== Estado del Almacén ===")
        for estanteria in self.estanterias.values():
            print(f"\n{estanteria.nombre}:")
            if not estanteria.productos:
                print("  - Sin productos.")
                continue
            total_productos = 0
            for producto in estanteria.productos:
                total = producto.cantidad * producto.precio
                total_valor += total
                total_productos += producto.cantidad
                print(f"  - {producto.nombre}: {producto.cantidad} unidades, Precio unitario: {producto.precio}€, Total: {total}€")
            print(f"  Total productos en {estanteria.nombre}: {total_productos} unidades")
            print(f"  Valor total en {estanteria.nombre}: {estanteria.total_valor()}€")
        print(f"\nValor total del almacén: {total_valor}€\n")
#el usuario puede transferir producto de una estanteria a otra
    def transferir_producto(self, nombre, cantidad, estanteria_origen, estanteria_destino):
        origen_normalizado = normalizar_nombre(estanteria_origen)
        destino_normalizado = normalizar_nombre(estanteria_destino)

        origen = self.estanterias.get(origen_normalizado)
        destino = self.estanterias.get(destino_normalizado)

        if not origen:
            print(f"Error: Estantería de origen '{estanteria_origen}' no existe.")
            return
        if not destino:
            print(f"Error: Estantería de destino '{estanteria_destino}' no existe.")
            return

        producto = origen.buscar_producto(nombre)
        if producto and producto.cantidad >= cantidad:
            if origen.retirar_producto(nombre, cantidad):
                producto_transferido = Producto(nombre, cantidad, producto.precio)
                destino.agregar_producto(producto_transferido)
                print(f"Transferido: {cantidad} unidades de '{nombre}' de {estanteria_origen} a {estanteria_destino}")
        else:
            print(f"Error: No hay suficiente cantidad de '{nombre}' en '{estanteria_origen}' o el producto no existe.")

    def listar_estanterias(self):
        if not self.estanterias:
            print("No hay estanterías en el almacén.")
            return
        print("\nEstanterías disponibles:")
        for nombre in self.estanterias:
            print(f" - {nombre}")
        print()

    def listar_productos_estanteria(self, estanteria):
        estanteria_normalizada = normalizar_nombre(estanteria)
        est = self.estanterias.get(estanteria_normalizada)
        if not est:
            print(f"Error: La estantería '{estanteria}' no existe.")
            return
        if not est.productos:
            print(f"La estantería '{estanteria}' está vacía.")
            return
        print(f"\nProductos en '{estanteria}':")
        for producto in est.productos:
            print(f" - {producto}")
        print()


# Función para mostrar el menú
def mostrar_menu():
    print("\n=== Gestión de Almacén ===")
    print("1. Agregar Producto")
    print("2. Retirar Producto")
    print("3. Verificar Disponibilidad de Producto")
    print("4. Ver Estado del Almacén")
    print("5. Transferir Producto entre Estanterías")
    print("6. Listar Estanterías")
    print("7. Listar Productos en una Estantería")
    print("8. Optimización del Inventario")  # Nueva opción para optimizar inventario
    print("9. Salir")


# Función principal para manejar la interacción con el usuario
def main():
    almacen = Almacen()

    # Datos iniciales del almacén
    datos_iniciales = {
        "Estantería A": [
            {"nombre": "Chocolate Amargo", "cantidad": 20, "precio": 2.5},
            {"nombre": "Mermelada de Fresa", "cantidad": 15, "precio": 3.0}
        ],
        "Estantería B": [
            {"nombre": "Aceitunas Verdes", "cantidad": 50, "precio": 1.5},
            {"nombre": "Aceite de Oliva Extra", "cantidad": 10, "precio": 6.0}
        ],
        "Estantería C": [
            {"nombre": "Café Molido", "cantidad": 25, "precio": 5.0},
            {"nombre": "Té Verde", "cantidad": 40, "precio": 2.0}
        ],
        "Estantería D": [
            {"nombre": "Pasta Integral", "cantidad": 30, "precio": 1.8},
            {"nombre": "Arroz Basmati", "cantidad": 20, "precio": 1.7}
        ]
    }

    # Cargar datos iniciales
    for estanteria, productos in datos_iniciales.items():
        almacen.agregar_estanteria(estanteria)
        for prod in productos:
            almacen.agregar_producto(estanteria, prod["nombre"], prod["cantidad"], prod["precio"])

    while True:
        mostrar_menu()
        try:
            opcion = int(input("Seleccione una opción (1-8): "))
        except ValueError:
            print("Entrada inválida. Por favor, ingrese un número entre 1 y 8.")
            continue

        if opcion == 1:
            # Agregar Producto
            estanteria = input("Ingrese el nombre de la estantería: ").strip()
            nombre = input("Ingrese el nombre del producto: ").strip()
            try:
                cantidad = int(input("Ingrese la cantidad: "))
                precio = float(input("Ingrese el precio: "))
                if cantidad < 0 or precio < 0:
                    print("Cantidad y precio deben ser valores positivos.")
                    continue
            except ValueError:
                print("Cantidad debe ser un entero y precio un número.")
                continue
            almacen.agregar_producto(estanteria, nombre, cantidad, precio)

        elif opcion == 2:
            # Retirar Producto
            nombre = input("Ingrese el nombre del producto a retirar: ").strip()
            try:
                cantidad = int(input("Ingrese la cantidad a retirar: "))
                if cantidad <= 0:
                    print("La cantidad debe ser un número positivo.")
                    continue
            except ValueError:
                print("Cantidad debe ser un entero.")
                continue
            almacen.retirar_producto(nombre, cantidad)

        elif opcion == 3:
            # Verificar Disponibilidad de Producto
            nombre = input("Ingrese el nombre del producto a verificar: ").strip()
            almacen.verificar_disponibilidad(nombre)

        elif opcion == 4:
            # Ver Estado del Almacén
            almacen.estado_almacen()

        elif opcion == 5:
            # Transferir Producto entre Estanterías
            nombre = input("Ingrese el nombre del producto a transferir: ").strip()
            try:
                cantidad = int(input("Ingrese la cantidad a transferir: "))
                if cantidad <= 0:
                    print("La cantidad debe ser un número positivo.")
                    continue
            except ValueError:
                print("Cantidad debe ser un entero.")
                continue
            estanteria_origen = input("Ingrese la estantería de origen: ").strip()
            estanteria_destino = input("Ingrese la estantería de destino: ").strip()
            almacen.transferir_producto(nombre, cantidad, estanteria_origen, estanteria_destino)

        elif opcion == 6:
            # Listar Estanterías
            almacen.listar_estanterias()

        elif opcion == 7:
            # Listar Productos en una Estantería
            estanteria = input("Ingrese el nombre de la estantería: ").strip()
            almacen.listar_productos_estanteria(estanteria)

        elif opcion == 8:
         # Optimización del Inventario
            almacen.optimizar_inventario()
            
        elif opcion == 9:
            # Salir
            print("Saliendo del sistema de gestión del almacén. ¡Hasta luego!")
            break

        else:
            print("Opción no válida. Por favor, seleccione un número entre 1 y 8.")

if __name__ == "__main__":
    main()
