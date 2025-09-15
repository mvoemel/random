import tkinter as tk
from tkinter import ttk
from math import exp

class LogisticRegressionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Allgemeine logistische Regression")

        self.param_entries = []
        self.precision_var = tk.IntVar(value=1)

        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.grid()

        # θ₀ (Bias)
        ttk.Label(main_frame, text="θ₀ (Bias):").grid(row=0, column=0, sticky="e")
        self.bias_entry = ttk.Entry(main_frame)
        self.bias_entry.grid(row=0, column=1)
        self.bias_entry.insert(0, "0")

        # Parameter-Label
        self.param_frame = ttk.LabelFrame(main_frame, text="Parameter (θᵢ · xᵢ)", padding=10)
        self.param_frame.grid(row=1, column=0, columnspan=2, pady=10)

        self.add_param_row()

        # Buttons zum Hinzufügen/Entfernen
        ttk.Button(main_frame, text="+ Parameter hinzufügen", command=self.add_param_row).grid(row=2, column=0, pady=5)
        ttk.Button(main_frame, text="− Letzten Parameter entfernen", command=self.remove_param_row).grid(row=2, column=1, pady=5)

        # Nachkommastellen
        ttk.Label(main_frame, text="Nachkommastellen:").grid(row=3, column=0, sticky="e", pady=(10, 0))
        self.precision_spinbox = ttk.Spinbox(main_frame, from_=0, to=10, textvariable=self.precision_var, width=5)
        self.precision_spinbox.grid(row=3, column=1, sticky="w", pady=(10, 0))

        # Berechnen
        ttk.Button(main_frame, text="Wahrscheinlichkeit berechnen", command=self.calculate_probability).grid(row=4, column=0, columnspan=2, pady=15)

        # Ergebnis
        self.result_label = ttk.Label(main_frame, text="Wahrscheinlichkeit: --")
        self.result_label.grid(row=5, column=0, columnspan=2)

    def add_param_row(self):
        row = len(self.param_entries)
        weight_var = tk.StringVar(value="0")
        input_var = tk.StringVar(value="0")

        weight_entry = ttk.Entry(self.param_frame, width=10, textvariable=weight_var)
        input_entry = ttk.Entry(self.param_frame, width=10, textvariable=input_var)

        weight_entry.grid(row=row, column=0, padx=5, pady=2)
        input_entry.grid(row=row, column=1, padx=5, pady=2)

        self.param_entries.append((weight_var, input_var))

    def remove_param_row(self):
        if self.param_entries:
            weight_var, input_var = self.param_entries.pop()
            weight_var.set("")
            input_var.set("")

            # Remove from UI
            widgets_to_destroy = self.param_frame.grid_slaves(row=len(self.param_entries))
            for widget in widgets_to_destroy:
                widget.destroy()

    def calculate_probability(self):
        try:
            z = float(self.bias_entry.get())
            for weight_var, input_var in self.param_entries:
                w = float(weight_var.get())
                x = float(input_var.get())
                z += w * x

            p = 1 / (1 + exp(-z))
            digits = self.precision_var.get()
            formatted = f"{p * 100:.{digits}f}%"
            self.result_label.config(text=f"Wahrscheinlichkeit: {formatted}")
        except Exception as e:
            self.result_label.config(text="Fehlerhafte Eingabe.")

# App starten
if __name__ == "__main__":
    root = tk.Tk()
    app = LogisticRegressionGUI(root)
    root.mainloop()
