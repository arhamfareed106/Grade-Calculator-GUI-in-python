import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# --- Grade Calculator Logic ---
def calculate():
    try:
        subjects = ["Math", "Physics", "Chemistry", "English", "Computer"]
        marks = []

        for subj in subjects:
            val = entries[subj].get()
            if val.strip() == "":
                raise ValueError("Empty field")
            marks.append(float(val))

        total = sum(marks)
        percentage = total / len(subjects)
        grade = get_grade(percentage)

        result_text = f"📊 Total: {total}     |     Percentage: {percentage:.2f}%     |     Grade: {grade}"
        result_label.config(text=result_text, foreground="#333")
        plot_graph(subjects, marks)

        # Save result for export
        result_data['subjects'] = subjects
        result_data['marks'] = marks
        result_data['total'] = total
        result_data['percentage'] = percentage
        result_data['grade'] = grade

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numeric marks in all fields.")

def get_grade(percentage):
    if percentage >= 90:
        return 'A+'
    elif percentage >= 80:
        return 'A'
    elif percentage >= 70:
        return 'B'
    elif percentage >= 60:
        return 'C'
    elif percentage >= 50:
        return 'D'
    else:
        return 'F'

# --- Graph Plotting ---
def plot_graph(subjects, marks):
    ax.clear()
    bars = ax.bar(subjects, marks, color=graph_color)
    for bar, mark in zip(bars, marks):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1, f'{mark:.1f}', ha='center', fontsize=9)
    ax.set_title("Subject-wise Marks", fontsize=12)
    ax.set_ylabel("Marks")
    ax.set_ylim(0, 100)
    canvas.draw()

# --- Export Function ---
def export_result():
    if not result_data:
        messagebox.showwarning("No Data", "Please calculate results before exporting.")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "w") as f:
            f.write("Student Grade Report\n\n")
            for subj, mark in zip(result_data['subjects'], result_data['marks']):
                f.write(f"{subj}: {mark}\n")
            f.write(f"\nTotal: {result_data['total']}\n")
            f.write(f"Percentage: {result_data['percentage']:.2f}%\n")
            f.write(f"Grade: {result_data['grade']}\n")
        messagebox.showinfo("Exported", "Result successfully exported!")

# --- Clear Inputs ---
def clear_fields():
    for entry in entries.values():
        entry.delete(0, tk.END)
    result_label.config(text="")
    ax.clear()
    canvas.draw()

# --- Theme Toggle ---
def toggle_theme():
    global graph_color
    current = theme.get()
    if current == "light":
        root.config(bg="#2b2b2b")
        form_frame.config(bg="#2b2b2b")
        result_label.config(background="#2b2b2b", foreground="#f5f5f5")
        title_label.config(background="#2b2b2b", foreground="#00ffff")
        style.configure('TLabel', background="#2b2b2b", foreground="#f5f5f5")
        style.configure('TEntry', fieldbackground="#3c3c3c", foreground="white")
        graph_color = "#00ffcc"
        theme.set("dark")
    else:
        root.config(bg="#eaf6f6")
        form_frame.config(bg="#eaf6f6")
        result_label.config(background="#eaf6f6", foreground="#333")
        title_label.config(background="#eaf6f6", foreground="#0e4d92")
        style.configure('TLabel', background="#eaf6f6", foreground="black")
        style.configure('TEntry', fieldbackground="white", foreground="black")
        graph_color = "#4CAF50"
        theme.set("light")

# --- Live Validation ---
def validate_numeric_input(P):
    return P == "" or P.replace(".", "", 1).isdigit()

# --- GUI Layout ---
root = tk.Tk()
root.title("📚 Student Grade Calculator")
root.geometry("850x650")
theme = tk.StringVar(value="light")
graph_color = "#4CAF50"
result_data = {}

# Theme Styling
style = ttk.Style()
style.theme_use('clam')
style.configure('TButton', font=('Arial', 12), padding=6)
style.configure('TEntry', font=('Arial', 12))
style.configure('TLabel', font=('Arial', 12))

# Title
title_label = tk.Label(root, text="📘 Student Grade Calculator", font=("Arial", 20, "bold"), bg="#eaf6f6", fg="#0e4d92")
title_label.pack(pady=20)

# Entry Form
form_frame = tk.Frame(root, bg="#eaf6f6")
form_frame.pack()

vcmd = (root.register(validate_numeric_input), "%P")

subjects = ["Math", "Physics", "Chemistry", "English", "Computer"]
entries = {}

for i, subject in enumerate(subjects):
    ttk.Label(form_frame, text=f"{subject} Marks:").grid(row=i, column=0, pady=8, padx=5, sticky='e')
    entry = ttk.Entry(form_frame, width=10, validate="key", validatecommand=vcmd)
    entry.grid(row=i, column=1, pady=8, padx=10)
    entries[subject] = entry

# Buttons
btn_frame = tk.Frame(root, bg="#eaf6f6")
btn_frame.pack(pady=15)

ttk.Button(btn_frame, text="🎯 Calculate Result", command=calculate).grid(row=0, column=0, padx=10)
ttk.Button(btn_frame, text="📤 Export Report", command=export_result).grid(row=0, column=1, padx=10)
ttk.Button(btn_frame, text="🔄 Clear", command=clear_fields).grid(row=0, column=2, padx=10)
ttk.Button(btn_frame, text="🌓 Toggle Theme", command=toggle_theme).grid(row=0, column=3, padx=10)

# Result Label
result_label = ttk.Label(root, text="", font=("Arial", 12), background="#eaf6f6")
result_label.pack(pady=10)

# Graph Area
fig, ax = plt.subplots(figsize=(6.5, 4))
fig.tight_layout()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(pady=20)

root.mainloop()
