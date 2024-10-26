import sympy as sp

def input_matrix(rows, cols, matrix_name):
    """
    Helper function to input a matrix. Elements can include symbolic expressions.
    """
    matrix = []
    print(f"Input elements for matrix {matrix_name} (use sympy expressions like 'cos(theta)' if needed):")
    for i in range(rows):
        row = []
        for j in range(cols):
            element = input(f"Element [{i+1}, {j+1}]: ")
            # Parse the input string as a sympy expression
            row.append(sp.sympify(element))
        matrix.append(row)
    return sp.Matrix(matrix)

def multiply_matrices(A, B):
    """
    Multiplies two matrices A and B, where A and B are sympy matrices.
    """
    try:
        # Attempt matrix multiplication
        result = A * B
        return result
    except Exception as e:
        print(f"Error in multiplication: {e}")
        return None

def main():
    # Input dimensions for matrix A
    rows_A = int(input("Enter number of rows for matrix A: "))
    cols_A = int(input("Enter number of columns for matrix A: "))

    # Input dimensions for matrix B
    rows_B = int(input("Enter number of rows for matrix B: "))
    cols_B = int(input("Enter number of columns for matrix B: "))

    # Check if matrices can be multiplied (cols_A == rows_B)
    if cols_A != rows_B:
        print("Error: Number of columns in A must be equal to the number of rows in B for matrix multiplication.")
        return

    # Input matrices A and B
    A = input_matrix(rows_A, cols_A, 'A')
    B = input_matrix(rows_B, cols_B, 'B')

    print("\nMatrix A:")
    sp.pprint(A)

    print("\nMatrix B:")
    sp.pprint(B)

    # Multiply matrices
    result = multiply_matrices(A, B)

    if result is not None:
        print("\nResult of A * B:")
        sp.pprint(result)

if __name__ == "__main__":
    main()

