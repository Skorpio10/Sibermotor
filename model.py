import sqlite3

class InventarioModel:
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
            return True
        except sqlite3.IntegrityError:
            return False

    def buscar_producto(self, codigo):
        self.c.execute('''SELECT nombre, cantidad, precio FROM productos WHERE codigo = ?''', (codigo,))
        return self.c.fetchone()

    def listar_productos(self):
        self.c.execute('''SELECT codigo, nombre, cantidad, precio FROM productos ORDER BY codigo''')
        return self.c.fetchall()

    def eliminar_producto(self, codigo):
        self.c.execute('''DELETE FROM productos WHERE codigo = ?''', (codigo,))
        if self.c.rowcount > 0:
            self.conn.commit()
            return True
        else:
            return False

    def cerrar_conexion(self):
        self.conn.close()
