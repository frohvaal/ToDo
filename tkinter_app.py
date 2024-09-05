import tkinter as tk
from tkinter import messagebox, simpledialog
import requests

API_URL = "http://127.0.0.1:5000/todos"

def get_todos():
    response = requests.get(API_URL)
    if response.status_code == 200:
        todos = response.json()
        listbox.delete(0, tk.END)
        for todo in todos:
            listbox.insert(tk.END, f"{todo['id']}: {todo['title']} - {'Completed' if todo['is_completed'] else 'Pending'}")
    else:
        messagebox.showerror("Error", "Failed to fetch To-Dos")

def add_todo():
    title = simpledialog.askstring("Input", "Enter To-Do Title")
    if title:
        data = {"title": title, "description": "", "is_completed": False}
        response = requests.post(API_URL, json=data)
        if response.status_code == 201:
            get_todos()
        else:
            messagebox.showerror("Error", "Failed to add To-Do")

def edit_todo():
    selected = listbox.curselection()
    if selected:
        todo_id = listbox.get(selected).split(":")[0]
        title = simpledialog.askstring("Input", "Enter new title")
        if title:
            data = {"title": title}
            response = requests.put(f"{API_URL}/{todo_id}", json=data)
            if response.status_code == 200:
                get_todos()
            else:
                messagebox.showerror("Error", "Failed to edit To-Do")

def delete_todo():
    selected = listbox.curselection()
    if selected:
        todo_id = listbox.get(selected).split(":")[0]
        response = requests.delete(f"{API_URL}/{todo_id}")
        if response.status_code == 200:
            get_todos()
        else:
            messagebox.showerror("Error", "Failed to delete To-Do")

app = tk.Tk()
app.title("To-Do Manager")

frame = tk.Frame(app)
frame.pack(pady=20)

listbox = tk.Listbox(frame, width=50, height=10)
listbox.pack(side=tk.LEFT, padx=20)

scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

btn_frame = tk.Frame(app)
btn_frame.pack(pady=20)

btn_get = tk.Button(btn_frame, text="Get To-Dos", command=get_todos)
btn_get.pack(side=tk.LEFT, padx=10)

btn_add = tk.Button(btn_frame, text="Add To-Do", command=add_todo)
btn_add.pack(side=tk.LEFT, padx=10)

btn_edit = tk.Button(btn_frame, text="Edit To-Do", command=edit_todo)
btn_edit.pack(side=tk.LEFT, padx=10)

btn_delete = tk.Button(btn_frame, text="Delete To-Do", command=delete_todo)
btn_delete.pack(side=tk.LEFT, padx=10)

app.mainloop()
