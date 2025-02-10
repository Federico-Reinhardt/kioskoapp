import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

# Función para agregar una venta
def agregar_venta(event=None):  # Añadimos 'event=None' para manejar el evento de teclado
    producto = entrada_producto.get().strip()
    forma_pago = combo_forma_pago.get()  # Obtener la forma de pago seleccionada
    try:
        valor = float(entrada_valor.get())
        if producto and valor > 0 and forma_pago:
            # Agregar la venta al diccionario con la fecha de hoy
            fecha_hoy = datetime.now().strftime("%Y-%m-%d")
            if fecha_hoy not in ventas:
                ventas[fecha_hoy] = {}
            # Guardar el producto con su valor y forma de pago
            ventas[fecha_hoy][producto] = {"valor": valor, "forma_pago": forma_pago}
            actualizar_resumen()
            entrada_producto.delete(0, tk.END)
            entrada_valor.delete(0, tk.END)
            combo_forma_pago.set("")  # Limpiar el campo de forma de pago
        else:
            messagebox.showwarning("Entrada inválida", "Por favor, complete todos los campos.")
    except ValueError:
        messagebox.showerror("Error", "El valor debe ser un número.")

# Función para eliminar un artículo
def eliminar_articulo(fecha, producto):
    if fecha in ventas and producto in ventas[fecha]:
        del ventas[fecha][producto]
        # Si no quedan productos en esa fecha, eliminar la fecha del diccionario
        if not ventas[fecha]:
            del ventas[fecha]
        actualizar_resumen()

# Función para actualizar el resumen de ventas
def actualizar_resumen():
    # Limpiar el frame de resumen
    for widget in frame_resumen.winfo_children():
        widget.destroy()
    
    total_acumulado = 0  # Variable para calcular el total acumulado
    
    for fecha, productos in ventas.items():
        # Mostrar la fecha como encabezado
        tk.Label(frame_resumen, text=f"--- Fecha: {fecha} ---", font=("Arial", 10, "bold"), bg="#F5F5F5", fg="#333333").pack(anchor="w", pady=5)
        for producto, datos in productos.items():
            valor = datos["valor"]
            forma_pago = datos["forma_pago"]
            # Crear un frame para cada artículo
            frame_articulo = tk.Frame(frame_resumen, bg="#F5F5F5")
            frame_articulo.pack(fill="x", pady=2)
            
            # Mostrar el artículo, su valor y forma de pago
            tk.Label(frame_articulo, text=f"{producto}: ${valor:.2f} ({forma_pago})", font=("Arial", 10), bg="#F5F5F5", fg="#333333").pack(side="left", padx=5)
            
            # Botón de eliminación (cesto de basura)
            boton_eliminar = tk.Button(frame_articulo, text="🗑️", font=("Arial", 10), bg="#FF5722", fg="white", relief=tk.FLAT,
                                       command=lambda f=fecha, p=producto: eliminar_articulo(f, p))
            boton_eliminar.pack(side="right", padx=5)
            
            total_acumulado += valor  # Sumar al total acumulado
    
    # Actualizar el campo de total acumulado
    label_total_acumulado.config(text=f"Total Acumulado: ${total_acumulado:.2f}")

# Función para guardar los datos y salir
def guardar_y_salir():
    try:
        with open("ventas_diarias.txt", "w") as archivo:
            total_acumulado = 0  # Variable para calcular el total acumulado
            
            for fecha, productos in ventas.items():
                archivo.write(f"--- Fecha: {fecha} ---\n")
                for producto, datos in productos.items():
                    valor = datos["valor"]
                    forma_pago = datos["forma_pago"]
                    archivo.write(f"{producto}: ${valor:.2f} ({forma_pago})\n")
                    total_acumulado += valor  # Sumar al total acumulado
                archivo.write("\n")
            
            # Escribir el total acumulado al final del archivo
            archivo.write(f"Total Acumulado: ${total_acumulado:.2f}\n")
        
        messagebox.showinfo("Guardado", "Datos guardados correctamente.")
        ventana.destroy()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar el archivo: {e}")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Sistema de Ventas Diarias")
ventana.geometry("450x650")  # Tamaño de la ventana
ventana.resizable(False, False)  # No permitir cambiar el tamaño
ventana.configure(bg="#F5F5F5")  # Color de fondo

# Variables globales
ventas = {}

# Etiqueta con la fecha de hoy
fecha_hoy = datetime.now().strftime("%d/%m/%Y")
label_fecha = tk.Label(ventana, text=f"Fecha: {fecha_hoy}", font=("Arial", 12, "bold"), bg="#F5F5F5", fg="#333333")
label_fecha.pack(pady=10)

# Etiquetas y campos de entrada para agregar ventas
tk.Label(ventana, text="Producto:", font=("Arial", 10), bg="#F5F5F5", fg="#333333").pack(pady=5)
entrada_producto = tk.Entry(ventana, width=30, font=("Arial", 10))
entrada_producto.pack(pady=5)
entrada_producto.bind("<Return>", agregar_venta)  # Vincular "Enter" al campo de producto

tk.Label(ventana, text="Valor:", font=("Arial", 10), bg="#F5F5F5", fg="#333333").pack(pady=5)
entrada_valor = tk.Entry(ventana, width=30, font=("Arial", 10))
entrada_valor.pack(pady=5)
entrada_valor.bind("<Return>", agregar_venta)  # Vincular "Enter" al campo de valor

# Campo desplegable para forma de pago
tk.Label(ventana, text="Forma de Pago:", font=("Arial", 10), bg="#F5F5F5", fg="#333333").pack(pady=5)
opciones_pago = ["Mercado Pago", "Débito", "Crédito", "Efectivo", "Otros"]
combo_forma_pago = ttk.Combobox(ventana, values=opciones_pago, font=("Arial", 10), state="readonly")
combo_forma_pago.pack(pady=5)

# Botón para agregar venta
boton_agregar = tk.Button(ventana, text="Agregar Venta", command=agregar_venta, font=("Arial", 10), bg="#4CAF50", fg="white", relief=tk.FLAT)
boton_agregar.pack(pady=10)

# Frame para mostrar el resumen
frame_resumen = tk.Frame(ventana, bg="#F5F5F5")
frame_resumen.pack(fill="both", expand=True, pady=10)

# Campo para mostrar el total acumulado
label_total_acumulado = tk.Label(ventana, text="Total Acumulado: $0.00", font=("Arial", 12, "bold"), bg="#F5F5F5", fg="#FF5722")
label_total_acumulado.pack(pady=10)

# Botón para guardar y salir
boton_guardar = tk.Button(ventana, text="Guardar y Salir", command=guardar_y_salir, font=("Arial", 10), bg="#FF5722", fg="white", relief=tk.FLAT)
boton_guardar.pack(pady=10)

# Ejecutar la aplicación
try:
    ventana.mainloop()
except Exception as e:
    print(f"Error al ejecutar la aplicación: {e}")