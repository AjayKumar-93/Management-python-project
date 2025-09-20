import json
import os
import tkinter as tk
from tkinter import messagebox, scrolledtext

DATA_FILE = "students.json"

# ---------- Helper Functions ----------
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ---------- Core Functionalities ----------
def add_student():
    name = name_entry.get().strip()
    roll = roll_entry.get().strip()
    marks = marks_entry.get().strip()

    if not name or not roll or not marks:
        messagebox.showwarning("Missing Data", "Please fill all fields.")
        return

    try:
        marks = float(marks)
    except ValueError:
        messagebox.showerror("Invalid Input", "Marks must be a number.")
        return

    data = load_data()
    if roll in data:
        messagebox.showerror("Duplicate Entry", f"Student with Roll Number {roll} already exists.")
    else:
        data[roll] = {"name": name, "marks": marks}
        save_data(data)
        messagebox.showinfo("Success", f"Student '{name}' added successfully!")
        name_entry.delete(0, tk.END)
        roll_entry.delete(0, tk.END)
        marks_entry.delete(0, tk.END)

def search_student():
    roll = roll_entry.get().strip()
    if not roll:
        messagebox.showwarning("Missing Data", "Enter Roll Number to search.")
        return

    data = load_data()
    if roll in data:
        student = data[roll]
        messagebox.showinfo("Student Found", f"ROLL: {roll}\nNAME: {student['name']}\nMARKS: {student['marks']}")
    else:
        messagebox.showerror("Not Found", f"No student found with Roll Number {roll}.")

def display_all_students():
    data = load_data()
    if not data:
        messagebox.showinfo("No Data", "No student records available.")
        return

    win = tk.Toplevel(root)
    win.title("All Students")
    win.geometry("400x300")

    txt = scrolledtext.ScrolledText(win, wrap=tk.WORD, width=50, height=15, font=("Courier", 11))
    txt.pack(padx=10, pady=10)

    txt.insert(tk.END, f"{'ROLL':<10} {'NAME':<20} {'MARKS':<10}\n")
    txt.insert(tk.END, "-" * 40 + "\n")
    for roll, details in data.items():
        txt.insert(tk.END, f"{roll:<10} {details['name']:<20} {details['marks']:<10}\n")
    txt.config(state=tk.DISABLED)

def find_topper():
    data = load_data()
    if not data:
        messagebox.showinfo("No Data", "No student records available.")
        return

    top_roll = max(data, key=lambda x: data[x]['marks'])
    topper = data[top_roll]
    messagebox.showinfo("Topper", f"ROLL: {top_roll}\nNAME: {topper['name']}\nMARKS: {topper['marks']}")

# ---------- Toggle Modes ----------
def toggle_search_mode():
    """Hide Name & Marks fields, show only Roll Number + Back button."""
    name_label.pack_forget()
    name_entry.pack_forget()
    marks_label.pack_forget()
    marks_entry.pack_forget()

    search_btn.config(state=tk.DISABLED)  # disable search button
    add_btn.config(state=tk.DISABLED)     # disable add button

    # Show back button
    global back_btn
    back_btn = tk.Button(root, text="Back to Add Mode", font=("Arial", 12, "bold"), bg="lightgray", command=restore_add_mode, width=20)
    back_btn.pack(pady=5)

    search_student()

def restore_add_mode():
    """Show Name & Marks fields again for adding students."""
    name_label.pack()
    name_entry.pack()
    marks_label.pack()
    marks_entry.pack()

    search_btn.config(state=tk.NORMAL)
    add_btn.config(state=tk.NORMAL)

    back_btn.destroy()  # remove back button

# ---------- GUI Setup ----------
root = tk.Tk()
root.title("Student Management System")
root.geometry("420x400")
root.configure(bg="white")

title_label = tk.Label(root, text="STUDENT MANAGEMENT SYSTEM", font=("Arial", 16, "bold"), bg="white")
title_label.pack(pady=10)

# Entry fields
name_label = tk.Label(root, text="Name:", font=("Arial", 12), bg="white")
name_label.pack()
name_entry = tk.Entry(root, font=("Arial", 12), width=30)
name_entry.pack()

tk.Label(root, text="Roll Number:", font=("Arial", 12), bg="white").pack()
roll_entry = tk.Entry(root, font=("Arial", 12), width=30)
roll_entry.pack()

marks_label = tk.Label(root, text="Marks:", font=("Arial", 12), bg="white")
marks_label.pack()
marks_entry = tk.Entry(root, font=("Arial", 12), width=30)
marks_entry.pack()

# Buttons
btn_frame = tk.Frame(root, bg="white")
btn_frame.pack(pady=15)

add_btn = tk.Button(btn_frame, text="Add Student", font=("Arial", 12, "bold"), bg="lightblue", command=add_student, width=15)
add_btn.grid(row=0, column=0, padx=5, pady=5)

search_btn = tk.Button(btn_frame, text="Search Student", font=("Arial", 12, "bold"), bg="lightgreen", command=toggle_search_mode, width=15)
search_btn.grid(row=0, column=1, padx=5, pady=5)

tk.Button(btn_frame, text="Display All", font=("Arial", 12, "bold"), bg="orange", command=display_all_students, width=15).grid(row=1, column=0, padx=5, pady=5)
tk.Button(btn_frame, text="Find Topper", font=("Arial", 12, "bold"), bg="pink", command=find_topper, width=15).grid(row=1, column=1, padx=5, pady=5)

tk.Button(root, text="Exit", font=("Arial", 12, "bold"), bg="red", fg="white", command=root.destroy, width=20).pack(pady=10)

root.mainloop()
