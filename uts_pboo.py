import tkinter as tk
from tkinter import messagebox, scrolledtext
import pickle
import os
import math

# Coba import pygame untuk suara, fallback ke beep
try:
    import pygame
    pygame.mixer.init()
    SOUND_ENABLED = True
except ImportError:
    SOUND_ENABLED = False

class Calculator:
    def __init__(self):
        self.history = []  # Riwayat sebagai list string
    
    def add(self, a, b):
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result
    
    def subtract(self, a, b):
        result = a - b
        self.history.append(f"{a} - {b} = {result}")
        return result
    
    def multiply(self, a, b):
        result = a * b
        self.history.append(f"{a} * {b} = {result}")
        return result
    
    def divide(self, a, b):
        if b == 0:
            raise ValueError("Tidak bisa bagi nol")
        result = a / b
        self.history.append(f"{a} / {b} = {result}")
        return result
    
    # Fungsi ilmiah baru
    def sin(self, x):
        result = math.sin(math.radians(x))  # Asumsi input derajat
        self.history.append(f"sin({x}) = {result}")
        return result
    
    def cos(self, x):
        result = math.cos(math.radians(x))
        self.history.append(f"cos({x}) = {result}")
        return result
    
    def tan(self, x):
        result = math.tan(math.radians(x))
        self.history.append(f"tan({x}) = {result}")
        return result
    
    def log(self, x):
        if x <= 0:
            raise ValueError("Log hanya untuk x > 0")
        result = math.log10(x)
        self.history.append(f"log({x}) = {result}")
        return result
    
    def ln(self, x):
        if x <= 0:
            raise ValueError("Ln hanya untuk x > 0")
        result = math.log(x)
        self.history.append(f"ln({x}) = {result}")
        return result
    
    def sqrt(self, x):
        if x < 0:
            raise ValueError("Sqrt hanya untuk x >= 0")
        result = math.sqrt(x)
        self.history.append(f"sqrt({x}) = {result}")
        return result
    
    def power(self, a, b):
        result = math.pow(a, b)
        self.history.append(f"{a}^{b} = {result}")
        return result
    
    def get_pi(self):
        return math.pi
    
    def get_e(self):
        return math.e
    
    def get_history(self):
        return "\n".join(self.history)
    
    def save_history(self, filename="history.pkl"):
        with open(filename, "wb") as f:
            pickle.dump(self.history, f)
    
    def load_history(self, filename="history.pkl"):
        if os.path.exists(filename):
            with open(filename, "rb") as f:
                self.history = pickle.load(f)

