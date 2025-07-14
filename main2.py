import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- GUI Setup ---
root = tk.Tk()
root.title("📈 Stock Price Analyzer - Light Theme")
root.geometry("960x680")
root.configure(bg="#f7f7f7")

# State Variables
current_df = None
show_sma = tk.BooleanVar(value=False)

# --- Functions ---
def fetch_data():
    symbol = symbol_entry.get().upper().strip()
    days = duration_var.get()

    if not symbol:
        messagebox.showwarning("Input Error", "Please enter a stock symbol.")
        return

    end = datetime.today()
    start = end - timedelta(days=int(days))

    try:
        df = yf.download(symbol, start=start, end=end)
        if df is None or df.empty:
            raise ValueError("No data found for this symbol")

        df.reset_index(inplace=True)
        df['SMA_10'] = df['Close'].rolling(window=10).mean()
        save_df(df)
        display_table(df)
        plot_graph(df)
        export_btn.config(state=tk.NORMAL)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch data: {e}")

def display_table(df):
    for row in tree.get_children():
        tree.delete(row)
    for _, row in df.iterrows():
        tree.insert("", "end", values=(
            row['Date'].strftime('%Y-%m-%d'),
            f"{row['Open']:.2f}",
            f"{row['Close']:.2f}",
            f"{row['High']:.2f}",
            f"{row['Low']:.2f}"
        ))

def plot_graph(df):
    ax.clear()
    ax.plot(df['Date'], df['Close'], color='blue', label='Close Price')
    ax.plot(df['Date'], df['Open'], color='green', label='Open Price')
    
    if show_sma.get():
        ax.plot(df['Date'], df['SMA_10'], color='orange', linestyle='--', label='SMA-10')

    ax.set_title("Stock Price Trend", color='black')
    ax.set_ylabel("Price (USD)", color='black')
    ax.tick_params(colors='black')
    ax.set_facecolor('#ffffff')
    fig.patch.set_facecolor('#f7f7f7')
    ax.legend()
    fig.autofmt_xdate()
    canvas.draw()

def export_csv():
    if current_df is not None:
        preview = current_df[['Date', 'Open', 'Close']].tail(3).to_string(index=False)
        confirmed = messagebox.askyesno("Preview Last Entries", f"Export the following data?\n\n{preview}")
        if confirmed:
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV File", "*.csv")])
            if file_path:
                current_df.to_csv(file_path, index=False)
                messagebox.showinfo("Success", "Data exported successfully!")

def save_df(df):
    global current_df
    current_df = df

def toggle_sma():
    if current_df is not None:
        plot_graph(current_df)

def suggest_ticker():
    sample = {
        "apple": "AAPL",
        "tesla": "TSLA",
        "microsoft": "MSFT",
        "google": "GOOGL"
    }
    query = symbol_entry.get().strip().lower()
    match = sample.get(query)
    if match:
        symbol_entry.delete(0, tk.END)
        symbol_entry.insert(0, match)

# --- Theming ---
style = ttk.Style()
style.theme_use("clam")
style.configure(".", background="#f7f7f7", foreground="black", fieldbackground="white", font=("Segoe UI", 11))
style.configure("Treeview", background="white", foreground="black", fieldbackground="white")
style.configure("Treeview.Heading", background="#e0e0e0", foreground="black")

# --- Title ---
tk.Label(root, text="Stock Price Analyzer", font=("Arial", 20, "bold"), fg="black", bg="#f7f7f7").pack(pady=10)

# --- Input Frame ---
input_frame = tk.Frame(root, bg="#f7f7f7")
input_frame.pack(pady=5)

tk.Label(input_frame, text="Stock Symbol:", bg="#f7f7f7", fg="black").grid(row=0, column=0, padx=5)
symbol_entry = tk.Entry(input_frame, width=12, font=("Arial", 11), bg="white", fg="black", insertbackground="black")
symbol_entry.grid(row=0, column=1, padx=5)

suggest_btn = tk.Button(input_frame, text="Suggest", command=suggest_ticker, bg="#dddddd", fg="black")
suggest_btn.grid(row=0, column=2, padx=5)

tk.Label(input_frame, text="Duration (days):", bg="#f7f7f7", fg="black").grid(row=0, column=3, padx=5)
duration_var = tk.StringVar(value="30")
duration_dropdown = ttk.Combobox(input_frame, textvariable=duration_var, values=["7", "30", "90"], width=5, state="readonly")
duration_dropdown.grid(row=0, column=4, padx=5)

fetch_btn = tk.Button(input_frame, text="Fetch Data", command=fetch_data, bg="#2980b9", fg="white")
fetch_btn.grid(row=0, column=5, padx=10)

sma_toggle = tk.Checkbutton(input_frame, text="Show SMA-10", variable=show_sma, command=toggle_sma, bg="#f7f7f7", fg="black", selectcolor="#f7f7f7", activebackground="#f7f7f7")
sma_toggle.grid(row=0, column=6, padx=5)

# --- Table ---
columns = ("Date", "Open", "Close", "High", "Low")
tree = ttk.Treeview(root, columns=columns, show="headings", height=8)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)
tree.pack(pady=10)

# --- Graph ---
fig, ax = plt.subplots(figsize=(8, 3))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(pady=10)

# --- Export ---
export_btn = tk.Button(root, text="Export to CSV", font=("Arial", 12), command=export_csv, state=tk.DISABLED, bg="#27ae60", fg="white")
export_btn.pack(pady=5)

# --- Start ---
root.mainloop()
