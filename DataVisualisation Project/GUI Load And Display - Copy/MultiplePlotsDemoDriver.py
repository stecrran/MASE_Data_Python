import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class MultiDataPlotterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-Data Plotter (2x2 Layout)")

        # Frame for the canvas
        self.plot_frame = tk.Frame(root)
        self.plot_frame.pack(fill=tk.BOTH, expand=True)

        # Canvas to hold the plots
        self.canvas = tk.Canvas(self.plot_frame)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Button to load and plot data
        self.plot_button = tk.Button(root, text="Load and Plot Data", command=self.load_and_plot_data)
        self.plot_button.pack(pady=10)

        # Placeholder for FigureCanvasTkAgg object
        self.fig_canvas = None

    def load_and_plot_data(self):
        # Clear previous plot from canvas if any
        if self.fig_canvas:
            self.fig_canvas.get_tk_widget().pack_forget()
            self.fig_canvas = None

        # Create sample dataframes
        df1 = pd.DataFrame({"X": range(1, 6), "Y": [2, 3, 5, 7, 11]})
        df2 = pd.DataFrame({"X": range(1, 6), "Y": [1, 4, 9, 16, 25]})
        df3 = pd.DataFrame({"X": range(1, 6), "Y": [10, 8, 6, 4, 2]})
        df4 = pd.DataFrame({"X": range(1, 6), "Y": [3, 6, 9, 12, 15]})

        # List of dataframes and titles
        dataframes = [df1, df2, df3, df4]
        titles = ["Prime Numbers", "Square Numbers", "Decreasing Pattern", "Multiples of 3"]

        # Create a 2x2 subplot figure
        fig, axs = plt.subplots(2, 2, figsize=(8, 8))

        # Plot each dataframe in a subplot
        for i, (df, title) in enumerate(zip(dataframes, titles)):
            ax = axs[i // 2, i % 2]  # 2x2 grid
            ax.plot(df["X"], df["Y"], marker='o')
            ax.set_title(title)
            ax.set_xlabel("X")
            ax.set_ylabel("Y")

        # Embed the plot into Tkinter canvas
        self.fig_canvas = FigureCanvasTkAgg(fig, master=self.canvas)
        self.fig_canvas.draw()
        self.fig_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    app = MultiDataPlotterApp(root)
    root.mainloop()
