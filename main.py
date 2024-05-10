import sqlite3

class Inventario:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS productos (
                            codigo TEXT PRIMARY KEY,
                            nombre TEXT NOT NULL,
                            cantidad INTEGER,
                            precio REAL
                          )''')
        self.conn.commit()

    def agregar_producto(self, codigo, nombre, cantidad, precio):
        try:
            self.c.execute('''INSERT INTO productos (codigo, nombre, cantidad, precio)
                               VALUES (?, ?, ?, ?)''', (codigo, nombre, cantidad, precio))
            self.conn.commit()
            print(f"Producto '{nombre}' agregado al inventario.")
        except sqlite3.IntegrityError:
            print(f"El producto con código {codigo} ya existe en el inventario.")

    def buscar_producto(self, codigo):
        self.c.execute('''SELECT nombre, cantidad, precio FROM productos WHERE codigo = ?''', (codigo,))
        producto = self.c.fetchone()
        if producto:
            print(f"Nombre: {producto[0]}")
            print(f"Cantidad: {producto[1]}")
            print(f"Precio: ${producto[2]:.2f}")
        else:
            print(f"No se encontró ningún producto con el código {codigo}.")

    def eliminar_producto(self, codigo):
        self.c.execute('''DELETE FROM productos WHERE codigo = ?''', (codigo,))
        if self.c.rowcount > 0:
            self.conn.commit()
            print(f"Producto con código {codigo} eliminado del inventario.")
        else:
            print(f"No se encontró ningún producto con el código {codigo}.")

    def listar_productos(self):
        self.c.execute('''SELECT codigo, nombre, cantidad, precio FROM productos''')
        productos = self.c.fetchall()
        print("Inventario:")
        for producto in productos:
            print(f"Código: {producto[0]}")
            print(f"Nombre: {producto[1]}")
            print(f"Cantidad: {producto[2]}")
            print(f"Precio: ${producto[3]:.2f}")
            print("----------")

    def __del__(self):
        self.conn.close()

# Ejemplo de uso
if __name__ == "__main__":
    db_file = 'inventario.db'
    inventario = Inventario(db_file)

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
