import tkinter as tk

def show_message():
    message.config(text="Hello! You clicked the button.")

root = tk.Tk()
root.title("Tkinter Hello World")
root.geometry("350x180")

message = tk.Label(root, text="Hello from Tkinter!", font=("Arial", 14))
message.pack(pady=25)

button = tk.Button(root, text="Click me", command=show_message)
button.pack()

root.mainloop()
