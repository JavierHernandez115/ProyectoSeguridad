import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import chat_interface # Asumiendo que el otro archivo se llama second_interface.py

# Crear la ventana principal
root = tk.Tk()
root.title("Interfaz Translucida")

# Hacer la ventana translúcida
root.attributes('-alpha', 0.8)

# Definir el tamaño de la ventana
root.geometry("300x400")

# Crear un marco para centrar los widgets
frame = ttk.Frame(root, padding=20)
frame.pack(expand=True)

# Cargar y mostrar la imagen
image_path = "./Images/Pastor.jpg"
image = Image.open(image_path).resize((250, 150))
photo = ImageTk.PhotoImage(image)

image_label = ttk.Label(frame, image=photo)
image_label.image = photo  # Mantener una referencia a la imagen para que no sea recolectada por el garbage collector
image_label.pack(pady=10)

# Crear una etiqueta
ip_label = ttk.Label(frame, text="Ingrese la IP del otro usuario:")
ip_label.pack(pady=5)

# Crear un campo de texto
ip_entry = ttk.Entry(frame, width=30)
ip_entry.pack(pady=5)

# Función que se ejecuta al hacer clic en el botón
def on_accept():
    ip = ip_entry.get()
    chat_interface.load_interface(ip)

# Crear un botón
accept_button = ttk.Button(frame, text="Aceptar", command=on_accept)
accept_button.pack(pady=10)

# Ejecutar el bucle principal
root.mainloop()
