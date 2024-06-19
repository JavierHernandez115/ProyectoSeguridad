import tkinter as tk
from tkinter import filedialog, scrolledtext

class ChatInterfaz:
    def __init__(self, master):
        self.master = master
        master.title("Chat Interfaz")

        # Crear un área de texto para mostrar mensajes
        self.chat_area = scrolledtext.ScrolledText(master, wrap=tk.WORD, state='disabled')
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Crear un campo de entrada para escribir mensajes
        self.message_entry = tk.Entry(master)
        self.message_entry.pack(padx=10, pady=5, fill=tk.X, expand=True)
        
        # Botón para enviar mensajes
        self.send_button = tk.Button(master, text="Enviar", command=self.enviar_mensaje)
        self.send_button.pack(padx=10, pady=5, side=tk.LEFT)
        
        # Botón para seleccionar archivo de texto
        self.file_button = tk.Button(master, text="Seleccionar Archivo", command=self.seleccionar_archivo)
        self.file_button.pack(padx=10, pady=5, side=tk.RIGHT)

    def enviar_mensaje(self):
        mensaje = self.message_entry.get()
        if mensaje:
            self.mostrar_mensaje("Yo", mensaje)
            self.message_entry.delete(0, tk.END)
            # Aquí se enviaría el mensaje al servidor
            # Simulamos una respuesta del servidor
            self.simular_respuesta_servidor(mensaje)

    def mostrar_mensaje(self, remitente, mensaje):
        self.chat_area.configure(state='normal')
        self.chat_area.insert(tk.END, f"{remitente}: {mensaje}\n")
        self.chat_area.configure(state='disabled')
        self.chat_area.yview(tk.END)

    def simular_respuesta_servidor(self, mensaje):
        # Simulación de una respuesta del servidor (puedes ajustar esto según tu implementación real)
        self.mostrar_mensaje("Servidor", f"Respuesta a: {mensaje}")

    def seleccionar_archivo(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                contenido = file.read()
                self.mostrar_mensaje("Archivo", contenido)

if __name__ == "__main__":
    root = tk.Tk()
    chat_interfaz = ChatInterfaz(root)
    root.mainloop()
