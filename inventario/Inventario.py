import csv
import os
import pyqrcode
from excepciones import CampoVacioError, CantidadInvalidaError


class Producto:
    def __init__(self, nombre, descripcion, categoria, cantidad, qr_path=""):
        self.nombre = nombre
        self.descripcion = descripcion
        self.categoria = categoria
        self.cantidad = cantidad
        self.qr_path = qr_path


class GeneradorQR:
    def __init__(self, qr_directory="qr_codes"):
        self.qr_directory = qr_directory

    def generar_qr(self, producto):
        url = f"https://miapp.com/productos/{producto.nombre.replace(' ', '_')}"
        contenido_qr = f"{url}\nDescripción: {producto.descripcion[:30]}"  # hasta 30 caracteres

        codigo_qr = pyqrcode.create(contenido_qr)

        if not os.path.exists(self.qr_directory):
            os.makedirs(self.qr_directory)

        filename = os.path.join(self.qr_directory, f"{producto.nombre.replace(' ', '_')}_qr.png")
        codigo_qr.png(filename, scale=5)
        return filename


class Inventario:
    def __init__(self):
        self.productos = []
        self.generador_qr = GeneradorQR()

    def agregar_producto(self, nombre, descripcion, categoria, cantidad):
        if not nombre or not descripcion or not categoria:
            raise CampoVacioError()
        if cantidad < 0:
            raise CantidadInvalidaError()

        producto = Producto(nombre, descripcion, categoria, cantidad)
        producto.qr_path = self.generador_qr.generar_qr(producto)
        self.productos.append(producto)

    def buscar_producto(self, nombre):
        for producto in self.productos:
            if producto.nombre == nombre:
                return producto
        return None

    def actualizar_cantidad(self, nombre, cantidad):
        producto = self.buscar_producto(nombre)
        if producto:
            if cantidad < 0:
                raise CantidadInvalidaError("La cantidad de actualización no puede ser negativa.")
            producto.cantidad += cantidad
        else:
            raise ValueError("Producto no encontrado.")

    def eliminar_producto(self, nombre):
        producto = self.buscar_producto(nombre)
        if producto:
            self.productos.remove(producto)
        else:
            raise ValueError("Producto no encontrado.")


    def exportar_a_csv(self, filename="inventario.csv"):
        try:
            with open(filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Nombre", "Descripción", "Categoría", "Cantidad", "QR"])  # Encabezados
                for producto in self.productos:
                    writer.writerow([producto.nombre, producto.descripcion, producto.categoria, producto.cantidad,
                                     producto.qr_path])

            print(f"Inventario exportado exitosamente a {filename}")

        except Exception as e:
            print(f"Error al exportar el archivo CSV: {e}")
