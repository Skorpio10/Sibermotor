import tkinter as tk
from tkinter import messagebox, ttk
from controller import InventarioController
from model import InventarioModel

class InventarioView:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Inventario")

        self.controller = InventarioController(model=InventarioModel(db_file='inventario.db'))

        self.create_widgets()

    def create_widgets(self):
        self.frame_agregar = ttk.LabelFrame(self.root, text="Agregar Producto")
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

        self.frame_operaciones = ttk.LabelFrame(root, text="Operaciones")
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

        if self.controller.agregar_producto(codigo, nombre, cantidad, precio):
            messagebox.showinfo("Éxito", f"Producto '{nombre}' agregado al inventario.")
        else:
            messagebox.showerror("Error", f"El producto con código {codigo} ya existe en el inventario.")
    
    def buscar_producto(self):
        codigo = self.entry_codigo.get().strip()
        if not codigo:
            messagebox.showerror("Error", "Ingrese un código para buscar.")
            return

        
        producto = self.controller.buscar_producto(codigo)
        if producto:
            nombre, cantidad, precio = producto
            messagebox.showinfo("Información", f"Nombre: {nombre}\nCantidad: {cantidad}\nPrecio: ${precio:.2f}")
        else:
            messagebox.showerror("Error", f"No se encontró ningún producto con el código {codigo}.")

    def listar_productos(self):

        productos = self.controller.listar_productos()
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

        if self.controller.eliminar_producto(codigo):
            messagebox.showinfo("Éxito", f"Producto con código {codigo} eliminado del inventario.")
        else:
            messagebox.showerror("Error", f"No se encontró ningún producto con el código {codigo}.")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = InventarioView(root)
    app.run()
