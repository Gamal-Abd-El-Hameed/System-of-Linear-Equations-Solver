import datetime
import time
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from GaussJaccobi.GaussSeidil import GaussSeidil
from GaussJaccobi.Jacobi import Jacobi
from Gauss.GaussEliminator import GaussEliminator
from GJ.FloatChopper import FloatChopper
from GJ.FloatRounder import FloatRounder
from GJ.GaussJordan import Gauss_Jordan
from inputHandler import *
from LU.LUController import *


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.initial_guess_entry = None
        self.l4 = None
        self.l3 = None
        self.l2 = None
        self.l1 = None
        self.l0 = None
        self.epsilon_entry = None
        self.iterations_used = None
        self.lu_options = None
        self.digits_used = None
        self.equations_input = None
        self.method_menu = None
        self.submit_button = None

        self.title('Numerical Project')
        self.geometry("1300x410")

        self.number_of_iterations = tk.StringVar()
        self.number_of_iterations.set("50")

        self.epsilon = tk.StringVar()
        self.epsilon.set("10**-5")

        self.lu_config = tk.StringVar()
        self.lu_config.set("Doolittle")

        self.number_of_digits = tk.StringVar()
        self.number_of_digits.set("7")

        self.methods = ["Gauss", "Gauss-Jordan", "LU", "Gauss-Seidel", "Jacobi"]
        self.operation_on_numbers = ["Rounding", "Chopping"]

        self.round_or_chop = tk.StringVar()
        self.round_or_chop.set("Operation on numbers")

        self.method_selected = tk.StringVar()
        self.method_selected.set("Select the method")
        # Define the grid
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)
        self.columnconfigure(5, weight=1)
        self.columnconfigure(6, weight=1)
        self.columnconfigure(7, weight=1)
        self.columnconfigure(8, weight=1)
        self.columnconfigure(9, weight=1)
        self.columnconfigure(10, weight=1)
        self.columnconfigure(11, weight=1)
        self.columnconfigure(12, weight=1)
        self.columnconfigure(13, weight=1)
        self.columnconfigure(14, weight=1)
        self.columnconfigure(15, weight=1)
        self.columnconfigure(16, weight=1)
        self.columnconfigure(17, weight=1)
        self.columnconfigure(18, weight=1)
        self.columnconfigure(19, weight=1)
        self.columnconfigure(20, weight=1)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(6, weight=1)
        self.rowconfigure(7, weight=1)
        self.rowconfigure(8, weight=1)
        self.rowconfigure(9, weight=1)
        self.rowconfigure(10, weight=1)
        self.rowconfigure(11, weight=1)
        self.rowconfigure(12, weight=1)
        self.rowconfigure(13, weight=1)
        self.rowconfigure(14, weight=1)
        self.rowconfigure(15, weight=1)
        self.rowconfigure(16, weight=1)
        self.rowconfigure(17, weight=1)
        self.rowconfigure(18, weight=1)
        # Creating The widgets
        self.create_widgets()

    def create_widgets(self):
        self.method_menu = ttk.OptionMenu(self, self.method_selected, self.method_selected.get(), *self.methods, command=self.toggle)
        self.method_menu.grid(column=0, row=0)

        self.method_menu = ttk.OptionMenu(self, self.round_or_chop, self.round_or_chop.get(), *self.operation_on_numbers)
        self.method_menu.grid(column=1, row=0)

        self.lu_options = ttk.OptionMenu(self, self.lu_config, self.lu_config.get(), *["Doolittle", "Crout"])

        self.l1 = ttk.Label(self, text="Digits:")
        self.l1.grid(column=19, row=0)
        self.digits_used = ttk.Entry(self, textvariable=self.number_of_digits, justify='center')
        self.digits_used.grid(column=20, row=0)

        self.l2 = ttk.Label(self, text="Iterations:")
        self.iterations_used = ttk.Entry(self, textvariable=self.number_of_iterations, justify='center')

        self.l3 = ttk.Label(self, text="Epsilon:")
        self.epsilon_entry = ttk.Entry(self, textvariable=self.epsilon, justify='center')

        self.l4 = ttk.Label(self, text="Initial guess", font=10)
        self.initial_guess_entry = scrolledtext.ScrolledText(self, wrap="none", width=25, height=10)

        self.l0 = ttk.Label(self, text="Equations", font=10)
        self.l0.grid(column=10, row=4)
        self.equations_input = scrolledtext.ScrolledText(self, wrap="none", width=60, height=15)
        self.equations_input.grid(column=10, row=5)

        self.submit_button = ttk.Button(self, text="Solve", command=self.solve_equations)
        self.submit_button.grid(column=10, row=7)

    def toggle(self, *args):
        self.lu_config.set("Doolittle")

        if self.number_of_digits.get() == "":
            self.number_of_digits.set("7")

        if self.epsilon.get() == "":
            self.epsilon.set("10**-5")

        if self.number_of_iterations.get() == "":
            self.number_of_iterations = "50"

        self.l2.grid_forget()
        self.l3.grid_forget()
        self.l4.grid_forget()
        self.iterations_used.grid_forget()
        self.epsilon_entry.grid_forget()
        self.initial_guess_entry.grid_forget()
        self.lu_options.grid_forget()

        if self.method_selected.get() == "LU":
            self.lu_options.grid(column=2, row=0)
        elif self.method_selected.get() == "Gauss-Seidel" or self.method_selected.get() == "Jacobi":
            self.l2.grid(column=19, row=1)
            self.iterations_used.grid(column=20, row=1)
            self.l3.grid(column=19, row=2)
            self.epsilon_entry.grid(column=20, row=2)
            self.l4.grid(column=19, row=4)
            self.initial_guess_entry.grid(column=19, row=5)

    def solve_equations(self):

        def close_error():
            error_window.destroy()

        def close_answer():
            answer_window.destroy()

        if self.epsilon.get() == "":
            self.epsilon.set("10**-5")

        eps = 10 ** -5
        initial_array = []

        if self.method_selected.get() == "Gauss-Seidel" or self.method_selected.get() == "Jacobi":
            try:
                eps = eval(self.epsilon.get())
            except:
                eps = 10 ** -5
                self.epsilon.set("10**-5")

        equations = self.equations_input.get('1.0', 'end')
        initial = self.initial_guess_entry.get('1.0', 'end')

        if equations == "\n":
            error_window = tk.Toplevel(self)
            error_window.geometry("400x100")
            error_window.title("Error!")
            l1 = ttk.Label(error_window, text=f"Error!", font=14)
            l1.pack()
            l2 = ttk.Label(error_window, text=f"Enter The equations", font=12)
            l2.pack()
            b1 = ttk.Button(error_window, text="OK", command=close_error)
            b1.pack()
            return

        if not self.number_of_iterations.get().isnumeric():
            self.number_of_iterations.set("50")

        if not self.number_of_digits.get().isnumeric():
            self.number_of_digits.set("7")

        if self.method_selected.get() == "Gauss-Seidel" or self.method_selected.get() == "Jacobi":
            if initial == "\n":
                error_window = tk.Toplevel(self)
                error_window.geometry("400x100")
                error_window.title("Error!")
                l1 = ttk.Label(error_window, text=f"Error!", font=14)
                l1.pack()
                l2 = ttk.Label(error_window, text=f"Enter The initial values", font=12)
                l2.pack()
                b1 = ttk.Button(error_window, text="OK", command=close_error)
                b1.pack()
                return

            initial_array = str.split(initial, "\n")
            i = len(initial_array) - 1
            while i >= 0:
                if initial_array[i] == "":
                    del initial_array[i]
                i = i - 1

            for k in range(len(initial_array)):
                try:
                    initial_array[k] = float(initial_array[k])
                except:
                    error_window = tk.Toplevel(self)
                    error_window.geometry("400x100")
                    error_window.title("Error!")
                    l1 = ttk.Label(error_window, text=f"Error!", font=14)
                    l2 = ttk.Label(error_window, text=f"Enter initial values correctly", font=12)
                    l1.pack()
                    l2.pack()
                    b1 = ttk.Button(error_window, text="OK", command=close_error)
                    b1.pack()
                    return

        if self.method_selected.get() == "LU":
            if self.lu_config.get() == "None":
                error_window = tk.Toplevel(self)
                error_window.geometry("400x100")
                error_window.title("Error!")
                l1 = ttk.Label(error_window, text=f"Error!", font=14)
                l2 = ttk.Label(error_window, text=f"Choose from a LU-Method", font=12)
                l1.pack()
                l2.pack()
                b1 = ttk.Button(error_window, text="OK", command=close_error)
                b1.pack()
                return

        if self.method_selected.get() == "Select the method" or self.round_or_chop.get() == "Operation on numbers":
            error_window = tk.Toplevel(self)
            error_window.geometry("400x100")
            error_window.title("Error!")
            l1 = ttk.Label(error_window, text=f"Error!", font=14)
            l2 = ttk.Label(error_window, text=f"Choose from option-menu", font=12)
            l1.pack()
            l2.pack()
            b1 = ttk.Button(error_window, text="OK", command=close_error)
            b1.pack()
            return

        answer_window = tk.Toplevel(self)
        answer_window.geometry("600x400")
        answer_window.title("Solution")

        answer_window.columnconfigure(0, weight=1)
        answer_window.columnconfigure(1, weight=1)
        answer_window.columnconfigure(2, weight=1)
        answer_window.columnconfigure(3, weight=1)
        answer_window.columnconfigure(4, weight=1)
        answer_window.columnconfigure(5, weight=1)
        answer_window.columnconfigure(6, weight=1)

        answer_window.rowconfigure(0, weight=1)
        answer_window.rowconfigure(1, weight=1)
        answer_window.rowconfigure(2, weight=1)
        answer_window.rowconfigure(3, weight=1)
        answer_window.rowconfigure(4, weight=1)
        answer_window.rowconfigure(5, weight=1)
        answer_window.rowconfigure(6, weight=1)

        l1 = ttk.Label(answer_window, text=f"Solved By {self.method_selected.get()}", font=14)
        l1.grid(column=3, row=0)

        equations_array = str.split(equations, "\n")
        time_before = time.perf_counter_ns()

        try:
            input_handler = InputHandler(equations_array)
            coefficients, variables, constants = input_handler.getAug()
        except:
            answer_window.destroy()
            error_window = tk.Toplevel(self)
            error_window.geometry("400x100")
            error_window.title("Error!")
            l1 = ttk.Label(error_window, text=f"Error!", font=14)
            l2 = ttk.Label(error_window, text=f"Check the equations", font=12)
            l1.pack()
            l2.pack()
            b1 = ttk.Button(error_window, text="OK", command=close_error)
            b1.pack()
            return

        answer = []

        if self.round_or_chop.get() == "Rounding":
            float_converter = FloatRounder(int(self.number_of_digits.get()))
        elif self.round_or_chop.get() == "Chopping":
            float_converter = FloatChopper(int(self.number_of_digits.get()))
        else:
            float_converter = None

        if self.method_selected.get() == "Gauss":
            try:
                gauss = GaussEliminator(coefficients, constants, float_converter)
                answer = gauss.solve()
            except:
                answer_window.destroy()
                error_window = tk.Toplevel(self)
                error_window.geometry("400x100")
                error_window.title("Error!")
                l1 = ttk.Label(error_window, text=f"Error!", font=14)
                l2 = ttk.Label(error_window, text=f"Check the input", font=12)
                l1.pack()
                l2.pack()
                b1 = ttk.Button(error_window, text="OK", command=close_error)
                b1.pack()
                return

        elif self.method_selected.get() == "Gauss-Jordan":
            try:
                gauss_jordan = Gauss_Jordan(coefficients, constants, float_converter)
                answer = gauss_jordan.solve()
            except:
                answer_window.destroy()
                error_window = tk.Toplevel(self)
                error_window.geometry("400x100")
                error_window.title("Error!")
                l1 = ttk.Label(error_window, text=f"Error!", font=14)
                l2 = ttk.Label(error_window, text=f"Check the input", font=12)
                l1.pack()
                l2.pack()
                b1 = ttk.Button(error_window, text="OK", command=close_error)
                b1.pack()
                return

        elif self.method_selected.get() == "LU":
            try:
                lu = LUController(self.lu_config.get(), coefficients, constants, float_converter)
                answer = lu.solve()
            except ZeroDivisionError:
                answer_window.destroy()
                error_window = tk.Toplevel(self)
                error_window.geometry("400x100")
                error_window.title("Error!")
                l1 = ttk.Label(error_window, text=f"Error!", font=14)
                l2 = ttk.Label(error_window, text=f"Diagonal contains zeros!", font=12)
                l1.pack()
                l2.pack()
                b1 = ttk.Button(error_window, text="OK", command=close_error)
                b1.pack()
                return
            except:
                answer_window.destroy()
                error_window = tk.Toplevel(self)
                error_window.geometry("400x100")
                error_window.title("Error!")
                l1 = ttk.Label(error_window, text=f"Error!", font=14)
                l2 = ttk.Label(error_window, text=f"Check the input", font=12)
                l1.pack()
                l2.pack()
                b1 = ttk.Button(error_window, text="OK", command=close_error)
                b1.pack()
                return


        elif self.method_selected.get() == "Gauss-Seidel":
            try:
                gauss_seidel = GaussSeidil(coefficients, constants, int(self.number_of_iterations.get()), eps, initial_array, float_converter)
                answer = gauss_seidel.solve()
            except ValueError:
                answer_window.destroy()
                error_window = tk.Toplevel(self)
                error_window.geometry("400x100")
                error_window.title("Error!")
                l1 = ttk.Label(error_window, text=f"Error!", font=14)
                l2 = ttk.Label(error_window, text=f"The method diverges!", font=12)
                l1.pack()
                l2.pack()
                b1 = ttk.Button(error_window, text="OK", command=close_error)
                b1.pack()
                return
            except ZeroDivisionError:
                answer_window.destroy()
                error_window = tk.Toplevel(self)
                error_window.geometry("400x100")
                error_window.title("Error!")
                l1 = ttk.Label(error_window, text=f"Error!", font=14)
                l2 = ttk.Label(error_window, text=f"Diagonal contains zeros!", font=12)
                l1.pack()
                l2.pack()
                b1 = ttk.Button(error_window, text="OK", command=close_error)
                b1.pack()
                return

        elif self.method_selected.get() == "Jacobi":
            try:
                jacobi = Jacobi(coefficients, constants, int(self.number_of_iterations.get()), eps, initial_array, float_converter)
                answer = jacobi.solve()
            except ValueError:
                answer_window.destroy()
                error_window = tk.Toplevel(self)
                error_window.geometry("400x100")
                error_window.title("Error!")
                l1 = ttk.Label(error_window, text=f"Error!", font=14)
                l2 = ttk.Label(error_window, text=f"The method diverges!", font=12)
                l1.pack()
                l2.pack()
                b1 = ttk.Button(error_window, text="OK", command=close_error)
                b1.pack()
                return
            except ZeroDivisionError:
                answer_window.destroy()
                error_window = tk.Toplevel(self)
                error_window.geometry("400x100")
                error_window.title("Error!")
                l1 = ttk.Label(error_window, text=f"Error!", font=14)
                l2 = ttk.Label(error_window, text=f"Diagonal contains zeros!", font=12)
                l1.pack()
                l2.pack()
                b1 = ttk.Button(error_window, text="OK", command=close_error)
                b1.pack()
                return

        time_after = time.perf_counter_ns()
        time_taken = (time_after - time_before)

        l2 = ttk.Label(answer_window, text=f"Time Before = {time_before} ns")
        l2.grid(column=0, row=1)
        l3 = ttk.Label(answer_window, text=f"Time Taken = {time_taken} ns")
        l3.grid(column=3, row=1)
        l3 = ttk.Label(answer_window, text=f"Time After = {time_after} ns")
        l3.grid(column=6, row=1)

        results = ""
        for i in range(len(answer)):
            results = results + f"{variables[i]} = {answer[i]}\n"

        l4 = ttk.Label(answer_window, text=results, font=10)
        l4.grid(column=3, row=2)

        b1 = ttk.Button(answer_window, text="OK", command=close_answer)
        b1.grid(column=3, row=5)


if __name__ == "__main__":
    app = App()
    app.mainloop()
