import tkinter as tk
from tkinter import messagebox, StringVar, OptionMenu
import sympy as sp

class MatrixCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Matrix Calculator")

        # Set the desired font (Hack) for all Entry and Text widgets
        self.entry_font = ("Hack", 14)  # Change font size to 14
        self.text_font = ("Hack", 14)

        # Create the top frame for matrix dimension inputs
        self.top_frame = tk.Frame(root)
        self.top_frame.grid(row=0, column=0, padx=10, pady=5)

        # Labels and entries for matrix dimensions
        self.label_matrix_a = tk.Label(self.top_frame, text="Matrix A Dimensions:")
        self.label_matrix_a.grid(row=0, column=0, padx=10, pady=5)

        self.rows_a_entry = tk.Entry(self.top_frame, width=5, font=self.entry_font)
        self.rows_a_entry.grid(row=0, column=1, padx=5)
        self.cols_a_entry = tk.Entry(self.top_frame, width=5, font=self.entry_font)
        self.cols_a_entry.grid(row=0, column=2, padx=5)

        self.label_matrix_b = tk.Label(self.top_frame, text="Matrix B Dimensions:")
        self.label_matrix_b.grid(row=1, column=0, padx=10, pady=5)

        self.rows_b_entry = tk.Entry(self.top_frame, width=5, font=self.entry_font)
        self.rows_b_entry.grid(row=1, column=1, padx=5)
        self.cols_b_entry = tk.Entry(self.top_frame, width=5, font=self.entry_font)
        self.cols_b_entry.grid(row=1, column=2, padx=5)

        # Dropdown for choosing operation type
        self.operation_var = StringVar(root)
        self.operation_var.set("Multiply")  # Set default value
        self.operation_menu = OptionMenu(self.top_frame, self.operation_var, "Multiply", "Dot Product", "Cross Product")
        self.operation_menu.grid(row=2, column=3, padx=10, pady=5)

        # Button to generate matrix inputs
        self.generate_button = tk.Button(self.top_frame, text="Generate Matrices", command=self.generate_matrix_inputs)
        self.generate_button.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        # Create frame for matrix inputs (separate from top_frame)
        self.matrix_frame = tk.Frame(root)
        self.matrix_frame.grid(row=3, column=0, padx=10, pady=10)

        # Create frame for result and calculate button
        self.bottom_frame = tk.Frame(root)
        self.bottom_frame.grid(row=4, column=0, padx=10, pady=10)

        # Result text box (read-only)
        self.result_text = tk.Text(self.bottom_frame, height=10, width=50, font=self.text_font, state=tk.DISABLED)  # Set to disabled to make it read-only
        self.result_text.pack(pady=5)

        # Button to calculate result
        self.calculate_button = tk.Button(self.bottom_frame, text="Calculate", command=self.calculate)
        self.calculate_button.pack(pady=5)

    def generate_matrix_inputs(self):
        # Clear existing inputs
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()

        # Get dimensions of matrix A and B
        try:
            rows_a = int(self.rows_a_entry.get()) if self.rows_a_entry.get() else 0
            cols_a = int(self.cols_a_entry.get()) if self.cols_a_entry.get() else rows_a
            rows_b = int(self.rows_b_entry.get()) if self.rows_b_entry.get() else 0
            cols_b = int(self.cols_b_entry.get()) if self.cols_b_entry.get() else rows_b
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid dimensions")
            return

        # Check if matrix operations are valid
        operation = self.operation_var.get()
        if operation == "Multiply" and cols_a != rows_b:
            messagebox.showerror("Dimension Error", "Number of columns in A must equal number of rows in B for multiplication")
            return
        elif operation == "Dot Product" and (cols_a != cols_b or rows_a != 1 or rows_b != 1):
            messagebox.showerror("Dimension Error", "Dot Product requires both matrices to be 1xN")
            return
        elif operation == "Cross Product" and (cols_a != 3 or cols_b != 3 or rows_a != 1 or rows_b != 1):
            messagebox.showerror("Dimension Error", "Cross Product requires both matrices to be 1x3")

        # Create input fields for matrix A
        tk.Label(self.matrix_frame, text="Matrix A:").grid(row=0, column=0, padx=10, pady=5, sticky='w')
        self.matrix_a_entries = []
        for i in range(rows_a):
            row_entries = []
            for j in range(cols_a):
                entry = tk.Entry(self.matrix_frame, width=7, font=self.entry_font)  # Apply Hack font
                entry.grid(row=i+1, column=j, padx=5, pady=5)
                row_entries.append(entry)
            self.matrix_a_entries.append(row_entries)

        # Create input fields for matrix B
        tk.Label(self.matrix_frame, text="Matrix B:").grid(row=rows_a+1, column=0, padx=10, pady=5, sticky='w')
        self.matrix_b_entries = []
        for i in range(rows_b):
            row_entries = []
            for j in range(cols_b):
                entry = tk.Entry(self.matrix_frame, width=7, font=self.entry_font)  # Apply Hack font
                entry.grid(row=i+rows_a+2, column=j, padx=5, pady=5)
                row_entries.append(entry)
            self.matrix_b_entries.append(row_entries)

    def get_matrix_from_entries(self, entries):
        rows = len(entries)
        cols = len(entries[0])
        matrix = []
        for i in range(rows):
            row = []
            for j in range(cols):
                element = entries[i][j].get().strip()  # Get element from entry and strip any extra spaces
                if element == "":  # If entry is empty, treat it as 0
                    element = "0"
                row.append(sp.sympify(element))  # Convert string input to sympy expression
            matrix.append(row)
        return sp.Matrix(matrix)

    def pretty_print_matrix(self, matrix):
        # Convert the matrix to a pretty string
        pretty_str = sp.pretty(matrix, use_unicode=True)  # Use Unicode for better formatting
        return pretty_str.replace('**', '()^')  # Ensure exponentiation is formatted correctly

    def calculate(self):
        try:
            # Retrieve matrices A and B from entries
            A = self.get_matrix_from_entries(self.matrix_a_entries)
            B = self.get_matrix_from_entries(self.matrix_b_entries)

            operation = self.operation_var.get()
            if operation == "Multiply":
                # Perform matrix multiplication
                result = A * B
            elif operation == "Dot Product":
                # Perform dot product (1xN * Nx1)
                result = A.dot(B.transpose()).expand()  # Dot product
            elif operation == "Cross Product":
                # Perform cross product (1x3 * 1x3)
                result = sp.Matrix([[A[0, 0] * B[0, 1] - A[0, 1] * B[0, 0], 
                                     A[0, 1] * B[0, 2] - A[0, 2] * B[0, 1], 
                                     A[0, 2] * B[0, 0] - A[0, 0] * B[0, 2]]])

            # Get pretty printed result
            formatted_result = self.pretty_print_matrix(result)

            # Display result in the text box
            self.result_text.config(state=tk.NORMAL)  # Enable editing temporarily to insert text
            self.result_text.delete(1.0, tk.END)  # Clear previous result
            self.result_text.insert(tk.END, formatted_result)  # Insert formatted result
            self.result_text.config(state=tk.DISABLED)  # Disable editing again
            print(formatted_result)
        except Exception as e:
            messagebox.showerror("Calculation Error", str(e))

# Create the main application window
root = tk.Tk()
app = MatrixCalculator(root)
root.mainloop()
