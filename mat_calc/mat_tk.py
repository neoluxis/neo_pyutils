import tkinter as tk
from tkinter import messagebox, Entry, Text, Button, Toplevel
import sympy as sp

class MatrixCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Matrix Calculator")

        self.matrices = {}  # Store matrices by name
        self.last_matrix = None  # Keep track of the last matrix used

        # Create main frame
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(padx=10, pady=10)

        # Add button to create new matrix
        self.add_matrix_button = Button(self.main_frame, text="+ Add Matrix", command=self.add_matrix)
        self.add_matrix_button.pack(pady=5)

        # Frame for matrix buttons (horizontal layout)
        self.matrix_buttons_frame = tk.Frame(self.main_frame)
        self.matrix_buttons_frame.pack(pady=5)

        # Frame for operation input
        self.operation_frame = tk.Frame(self.main_frame)
        self.operation_frame.pack(pady=5)

        self.operation_label = tk.Label(self.operation_frame, text="Define Matrix Operation:")
        self.operation_label.pack(side=tk.LEFT)

        self.operation_entry = Entry(self.operation_frame, width=40)
        self.operation_entry.pack(side=tk.LEFT)

        self.calculate_button = Button(self.operation_frame, text="Calculate", command=self.calculate)
        self.calculate_button.pack(side=tk.LEFT, padx=5)

        # Symbol area for matrices and operations
        self.symbol_frame = tk.Frame(self.main_frame)
        self.symbol_frame.pack(pady=5)

        self.matrix_symbols_label = tk.Label(self.symbol_frame, text="Matrices:")
        self.matrix_symbols_label.grid(row=0, column=0)

        self.operation_symbols_label = tk.Label(self.symbol_frame, text="Operations:")
        self.operation_symbols_label.grid(row=1, column=0)

        self.populate_symbol_area()  # Populate symbol buttons

        # Result text box (read-only)
        self.result_text = Text(self.main_frame, height=10, width=50, font=("Hack", 14), state=tk.DISABLED)
        self.result_text.pack(pady=5)

    def populate_symbol_area(self):
        # Matrix buttons
        col = 1
        for name in self.matrices.keys():
            button = Button(self.symbol_frame, text=name, command=lambda n=name: self.insert_to_entry(n))
            button.grid(row=0, column=col, padx=5, pady=5)
            col += 1

        # Operation buttons (includes parentheses now)
        operations = ["+", "-", "*", "**", "T", "outer", "inner", "(", ")"]
        for i, operation in enumerate(operations):
            if operation == "T":
                button = Button(self.symbol_frame, text="T", command=lambda op=".T": self.insert_to_entry(op))
            else:
                button = Button(self.symbol_frame, text=operation, command=lambda op=operation: self.insert_to_entry(op))
            button.grid(row=1, column=i + 1, padx=5, pady=5)

    def add_matrix(self):
        self.add_matrix_window = Toplevel(self.root)
        self.add_matrix_window.title("Create New Matrix")

        tk.Label(self.add_matrix_window, text="Matrix Name:").pack(pady=5)
        self.matrix_name_entry = Entry(self.add_matrix_window)
        self.matrix_name_entry.pack(pady=5)

        tk.Label(self.add_matrix_window, text="Rows (m):").pack(pady=5)
        self.rows_entry = Entry(self.add_matrix_window)
        self.rows_entry.pack(pady=5)

        tk.Label(self.add_matrix_window, text="Cols (n):").pack(pady=5)
        self.cols_entry = Entry(self.add_matrix_window)
        self.cols_entry.pack(pady=5)

        self.next_button = Button(self.add_matrix_window, text="Next", command=self.create_matrix_entries)
        self.next_button.pack(pady=10)

    def create_matrix_entries(self):
        matrix_name = self.matrix_name_entry.get()
        try:
            rows = int(self.rows_entry.get())
            cols = int(self.cols_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid dimensions")
            return

        if matrix_name in self.matrices:
            messagebox.showerror("Input Error", "Matrix name already exists")
            return

        self.add_matrix_window.destroy()  # Close the current window
        self.matrix_entries_window = Toplevel(self.root)
        self.matrix_entries_window.title(f"Input Elements for {matrix_name}")

        self.entries = []
        for i in range(rows):
            row_entries = []
            for j in range(cols):
                entry = Entry(self.matrix_entries_window, width=7)
                entry.grid(row=i, column=j, padx=5, pady=5)
                row_entries.append(entry)
            self.entries.append(row_entries)

        finish_button = Button(self.matrix_entries_window, text="Finish", command=lambda: self.finish_matrix(matrix_name))
        finish_button.grid(row=rows, columnspan=cols, pady=10)

    def finish_matrix(self, matrix_name):
        matrix = []
        for row in self.entries:
            matrix_row = []
            for entry in row:
                value = entry.get().strip() or "0"  # Treat empty as 0
                matrix_row.append(sp.sympify(value))
            matrix.append(matrix_row)

        self.matrices[matrix_name] = sp.Matrix(matrix)  # Store matrix by name
        self.last_matrix = matrix_name  # Update last matrix used
        self.update_matrix_buttons()  # Refresh the button list

        messagebox.showinfo("Success", f"Matrix '{matrix_name}' created successfully!")
        self.matrix_entries_window.destroy()
        self.populate_symbol_area()  # Update symbol area with new matrix

    def update_matrix_buttons(self):
        for widget in self.matrix_buttons_frame.winfo_children():
            widget.destroy()

        col = 0
        for name in self.matrices.keys():
            button = Button(self.matrix_buttons_frame, text=name, command=lambda n=name: self.modify_matrix(n))
            button.grid(row=0, column=col, padx=5, pady=5)  # Horizontal layout
            col += 1

    def insert_to_entry(self, value):
        current_text = self.operation_entry.get()
        self.operation_entry.delete(0, tk.END)  # Clear current entry
        self.operation_entry.insert(0, current_text + value)  # Append the selected value

    def modify_matrix(self, matrix_name):
        matrix = self.matrices[matrix_name]
        self.matrix_entries_window = Toplevel(self.root)
        self.matrix_entries_window.title(f"Modify Matrix: {matrix_name}")

        rows, cols = matrix.shape
        self.entries = []
        for i in range(rows):
            row_entries = []
            for j in range(cols):
                entry = Entry(self.matrix_entries_window, width=7)
                entry.grid(row=i, column=j, padx=5, pady=5)
                entry.insert(tk.END, str(matrix[i, j]))  # Populate with current values
                row_entries.append(entry)
            self.entries.append(row_entries)

        finish_button = Button(self.matrix_entries_window, text="Update", command=lambda: self.update_matrix(matrix_name))
        finish_button.grid(row=rows, columnspan=cols, pady=10)

    def update_matrix(self, matrix_name):
        matrix = []
        for row in self.entries:
            matrix_row = []
            for entry in row:
                value = entry.get().strip() or "0"  # Treat empty as 0
                matrix_row.append(sp.sympify(value))
            matrix.append(matrix_row)

        self.matrices[matrix_name] = sp.Matrix(matrix)  # Update matrix

        messagebox.showinfo("Success", f"Matrix '{matrix_name}' updated successfully!")
        self.matrix_entries_window.destroy()

    def calculate(self):
        operation = self.operation_entry.get()
        try:
            result = eval(operation, {}, self.matrices)
            formatted_result = sp.pretty(result, use_unicode=True).replace('**', '()^')

            self.result_text.config(state=tk.NORMAL)  # Enable editing temporarily
            self.result_text.delete(1.0, tk.END)  # Clear previous result
            self.result_text.insert(tk.END, formatted_result)  # Insert formatted result
            self.result_text.config(state=tk.DISABLED)  # Disable editing again
        except Exception as e:
            messagebox.showerror("Calculation Error", str(e))

# Create the main application window
root = tk.Tk()
app = MatrixCalculator(root)
root.mainloop()
