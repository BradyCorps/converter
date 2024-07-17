import tkinter as tk
from tkinter import messagebox
import shelve

def convert_column_to_semicolon_list(data):
    # Split the input data by new lines and strip any leading/trailing whitespace
    data = data.strip().split('\n')
    data = [item.strip() for item in data]

    # Convert the list to a semicolon-separated string
    semicolon_separated_list = ";".join(data)

    return semicolon_separated_list

def on_convert_button_click():
    # Get the input data from the text field
    input_data = text_input.get("1.0", tk.END)

    # Convert the input data to a semicolon-separated list
    result = convert_column_to_semicolon_list(input_data)

    # Display the result in the output field
    text_output.delete("1.0", tk.END)
    text_output.insert(tk.END, result)

    # Save the result to persistent storage
    save_conversion(result)

    # Update the last 5 conversions display
    update_last_conversions_display()

def save_conversion(conversion):
    with shelve.open('conversions.db') as db:
        if 'conversions' not in db:
            db['conversions'] = []
        conversions = db['conversions']
        conversions.insert(0, conversion)  # Insert the new conversion at the beginning
        if len(conversions) > 5:
            conversions = conversions[:5]  # Keep only the last 5 conversions
        db['conversions'] = conversions

def load_last_conversions():
    with shelve.open('conversions.db') as db:
        return db.get('conversions', [])

def update_last_conversions_display():
    conversions = load_last_conversions()
    last_conversions_display.delete("1.0", tk.END)
    for conversion in conversions:
        last_conversions_display.insert(tk.END, conversion + "\n\n")

# Create the main application window
root = tk.Tk()
root.title("Column to Semicolon List Converter")

# Create and place the input text field
text_input_label = tk.Label(root, text="Input Column Data:")
text_input_label.pack()
text_input = tk.Text(root, height=10, width=50)
text_input.pack()

# Create and place the convert button
convert_button = tk.Button(root, text="Convert", command=on_convert_button_click)
convert_button.pack()

# Create and place the output text field
text_output_label = tk.Label(root, text="Semicolon-Separated List:")
text_output_label.pack()
text_output = tk.Text(root, height=10, width=50)
text_output.pack()

# Create and place the last 5 conversions display
last_conversions_label = tk.Label(root, text="Last 5 Conversions:")
last_conversions_label.pack()
last_conversions_display = tk.Text(root, height=10, width=50)
last_conversions_display.pack()

# Load and display the last 5 conversions
update_last_conversions_display()

# Run the Tkinter event loop
root.mainloop()
