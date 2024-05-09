class Inventario:
    def __init__(self):
        self.productos = {}

    def agregar_producto(self, codigo, nombre, cantidad, precio):
        if codigo in self.productos:
            print(f"El producto con código {codigo} ya existe en el inventario.")
        else:
            self.productos[codigo] = {
                'nombre': nombre,
                'cantidad': cantidad,
                'precio': precio
            }
            print(f"Producto '{nombre}' agregado al inventario.")

    def buscar_producto(self, codigo):
        if codigo in self.productos:
            producto = self.productos[codigo]
            print(f"Nombre: {producto['nombre']}")
            print(f"Cantidad: {producto['cantidad']}")
            print(f"Precio: ${producto['precio']:.2f}")
        else:
            print(f"No se encontró ningún producto con el código {codigo}.")

    def eliminar_producto(self, codigo):
        if codigo in self.productos:
            del self.productos[codigo]
            print(f"Producto con código {codigo} eliminado del inventario.")
        else:
            print(f"No se encontró ningún producto con el código {codigo}.")

    def listar_productos(self):
        print("Inventario:")
        for codigo, producto in self.productos.items():
            print(f"Código: {codigo}")
            print(f"Nombre: {producto['nombre']}")
            print(f"Cantidad: {producto['cantidad']}")
            print(f"Precio: ${producto['precio']:.2f}")
            print("----------")

# Ejemplo de uso
if __name__ == "__main__":
    inventario = Inventario()

    # Agregar productos
    inventario.agregar_producto("123456", "Laptop Lenovo", 10, 899.99)
    inventario.agregar_producto("789012", "Monitor Samsung", 20, 249.99)

    # Buscar un producto por código
    inventario.buscar_producto("123456")

    # Listar todos los productos en el inventario
    inventario.listar_productos()

    # Eliminar un producto por código
    inventario.eliminar_producto("789012")

    # Listar nuevamente los productos después de eliminar
    inventario.listar_productos()
