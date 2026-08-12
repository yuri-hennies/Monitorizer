import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("My program")
root.geometry("700x400")

columns = ("Name", "Age", "City")

table = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
	table.heading(col, text = col)
	table.column(col, width=150)

table.insert("", "end", values=("John", 25, "New York"))
table.insert("", "end", values=("Alice", 31, "London"))
table.insert("", "end", values=("Bob", 28, "Tokyo"))

table.pack(fill="both", expand=True, padx=15, pady=15)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

def button1():
	print("Button 1 pressed")

def button2():
	print("Button 2 pressed")


btn1 = tk.Button(button_frame, text="Button 1", command=button1)
btn1.pack(side="left", padx=5)

btn2 = tk.Button(button_frame, text="Button 2", command=button2)
btn2.pack(side="left", padx=5)

root.mainloop()