class CalculatorUI:
    def __init__(self, root, calculator):
        self.root = root
        self.calculator = calculator
        self.scientific_mode = False  # Mode ilmiah off default
        self.root.title("Azico Kalkulator")
        self.root.geometry("650x850")  # Lebih lebar untuk tombol ilmiah
        self.root.configure(bg="#2e8b57")
        
        # Judul
        title_label = tk.Label(root, text="Azico Kalkulator", font=("Helvetica", 40, "bold"), bg="#2e8b57", fg="#ffff00")
        title_label.grid(row=0, column=0, columnspan=5, pady=10)
        
        # Layar
        self.display = tk.Entry(root, font=("Helvetica", 28), bg="#ffff99", fg="#2e8b57", justify="right", bd=10, relief="sunken")
        self.display.grid(row=1, column=0, columnspan=5, padx=15, pady=10, sticky="nsew")
        
        # Tombol mode
        mode_btn = tk.Button(root, text="Mode Ilmiah", font=("Arial Black", 14), bg="#666666", fg="#ffffff", activebackground="#000000", activeforeground="#ffffff", relief="raised", bd=5)
        mode_btn.grid(row=2, column=4, padx=5, pady=5, sticky="nsew")
        mode_btn.config(command=self.toggle_mode)
        
        # Tombol dasar
        basic_buttons = [
            ("7", 3, 0), ("8", 3, 1), ("9", 3, 2), ("/", 3, 3),
            ("4", 4, 0), ("5", 4, 1), ("6", 4, 2), ("*", 4, 3),
            ("1", 5, 0), ("2", 5, 1), ("3", 5, 2), ("-", 5, 3),
            ("0", 6, 0), (".", 6, 1), ("=", 6, 2), ("+", 6, 3),
            ("C", 7, 0), ("⌫", 7, 1), ("History", 7, 2), ("Save", 7, 3), ("Load", 7, 4)
        ]
        
        # Tombol ilmiah (hidden default)
        scientific_buttons = [
            ("sin", 3, 0), ("cos", 3, 1), ("tan", 3, 2), ("log", 3, 3), ("ln", 3, 4),
            ("sqrt", 4, 0), ("^", 4, 1), ("pi", 4, 2), ("e", 4, 3), ("(", 4, 4),
            (")", 5, 0)
        ]
        
        self.basic_buttons = []
        self.scientific_buttons = []
        
        for item in basic_buttons:
            text, row, col = item[0], item[1], item[2]
            btn = tk.Button(root, text=text, font=("Arial Black", 18), bg="#666666", fg="#ffffff", activebackground="#000000", activeforeground="#ffffff", relief="raised", bd=5)
            btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            btn.config(command=lambda t=text: self.on_button_click(t))
            self.basic_buttons.append(btn)
        
        for item in scientific_buttons:
            text, row, col = item[0], item[1], item[2]
            btn = tk.Button(root, text=text, font=("Arial Black", 14), bg="#666666", fg="#ffffff", activebackground="#000000", activeforeground="#ffffff", relief="raised", bd=5)
            btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            btn.config(command=lambda t=text: self.on_button_click(t))
            btn.grid_remove()  # Sembunyikan default
            self.scientific_buttons.append(btn)
        
        # Grid responsif
        for i in range(8):
            root.grid_rowconfigure(i, weight=1)
        for j in range(5):
            root.grid_columnconfigure(j, weight=1)
        
        # Keyboard
        self.root.bind("<Key>", self.on_key_press)
        
        self.current_input = ""
        self.operation = None
        self.first_number = None
    
    def toggle_mode(self):
        self.scientific_mode = not self.scientific_mode
        if self.scientific_mode:
            for btn in self.basic_buttons:
                btn.grid_remove()
            for btn in self.scientific_buttons:
                btn.grid()
            self.root.geometry("550x700")
        else:
            for btn in self.scientific_buttons:
                btn.grid_remove()
            for btn in self.basic_buttons:
                btn.grid()
            self.root.geometry("450x650")
    
    def on_button_click(self, text):
        self.play_sound()
        result = None  # Inisialisasi result
        
        if text.isdigit() or text == "." or text in ["(", ")"]:
            self.current_input += text
            self.update_display()
        elif text in ["+", "-", "*", "/"]:
            if self.current_input and not self.operation:
                self.first_number = float(self.current_input)
                self.operation = text
                self.current_input = ""
        elif text == "=":
            if self.first_number is not None and self.current_input:
                second_number = float(self.current_input)
                try:
                    if self.operation == "+":
                        result = self.calculator.add(self.first_number, second_number)
                    elif self.operation == "-":
                        result = self.calculator.subtract(self.first_number, second_number)
                    elif self.operation == "*":
                        result = self.calculator.multiply(self.first_number, second_number)
                    elif self.operation == "/":
                        result = self.calculator.divide(self.first_number, second_number)
                    elif self.operation == "^":
                        result = self.calculator.power(self.first_number, second_number)
                    if result is not None:
                        self.display.delete(0, tk.END)
                        self.display.insert(0, str(result))
                        self.current_input = str(result)
                        self.first_number = None
                        self.operation = None
                except ValueError as e:
                    messagebox.showerror("Error", str(e))
        elif text == "sin":
            if self.current_input:
                try:
                    result = self.calculator.sin(float(self.current_input))
                except ValueError as e:
                    messagebox.showerror("Error", str(e))
        elif text == "cos":
            if self.current_input:
                try:
                    result = self.calculator.cos(float(self.current_input))
                except ValueError as e:
                    messagebox.showerror("Error", str(e))
        elif text == "tan":
            if self.current_input:
                try:
                    result = self.calculator.tan(float(self.current_input))
                except ValueError as e:
                    messagebox.showerror("Error", str(e))
        elif text == "log":
            if self.current_input:
                try:
                    result = self.calculator.log(float(self.current_input))
                except ValueError as e:
                    messagebox.showerror("Error", str(e))
        elif text == "ln":
            if self.current_input:
                try:
                    result = self.calculator.ln(float(self.current_input))
                except ValueError as e:
                    messagebox.showerror("Error", str(e))
        elif text == "sqrt":
            if self.current_input:
                try:
                    result = self.calculator.sqrt(float(self.current_input))
                except ValueError as e:
                    messagebox.showerror("Error", str(e))
        elif text == "^":
            if self.current_input and not self.operation:
                self.first_number = float(self.current_input)
                self.operation = "^"
                self.current_input = ""
        elif text == "pi":
            self.current_input += str(self.calculator.get_pi())
            self.update_display()
        elif text == "e":
            self.current_input += str(self.calculator.get_e())
            self.update_display()
        elif text == "C":
            self.clear_all()
        elif text == "⌫":
            self.current_input = self.current_input[:-1]
            self.update_display()
        elif text == "History":
            history = self.calculator.get_history()
            if history:
                history_window = tk.Toplevel(self.root)
                history_window.title("Riwayat")
                history_window.geometry("400x300")
                history_window.configure(bg="#2e8b57")
                text_area = scrolledtext.ScrolledText(history_window, font=("Helvetica", 12), bg="#ffff99", fg="#2e8b57")
                text_area.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
                text_area.insert(tk.END, history)
                text_area.config(state=tk.DISABLED)
            else:
                messagebox.showinfo("Riwayat", "Kosong")
        elif text == "Save":
            self.calculator.save_history()
            messagebox.showinfo("Info", "Disimpan!")
        elif text == "Load":
            self.calculator.load_history()
            messagebox.showinfo("Info", "Dimuat!")
        
        # Update display jika result ada (untuk fungsi ilmiah)
        if result is not None:
            self.display.delete(0, tk.END)
            self.display.insert(0, str(result))
            self.current_input = str(result)
    
    def play_sound(self):
        if SOUND_ENABLED:
            try:
                pygame.mixer.Sound("click.wav").play()
            except:
                print("\a")
        else:
            print("\a")
    
    def on_key_press(self, event):
        key = event.char
        if key.isdigit() or key == ".":
            self.on_button_click(key)
        elif key in ["+", "-", "*", "/"]:
            self.on_button_click(key)
        elif key == "\r":
            self.on_button_click("=")
        elif key == "\x08":
            self.on_button_click("⌫")
    
    def update_display(self):
        self.display.delete(0, tk.END)
        self.display.insert(0, self.current_input)
    
    def clear_all(self):
        self.current_input = ""
        self.first_number = None
        self.operation = None
        self.display.delete(0, tk.END)

# Jalankan
if __name__ == "__main__":
    calc = Calculator()
    root = tk.Tk()
    ui = CalculatorUI(root, calc)
    root.mainloop()
