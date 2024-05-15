from model import InventarioModel

class InventarioController:
    def __init__(self, model):
        self.model = model

    def agregar_producto(self, codigo, nombre, cantidad, precio):
        return self.model.agregar_producto(codigo, nombre, cantidad, precio)

    def buscar_producto(self, codigo):
        return self.model.buscar_producto(codigo)

    def listar_productos(self):
        return self.model.listar_productos()

    def eliminar_producto(self, codigo):
        return self.model.eliminar_producto(codigo)

    def cerrar_conexion(self):
        self.model.cerrar_conexion()
