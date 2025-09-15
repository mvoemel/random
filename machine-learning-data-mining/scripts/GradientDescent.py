import tkinter as tk
from tkinter import ttk
import numpy as np

class GradientDescentGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Gradient Descent Explorer")

        self.feature_count_var = tk.IntVar(value=1)
        self.examples = []  # list of (feature_vars, y_var)
        self.theta_vars = []

        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self.root, padding=10)
        frame.grid()

        # Feature count
        ttk.Label(frame, text="Anzahl Merkmale:").grid(row=0, column=0, sticky="e")
        self.feature_spin = ttk.Spinbox(frame, from_=1, to=10, textvariable=self.feature_count_var, width=5)
        self.feature_spin.grid(row=0, column=1, sticky="w")
        ttk.Button(frame, text="Merkmale setzen", command=self.set_features).grid(row=0, column=2, padx=5)

        # Examples table
        self.table_frame = ttk.LabelFrame(frame, text="Beispiele (x und y)", padding=5)
        self.table_frame.grid(row=1, column=0, columnspan=3, pady=10, sticky="ew")

        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=2, column=0, columnspan=3)
        ttk.Button(btn_frame, text="+ Beispiel hinzufügen", command=self.add_example).grid(row=0, column=0)
        ttk.Button(btn_frame, text="− Letztes Beispiel entfernen", command=self.remove_example).grid(row=0, column=1)

        # Theta frame
        self.theta_frame = ttk.LabelFrame(frame, text="Initiale Theta-Werte", padding=5)
        self.theta_frame.grid(row=3, column=0, columnspan=3, pady=10, sticky="ew")

        # Learning rate and steps
        lr_frame = ttk.Frame(frame)
        lr_frame.grid(row=4, column=0, columnspan=3, pady=5)
        ttk.Label(lr_frame, text="Lernrate (α):").grid(row=0, column=0, sticky="e")
        self.lr_var = tk.DoubleVar(value=0.01)
        ttk.Entry(lr_frame, textvariable=self.lr_var, width=7).grid(row=0, column=1, sticky="w", padx=(0,15))
        ttk.Label(lr_frame, text="Schritte:").grid(row=0, column=2, sticky="e")
        self.steps_var = tk.IntVar(value=10)
        ttk.Entry(lr_frame, textvariable=self.steps_var, width=7).grid(row=0, column=3, sticky="w")

        # Run button
        ttk.Button(frame, text="Gradient Descent starten", command=self.run_gradient_descent).grid(row=5, column=0, columnspan=3, pady=10)

        # Output
        out_frame = ttk.LabelFrame(frame, text="Ergebnisse", padding=5)
        out_frame.grid(row=6, column=0, columnspan=3, sticky="nsew")
        self.text = tk.Text(out_frame, height=15, width=60)
        self.text.grid(row=0, column=0)
        scrollbar = ttk.Scrollbar(out_frame, orient="vertical", command=self.text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.text.config(yscrollcommand=scrollbar.set)

        # Configure grid weight
        self.root.columnconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

    def set_features(self):
        # Clear existing examples and theta entries
        for widgets in self.table_frame.winfo_children():
            widgets.destroy()
        self.examples.clear()
        for widgets in self.theta_frame.winfo_children():
            widgets.destroy()
        self.theta_vars.clear()

        # Header
        cols = self.feature_count_var.get()
        for j in range(cols):
            ttk.Label(self.table_frame, text=f"x{j}").grid(row=0, column=j)
        ttk.Label(self.table_frame, text="y").grid(row=0, column=cols)

        # Add one initial example
        self.add_example()

        # Theta entries: bias + one per feature
        ttk.Label(self.theta_frame, text="θ₀ (Bias)").grid(row=0, column=0)
        bias_var = tk.DoubleVar(value=0.0)
        ttk.Entry(self.theta_frame, textvariable=bias_var, width=10).grid(row=1, column=0, padx=5)
        self.theta_vars.append(bias_var)
        for j in range(cols):
            ttk.Label(self.theta_frame, text=f"θ{j+1}").grid(row=0, column=j+1)
            var = tk.DoubleVar(value=0.0)
            ttk.Entry(self.theta_frame, textvariable=var, width=10).grid(row=1, column=j+1, padx=5)
            self.theta_vars.append(var)

    def add_example(self):
        cols = self.feature_count_var.get()
        row = len(self.examples) + 1
        feature_vars = []
        for j in range(cols):
            var = tk.DoubleVar(value=0.0)
            ttk.Entry(self.table_frame, textvariable=var, width=8).grid(row=row, column=j, padx=2, pady=2)
            feature_vars.append(var)
        y_var = tk.DoubleVar(value=0.0)
        ttk.Entry(self.table_frame, textvariable=y_var, width=8).grid(row=row, column=cols, padx=2, pady=2)
        self.examples.append((feature_vars, y_var))

    def remove_example(self):
        if not self.examples:
            return
        feature_vars, y_var = self.examples.pop()
        # destroy last row widgets
        row = len(self.examples) + 1
        for widget in self.table_frame.grid_slaves(row=row):
            widget.destroy()

    def run_gradient_descent(self):
        try:
            m = len(self.examples)
            if m == 0:
                return
            n = self.feature_count_var.get()
            X = np.ones((m, n+1))  # bias term
            y = np.zeros((m, 1))
            for i, (fvars, yvar) in enumerate(self.examples):
                for j, var in enumerate(fvars):
                    X[i, j+1] = var.get()
                y[i, 0] = yvar.get()

            theta = np.array([var.get() for var in self.theta_vars]).reshape((n+1, 1))
            alpha = self.lr_var.get()
            steps = self.steps_var.get()

            history = []
            for it in range(steps+1):
                # record
                history.append((it, theta.flatten().tolist()))
                # compute gradient
                preds = X.dot(theta)
                error = preds - y
                grad = (1/m) * X.T.dot(error)
                theta = theta - alpha * grad

            # display
            self.text.delete("1.0", tk.END)
            for it, thet in history:
                line = f"Schritt {it}: " + ", ".join(f"{t:.4f}" for t in thet) + "\n"
                self.text.insert(tk.END, line)
        except Exception as e:
            self.text.delete("1.0", tk.END)
            self.text.insert(tk.END, f"Fehler: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GradientDescentGUI(root)
    root.mainloop()
