import tkinter as tk
from tkinter import messagebox

class ClienteInterfaz:
    def __init__(self, master):
        self.master = master
        master.title("Cliente Interfaz")

        self.label = tk.Label(master, text="IP del Servidor:")
        self.label.pack()

        self.ip_entry = tk.Entry(master)
        self.ip_entry.pack()

        self.conectar_button = tk.Button(master, text="Conectar", command=self.conectar)
        self.conectar_button.pack()

    def conectar(self):
        ip = self.ip_entry.get()
        if self.validar_ip(ip):
            messagebox.showinfo("Conexión", f"Intentando conectar a {ip}")
            # Aquí iría el código para conectar al servidor usando la IP
        else:
            messagebox.showerror("Error", "IP inválida")

    def validar_ip(self, ip):
        parts = ip.split(".")
        if len(parts) != 4:
            return False
        for part in parts:
            if not part.isdigit() or not 0 <= int(part) <= 255:
                return False
        return True

if __name__ == "__main__":
    root = tk.Tk()
    cliente_interfaz = ClienteInterfaz(root)
    root.mainloop()
