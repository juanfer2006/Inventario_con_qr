import tkinter as tk
from tkinter import Toplevel
from inventario import Inventario
from excepciones import CampoVacioError, CantidadInvalidaError
from PIL import Image, ImageTk


class InterfazGrafica:
    def __init__(self, ventana_principal, inventario):
        self.ventana_principal = ventana_principal
        self.inventario = inventario
        self.campos_input = {}
        self.botones = {}

        self.ventana_principal.title("Sistema de Inventario")

        # Campos de entrada
        self.campos_input["nombre"] = tk.Entry(ventana_principal)
        self.campos_input["nombre"].grid(row=0, column=1)
        tk.Label(ventana_principal, text="Nombre").grid(row=0, column=0)

        self.campos_input["descripcion"] = tk.Entry(ventana_principal)
        self.campos_input["descripcion"].grid(row=1, column=1)
        tk.Label(ventana_principal, text="Descripción").grid(row=1, column=0)

        self.campos_input["categoria"] = tk.Entry(ventana_principal)
        self.campos_input["categoria"].grid(row=2, column=1)
        tk.Label(ventana_principal, text="Categoría").grid(row=2, column=0)

        self.campos_input["cantidad"] = tk.Entry(ventana_principal)
        self.campos_input["cantidad"].grid(row=3, column=1)
        tk.Label(ventana_principal, text="Cantidad").grid(row=3, column=0)

        # Botones de funciones
        self.botones["agregar"] = tk.Button(ventana_principal, text="Agregar Producto", command=self.agregar_producto_ui)
        self.botones["agregar"].grid(row=4, columnspan=2)

        self.botones["exportar"] = tk.Button(ventana_principal, text="Exportar a CSV", command=self.exportar_a_csv_ui)
        self.botones["exportar"].grid(row=5, columnspan=2)

        self.botones["eliminar"] = tk.Button(ventana_principal, text="Eliminar Producto", command=self.eliminar_producto_ui)
        self.botones["eliminar"].grid(row=7, columnspan=2)

        # Lista de productos
        self.lista_productos = tk.Listbox(ventana_principal, width=50)
        self.lista_productos.grid(row=6, columnspan=2)
        self.lista_productos.bind("<Double-1>", self.mostrar_informacion_producto)  # Doble clic para ver detalles del producto

    def agregar_producto_ui(self):
        nombre = self.campos_input["nombre"].get()
        descripcion = self.campos_input["descripcion"].get()
        categoria = self.campos_input["categoria"].get()
        try:
            cantidad = int(self.campos_input["cantidad"].get())
            self.inventario.agregar_producto(nombre, descripcion, categoria, cantidad)
            self.lista_productos.insert(tk.END, nombre)
            for campo in self.campos_input.values():
                campo.delete(0, tk.END)
        except CampoVacioError as e:
            print("Error:", str(e))
        except CantidadInvalidaError as e:
            print("Error:", str(e))
        except ValueError:
            print("Error: La cantidad debe ser un número entero.")

    def mostrar_informacion_producto(self, event):
        seleccionado = self.lista_productos.get(self.lista_productos.curselection())
        producto = self.inventario.buscar_producto(seleccionado)
        if producto:
            ventana_detalle = Toplevel(self.ventana_principal)
            ventana_detalle.title(f"Detalles de {producto.nombre}")

            # Mostrar información del producto
            info_text = (
                f"Nombre: {producto.nombre}\n"
                f"Descripción: {producto.descripcion}\n"
                f"Categoría: {producto.categoria}\n"
                f"Cantidad: {producto.cantidad}\n"
            )
            tk.Label(ventana_detalle, text=info_text).pack()

            # Mostrar QR
            qr_img = Image.open(producto.qr_path)
            qr_img = qr_img.resize((150, 150), Image.LANCZOS)
            qr_img_tk = ImageTk.PhotoImage(qr_img)
            label_qr = tk.Label(ventana_detalle, image=qr_img_tk)
            label_qr.image = qr_img_tk
            label_qr.pack()

    def eliminar_producto_ui(self):
        try:
            seleccionado = self.lista_productos.get(self.lista_productos.curselection())
            self.inventario.eliminar_producto(seleccionado)
            self.lista_productos.delete(self.lista_productos.curselection())
        except Exception as e:
            print("Error al eliminar el producto:", str(e))

    def exportar_a_csv_ui(self):
        self.inventario.exportar_a_csv()


class ControladorApp:
    def __init__(self):
        self.inventario = Inventario()
        self.ventana_principal = tk.Tk()
        self.interfaz = InterfazGrafica(self.ventana_principal, self.inventario)

    def iniciar_aplicacion(self):
        self.ventana_principal.mainloop()


if __name__ == "__main__":
    app = ControladorApp()
    app.iniciar_aplicacion()
