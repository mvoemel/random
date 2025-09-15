import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

class ConfusionMatrixApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dynamic Confusion Matrix Calculator")

        self.class_names = ["Class 1", "Class 2", "Class 3"]
        self.matrix_entries = {}

        self.setup_ui()

    def setup_ui(self):
        control_frame = ttk.Frame(self.root)
        control_frame.pack(pady=5)

        self.new_class_entry = ttk.Entry(control_frame, width=15)
        self.new_class_entry.pack(side="left", padx=5)

        ttk.Button(control_frame, text="Add Class", command=self.add_class).pack(side="left", padx=5)
        ttk.Button(control_frame, text="Remove Last Class", command=self.remove_class).pack(side="left", padx=5)

        self.matrix_frame = ttk.Frame(self.root)
        self.matrix_frame.pack(padx=10, pady=10)

        self.result_frame = ttk.Frame(self.root)
        self.result_frame.pack(padx=10, pady=10)

        ttk.Button(self.root, text="Calculate", command=self.calculate).pack(pady=10)

        self.build_matrix()

    def add_class(self):
        new_class = self.new_class_entry.get().strip()
        if new_class and new_class not in self.class_names:
            self.class_names.append(new_class)
            self.build_matrix()
        self.new_class_entry.delete(0, tk.END)

    def remove_class(self):
        if len(self.class_names) > 0:
            self.class_names.pop()
            self.build_matrix()

    def build_matrix(self):
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()
        for widget in self.result_frame.winfo_children():
            widget.destroy()
        self.matrix_entries.clear()

        ttk.Label(self.matrix_frame, text="Predicted \\ Actual").grid(row=0, column=0)

        for i, label in enumerate(self.class_names):
            ttk.Label(self.matrix_frame, text=label).grid(row=0, column=i + 1)
            ttk.Label(self.matrix_frame, text=label).grid(row=i + 1, column=0)

        for i, pred in enumerate(self.class_names):
            for j, actual in enumerate(self.class_names):
                entry = ttk.Entry(self.matrix_frame, width=5, justify='center')
                entry.insert(0, "0")
                entry.grid(row=i + 1, column=j + 1)
                self.matrix_entries[(pred, actual)] = entry

    def calculate(self):
        try:
            matrix = pd.DataFrame(0, index=self.class_names, columns=self.class_names)

            for (pred, actual), entry in self.matrix_entries.items():
                val = int(entry.get())
                matrix.loc[pred, actual] = val

            for widget in self.result_frame.winfo_children():
                widget.destroy()

            ttk.Label(self.result_frame, text="Class").grid(row=0, column=0, padx=5)
            ttk.Label(self.result_frame, text="Precision").grid(row=0, column=1, padx=5)
            ttk.Label(self.result_frame, text="Recall").grid(row=0, column=2, padx=5)
            ttk.Label(self.result_frame, text="F1-Score").grid(row=0, column=3, padx=5)

            total_correct = 0
            total_samples = matrix.values.sum()

            precisions, recalls, f1s = [], [], []

            for i, cls in enumerate(self.class_names):
                tp = matrix.loc[cls, cls]
                fp = matrix.loc[cls].sum() - tp
                fn = matrix[cls].sum() - tp

                precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
                recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
                f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0

                total_correct += tp

                precisions.append(precision)
                recalls.append(recall)
                f1s.append(f1)

                ttk.Label(self.result_frame, text=cls).grid(row=i + 1, column=0)
                ttk.Label(self.result_frame, text=f"{precision:.5f}").grid(row=i + 1, column=1)
                ttk.Label(self.result_frame, text=f"{recall:.5f}").grid(row=i + 1, column=2)
                ttk.Label(self.result_frame, text=f"{f1:.5f}").grid(row=i + 1, column=3)

            accuracy = total_correct / total_samples if total_samples > 0 else 0.0
            macro_precision = sum(precisions) / len(precisions)
            macro_recall = sum(recalls) / len(recalls)
            macro_f1 = sum(f1s) / len(f1s)

            sep_row = len(self.class_names) + 2
            ttk.Label(self.result_frame, text="Overall Accuracy:").grid(row=sep_row, column=0, sticky="w")
            ttk.Label(self.result_frame, text=f"{accuracy:.2%}").grid(row=sep_row, column=1, sticky="w")

            ttk.Label(self.result_frame, text="Macro Avg").grid(row=sep_row + 1, column=0)
            ttk.Label(self.result_frame, text=f"{macro_precision:.2f}").grid(row=sep_row + 1, column=1)
            ttk.Label(self.result_frame, text=f"{macro_recall:.2f}").grid(row=sep_row + 1, column=2)
            ttk.Label(self.result_frame, text=f"{macro_f1:.2f}").grid(row=sep_row + 1, column=3)

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid integers only.")


if __name__ == "__main__":
    root = tk.Tk()
    app = ConfusionMatrixApp(root)
    root.mainloop()
