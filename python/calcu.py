import customtkinter as ctk

# Set the dark theme
ctk.set_appearance_mode("dark")  # Use dark mode
ctk.set_default_color_theme(
    "dark-blue"
)  # You can change to other built-in themes like "green" or "blue"

# Initialize the CustomTkinter app
app = ctk.CTk()  # Creating the root window
app.geometry("400x500")  # Larger window size
app.title("Dark Calculator")

# Define the display entry field
entry = ctk.CTkEntry(app, width=380, height=70, justify="right", font=("Arial", 28))
entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10)


# Global variable to store expression
expression = ""


# Function to update the expression in the entry widget
def press(num):
    global expression
    expression += str(num)
    entry.delete(0, ctk.END)  # Clear the current entry
    entry.insert(ctk.END, expression)  # Insert new text


# Function to evaluate the expression
def equal_press():
    global expression
    try:
        result = str(eval(expression))  # Evaluate the expression
        entry.delete(0, ctk.END)
        entry.insert(ctk.END, result)  # Display result
        expression = result  # Store the result as the new expression
    except Exception as e:
        entry.delete(0, ctk.END)
        entry.insert(ctk.END, "Error")
        expression = ""


# Function to clear the display
def clear():
    global expression
    expression = ""
    entry.delete(0, ctk.END)


# Function to create buttons with larger size
def create_button(text, row, column, command):
    button = ctk.CTkButton(
        app, text=text, width=90, height=70, font=("Arial", 20), command=command
    )
    button.grid(row=row, column=column, padx=10, pady=10)


# Creating number buttons
numbers = [
    (7, 1, 0),
    (8, 1, 1),
    (9, 1, 2),
    (4, 2, 0),
    (5, 2, 1),
    (6, 2, 2),
    (1, 3, 0),
    (2, 3, 1),
    (3, 3, 2),
    (0, 4, 1),
]

for num, row, col in numbers:
    create_button(num, row, col, lambda num=num: press(num))

# Creating operator buttons
operators = [("+", 1, 3), ("-", 2, 3), ("*", 3, 3), ("/", 4, 3)]
for op, row, col in operators:
    create_button(op, row, col, lambda op=op: press(op))

# Creating special buttons
create_button("C", 4, 0, clear)  # Clear button
create_button("=", 4, 2, equal_press)  # Equals button

# Start the Tkinter main loop
app.mainloop()
