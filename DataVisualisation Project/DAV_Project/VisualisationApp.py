import tkinter as tk


class VisualisationApp(tk.Toplevel):
    def __init__(self, master=None, visualise_data_app=None, data=None):
        super().__init__(master)
        self.visualise_data_app = visualise_data_app
        self.data = data  # Pass the data needed for visualizations

        self.title("Visualization Options")
        self.geometry("400x400")

        # Buttons for each visualization function
        tk.Button(self, text="Plot % Profit/Loss by Year", command=self.plotPercentProfitLossByYear).pack(pady=10)
        tk.Button(self, text="Plot % Profit/Loss (Zoomed)", command=self.plotPercentProfitLossZoomed).pack(pady=10)
        tk.Button(self, text="Plot % Profit/Loss +/- 100%", command=self.plotPercentProfitLossPlusMinus100).pack(pady=10)

        # Close Button
        tk.Button(self, text="Close", command=self.closeWindow).pack(pady=10)


    # Plot % Profit/Loss by Year
    def plotPercentProfitLossByYear(self):
        if self.data is not None:
            self.visualise_data_app.plotPercentProfitOrLossByYear(self.data)
        else:
            print("Error: No data provided.")


    # Plot % Profit/Loss (Zoomed) by Year
    def plotPercentProfitLossZoomed(self):
        if self.data is not None:
            self.visualise_data_app.plotPercentProfitOrLossByYearZoom(self.data)
        else:
            print("Error: No data provided.")


    # Plot % Profit/Loss +/- 100% by Year
    def plotPercentProfitLossPlusMinus100(self):
        if self.data is not None:
            self.visualise_data_app.plotPercentProfitOrLossByYearPlusMinus100pct(self.data)
        else:
            print("Error: No data provided.")


    # Close visualisation menu
    def closeWindow(self):
        self.destroy()
