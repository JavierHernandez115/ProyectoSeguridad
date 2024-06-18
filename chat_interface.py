import tkinter as tk
from tkinter import ttk
import threading

class ChatInterface:
    def __init__(self, master, send_callback):
        self.master = master
        self.send_callback = send_callback

        self.master.title("Chat")
        self.master.geometry("400x500")

        self.frame = ttk.Frame(self.master, padding=20)
        self.frame.pack(expand=True, fill=tk.BOTH)

        self.text_area = tk.Text(self.frame, state='disabled', wrap='word')
        self.text_area.pack(pady=10, padx=10, expand=True, fill=tk.BOTH)

        self.message_entry = ttk.Entry(self.frame, width=50)
        self.message_entry.pack(pady=5, padx=10, side=tk.LEFT, expand=True, fill=tk.X)
        self.message_entry.bind('<Return>', lambda event: self.send_message())

        self.send_button = ttk.Button(self.frame, text="Enviar", command=self.send_message)
        self.send_button.pack(pady=5, padx=10, side=tk.RIGHT)

    def send_message(self):
        message = self.message_entry.get()
        if message:
            self.send_callback(message)
            self.message_entry.delete(0, tk.END)

    def display_message(self, message):
        self.text_area.config(state='normal')
        self.text_area.insert(tk.END, f"{message}\n")
        self.text_area.config(state='disabled')
        self.text_area.yview(tk.END)
