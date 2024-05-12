import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

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

        # Crear y posicionar widgets en la interfaz
        self.frame_agregar = ttk.LabelFrame(master, text="Agregar Producto")
        self.frame_agregar.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W+tk.E)

        self.label_codigo = ttk.Label(self.frame_agregar, text="Código:")
        self.label_nombre = ttk.Label(self.frame_agregar, text="Nombre:")
        self.label_cantidad = ttk.Label(self.frame_agregar, text="Cantidad:")
        self.label_precio = ttk.Label(self.frame_agregar, text="Precio:")

        self.label_codigo.grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)
        self.label_nombre.grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
        self.label_cantidad.grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)
        self.label_precio.grid(row=3, column=0, padx=10, pady=5, sticky=tk.E)

        self.entry_codigo = ttk.Entry(self.frame_agregar)
        self.entry_nombre = ttk.Entry(self.frame_agregar)
        self.entry_cantidad = ttk.Entry(self.frame_agregar)
        self.entry_precio = ttk.Entry(self.frame_agregar)

        self.entry_codigo.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)
        self.entry_nombre.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)
        self.entry_cantidad.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)
        self.entry_precio.grid(row=3, column=1, padx=10, pady=5, sticky=tk.W)

        self.button_agregar = ttk.Button(self.frame_agregar, text="Agregar", command=self.agregar_producto)
        self.button_agregar.grid(row=4, columnspan=2, padx=10, pady=10, sticky=tk.W+tk.E)

        self.frame_operaciones = ttk.LabelFrame(master, text="Operaciones")
        self.frame_operaciones.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W+tk.E)

        self.button_buscar = ttk.Button(self.frame_operaciones, text="Buscar", command=self.buscar_producto)
        self.button_buscar.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W+tk.E)

        self.button_listar = ttk.Button(self.frame_operaciones, text="Listar Todos", command=self.listar_productos)
        self.button_listar.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W+tk.E)

        self.button_eliminar = ttk.Button(self.frame_operaciones, text="Eliminar", command=self.eliminar_producto)
        self.button_eliminar.grid(row=0, column=2, padx=10, pady=5, sticky=tk.W+tk.E)

    def agregar_producto(self):
        codigo = self.entry_codigo.get().strip()
        nombre = self.entry_nombre.get().strip()
        cantidad = self.entry_cantidad.get().strip()
        precio = self.entry_precio.get().strip()

        if not codigo or not nombre or not cantidad or not precio:
            messagebox.showerror("Error", "Todos los campos son requeridos.")
            return

        try:
            cantidad = int(cantidad)
            precio = float(precio)
        except ValueError:
            messagebox.showerror("Error", "Cantidad y precio deben ser números enteros o decimales.")
            return

        try:
            self.c.execute('''INSERT INTO productos (codigo, nombre, cantidad, precio)
                               VALUES (?, ?, ?, ?)''', (codigo, nombre, cantidad, precio))
            self.conn.commit()
            messagebox.showinfo("Éxito", f"Producto '{nombre}' agregado al inventario.")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", f"El producto con código {codigo} ya existe en el inventario.")

    def buscar_producto(self):
        codigo = self.entry_codigo.get().strip()
        if not codigo:
            messagebox.showerror("Error", "Ingrese un código para buscar.")
            return

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
        codigo = self.entry_codigo.get().strip()
        if not codigo:
            messagebox.showerror("Error", "Ingrese un código para eliminar.")
            return

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
