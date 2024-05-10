import sqlite3
import tkinter as tk
from tkinter import messagebox

class InventarioApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Gestión de Inventario")

        # Conexión a la base de datos SQLite
        self.conn = sqlite3.connect('inventario.db')
        self.c = self.conn.cursor()

        # Crear la tabla de productos si no existe
        self.c.execute('''CREATE TABLE IF NOT EXISTS productos (
                            codigo TEXT PRIMARY KEY,
                            nombre TEXT NOT NULL,
                            cantidad INTEGER,
                            precio REAL
                          )''')
        self.conn.commit()

        # Crear widgets para la interfaz
        self.label_codigo = tk.Label(master, text="Código:")
        self.label_nombre = tk.Label(master, text="Nombre:")
        self.label_cantidad = tk.Label(master, text="Cantidad:")
        self.label_precio = tk.Label(master, text="Precio:")

        self.entry_codigo = tk.Entry(master)
        self.entry_nombre = tk.Entry(master)
        self.entry_cantidad = tk.Entry(master)
        self.entry_precio = tk.Entry(master)

        self.button_agregar = tk.Button(master, text="Agregar Producto", command=self.agregar_producto)
        self.button_buscar = tk.Button(master, text="Buscar Producto", command=self.buscar_producto)
        self.button_listar = tk.Button(master, text="Listar Productos", command=self.listar_productos)
        self.button_eliminar = tk.Button(master, text="Eliminar Producto", command=self.eliminar_producto)

        # Posicionar widgets en la interfaz
        self.label_codigo.grid(row=0, column=0, padx=10, pady=5)
        self.label_nombre.grid(row=1, column=0, padx=10, pady=5)
        self.label_cantidad.grid(row=2, column=0, padx=10, pady=5)
        self.label_precio.grid(row=3, column=0, padx=10, pady=5)

        self.entry_codigo.grid(row=0, column=1, padx=10, pady=5)
        self.entry_nombre.grid(row=1, column=1, padx=10, pady=5)
        self.entry_cantidad.grid(row=2, column=1, padx=10, pady=5)
        self.entry_precio.grid(row=3, column=1, padx=10, pady=5)

        self.button_agregar.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky=tk.W+tk.E)
        self.button_buscar.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky=tk.W+tk.E)
        self.button_listar.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky=tk.W+tk.E)
        self.button_eliminar.grid(row=7, column=0, columnspan=2, padx=10, pady=10, sticky=tk.W+tk.E)

    def agregar_producto(self):
        codigo = self.entry_codigo.get()
        nombre = self.entry_nombre.get()
        cantidad = self.entry_cantidad.get()
        precio = self.entry_precio.get()

        try:
            cantidad = int(cantidad)
            precio = float(precio)
            self.c.execute('''INSERT INTO productos (codigo, nombre, cantidad, precio)
                               VALUES (?, ?, ?, ?)''', (codigo, nombre, cantidad, precio))
            self.conn.commit()
            messagebox.showinfo("Éxito", f"Producto '{nombre}' agregado al inventario.")
        except ValueError:
            messagebox.showerror("Error", "Cantidad y precio deben ser números.")

    def buscar_producto(self):
        codigo = self.entry_codigo.get()
        self.c.execute('''SELECT nombre, cantidad, precio FROM productos WHERE codigo = ?''', (codigo,))
        producto = self.c.fetchone()
        if producto:
            nombre, cantidad, precio = producto
            messagebox.showinfo("Información", f"Nombre: {nombre}\nCantidad: {cantidad}\nPrecio: ${precio:.2f}")
        else:
            messagebox.showerror("Error", f"No se encontró ningún producto con el código {codigo}.")

    def listar_productos(self):
        self.c.execute('''SELECT codigo, nombre, cantidad, precio FROM productos''')
        productos = self.c.fetchall()
        if productos:
            lista_productos = "Inventario:\n"
            for producto in productos:
                lista_productos += f"Código: {producto[0]}, Nombre: {producto[1]}, Cantidad: {producto[2]}, Precio: ${producto[3]:.2f}\n"
            messagebox.showinfo("Lista de Productos", lista_productos)
        else:
            messagebox.showinfo("Lista de Productos", "El inventario está vacío.")

    def eliminar_producto(self):
        codigo = self.entry_codigo.get()
        self.c.execute('''DELETE FROM productos WHERE codigo = ?''', (codigo,))
        if self.c.rowcount > 0:
            self.conn.commit()
            messagebox.showinfo("Éxito", f"Producto con código {codigo} eliminado del inventario.")
        else:
            messagebox.showerror("Error", f"No se encontró ningún producto con el código {codigo}.")

    def __del__(self):
        self.conn.close()

# Crear la ventana principal de la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = InventarioApp(root)
    root.mainloop()