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
        # Estilo para etiquetas y botones
        style = ttk.Style()
        style.configure('TLabel', font=('Century Gothic', 12, 'bold'), foreground='white', background='#00482b')
        style.configure('TButton', font=('Century Gothic', 12, 'bold'), foreground='#00482b', background='white')
        style.configure('TLabelframe', foreground='white', background='#00482b')
        style.configure('TLabelframe.Label', font=('Century Gothic', 12, 'bold'), foreground='white', background='#00482b')
        

        # Frame para agregar producto
        self.frame_agregar = ttk.LabelFrame(self.root, text="Agregar Producto")
        self.frame_agregar.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Definir campos y etiquetas
        campos = [
            ("Código", "entry_codigo"),
            ("Nombre", "entry_nombre"),
            ("Cantidad", "entry_cantidad"),
            ("PrecioUni", "entry_PrecioUni")
        ]

        # Crear etiquetas y entradas dentro del Frame
        for i, (label_text, entry_name) in enumerate(campos):
            label = ttk.Label(self.frame_agregar, text=label_text + ":")
            label.grid(row=i, column=0, padx=10, pady=5, sticky=tk.E)

            entry_var = tk.StringVar()
            entry = ttk.Entry(self.frame_agregar, textvariable=entry_var, width=30)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky=tk.W)

            # Asignar la entrada a un atributo de la instancia dinámicamente
            setattr(self, entry_name, entry)

        # Botón para agregar producto
        self.button_agregar = ttk.Button(self.frame_agregar, text="Agregar Producto", command=self.agregar_producto)
        self.button_agregar.grid(row=len(campos), columnspan=2, padx=150, pady=10, sticky=tk.W+tk.E)

        # Frame para operaciones
        self.frame_operaciones = ttk.LabelFrame(self.root, text="Operaciones")
        self.frame_operaciones.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Botones de operaciones
        self.button_buscar = ttk.Button(self.frame_operaciones, text="Buscar Producto", command=self.buscar_producto)
        self.button_buscar.pack(side=tk.LEFT, padx=10, pady=5)

        self.button_listar = ttk.Button(self.frame_operaciones, text="Listar Todos", command=self.listar_productos)
        self.button_listar.pack(side=tk.LEFT, padx=10, pady=5)

        self.button_eliminar = ttk.Button(self.frame_operaciones, text="Eliminar Producto", command=self.eliminar_producto)
        self.button_eliminar.pack(side=tk.LEFT, padx=10, pady=5)

    def agregar_producto(self):
        # Obtener valores de las entradas
        codigo = self.entry_codigo.get().strip()
        nombre = self.entry_nombre.get().strip()
        cantidad = self.entry_cantidad.get().strip()
        PrecioUni = self.entry_PrecioUni.get().strip()

        # Validar campos requeridos
        if not codigo or not nombre or not cantidad or not PrecioUni:
            messagebox.showerror("Error", "Todos los campos son requeridos.")
            return

        # Validar formato de cantidad y PrecioUni
        try:
            cantidad = int(cantidad)
            PrecioUni = float(PrecioUni)
        except ValueError:
            messagebox.showerror("Error", "Cantidad y PrecioUni deben ser números enteros o decimales válidos.")
            return

        # Agregar producto usando el controlador
        if self.controller.agregar_producto(codigo, nombre, cantidad, PrecioUni):
            messagebox.showinfo("Éxito", f"Producto '{nombre}' agregado al inventario.")
            self.clear_entries()
        else:
            messagebox.showerror("Error", f"El producto con código {codigo} ya existe en el inventario.")

    def buscar_producto(self):
        # Obtener código del producto a buscar
        codigo = self.entry_codigo.get().strip()
        if not codigo:
            messagebox.showerror("Error", "Ingrese un código para buscar.")
            return

        # Buscar producto usando el controlador
        producto = self.controller.buscar_producto(codigo)
        if producto:
            nombre, cantidad, PrecioUni = producto
            messagebox.showinfo("Información", f"Nombre: {nombre}\tCantidad: {cantidad}\tPrecioUni: ${PrecioUni:.2f}")
        else:
            messagebox.showerror("Error", f"No se encontró ningún producto con el código {codigo}.")

    def listar_productos(self):
        # Obtener lista de todos los productos
        productos = self.controller.listar_productos()
        if productos:
            # Crear una nueva ventana para mostrar la lista de productos como una tabla
            lista_window = tk.Toplevel(self.root)
            lista_window.title("Lista de Productos")

            ttk.Style().configure("Treeview", foreground='#00482b', background='white', font=('Century Gothic', 12))
            ttk.Style().configure("Treeview.Cell", anchor="center")

            table = ttk.Treeview(lista_window, columns=("Código", "Nombre", "Cantidad", "PrecioUni"), show="headings")
            table.heading("Código", text="Código")
            table.heading("Nombre", text="Nombre")
            table.heading("Cantidad", text="Cantidad")
            table.heading("PrecioUni", text="PrecioUni")
            

            for codigo, nombre, cantidad, PrecioUni in productos:
                table.insert("", "end", values=(codigo, nombre, cantidad, f"${PrecioUni:.2f}"))

            table.pack(fill="both", expand=True)
        else:
            messagebox.showinfo("Lista de Productos", "El inventario está vacío.")

    def eliminar_producto(self):
        # Obtener código del producto a eliminar
        codigo = self.entry_codigo.get().strip()
        if not codigo:
            messagebox.showerror("Error", "Ingrese un código para eliminar.")
            return

        # Eliminar producto usando el controlador
        if self.controller.eliminar_producto(codigo):
            messagebox.showinfo("Éxito", f"Producto con código {codigo} eliminado del inventario.")
            self.clear_entries()
        else:
            messagebox.showerror("Error", f"No se encontró ningún producto con el código {codigo}.")

    def clear_entries(self):
        # Limpiar los valores de las entradas después de completar una acción
        for entry_name in ["entry_codigo", "entry_nombre", "entry_cantidad", "entry_PrecioUni"]:
            getattr(self, entry_name).delete(0, tk.END)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    root.config(background='#00482b')
    root.resizable(False,False)
    app = InventarioView(root)
    app.run()
