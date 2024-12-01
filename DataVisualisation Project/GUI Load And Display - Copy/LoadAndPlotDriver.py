import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DataPlotterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Data Plotter")
        self.data = None

        # Create a frame for the plot
        self.plot_frame = tk.Frame(root)
        self.plot_frame.pack(fill=tk.BOTH, expand=True)

        # Create a canvas for matplotlib figure
        self.canvas = tk.Canvas(self.plot_frame)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Load and plot buttons
        self.load_button = tk.Button(root, text="Load CSV", command=self.load_data)
        self.load_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.plot_button = tk.Button(root, text="Plot Data", command=self.plot_data)
        self.plot_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.modify_button = tk.Button(root, text="Modify Data", command=self.modify_data)
        self.modify_button.pack(side=tk.LEFT, padx=10, pady=10)

    def load_data(self):
        # Open file dialog to select CSV file
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                self.data = pd.read_csv(file_path)
                messagebox.showinfo("Data Loaded", f"Data loaded successfully from {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load data: {e}")

    def plot_data(self):
        if self.data is None:
            messagebox.showwarning("No Data", "Please load a CSV file first.")
            return

        # Clear existing plot
        self.canvas.delete("all")

        # Create a matplotlib figure
        fig, ax = plt.subplots()
        self.data.plot(ax=ax)

        # Embed the plot into Tkinter canvas
        self.fig_canvas = FigureCanvasTkAgg(fig, master=self.canvas)
        self.fig_canvas.draw()
        self.fig_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def modify_data(self):
        if self.data is None:
            messagebox.showwarning("No Data", "Please load a CSV file first.")
            return

        # Example modification: add a new column or change existing data
        # This can be replaced with any modification logic as required
        self.data["Modified"] = self.data.iloc[:, 0] * 2  # Example: Multiply first column by 2
        messagebox.showinfo("Data Modified", "Data has been modified. Please plot to see changes.")

if __name__ == "__main__":
    root = tk.Tk()
    app = DataPlotterApp(root)
    root.mainloop()
