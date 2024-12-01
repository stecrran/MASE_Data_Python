import tkinter as tk
from tkinter import ttk
import pandas as pd


class CustomerSearchApp:
    def __init__(self, root, csv_file):
        self.root = root
        self.root.title("Customer Search")

        # Load data from CSV file
        self.data = pd.read_csv(csv_file)

        # Entry widget for wildcard search
        self.search_label = tk.Label(root, text="Search Name:")
        self.search_label.pack(pady=5)

        self.search_entry = tk.Entry(root)
        self.search_entry.pack(pady=5)

        # Search button
        self.search_button = tk.Button(root, text="Search", command=self.search_customer)
        self.search_button.pack(pady=5)

        # Table to display results
        self.tree = ttk.Treeview(root, columns=("CustomerID", "Name"), show="headings")
        self.tree.heading("CustomerID", text="CustomerID")
        self.tree.heading("Name", text="Name")
        self.tree.pack(fill=tk.BOTH, expand=True)

    def search_customer(self):
        # Get search text and filter data
        search_text = self.search_entry.get()
        if search_text:
            # Filter data based on wildcard search
            filtered_data = self.data[self.data["Name"].str.contains(search_text, case=False, na=False)]

            # Clear existing table data
            for row in self.tree.get_children():
                self.tree.delete(row)

            # Insert filtered data into table
            for _, row in filtered_data.iterrows():
                self.tree.insert("", tk.END, values=(row["CustomerID"], row["Name"]))


if __name__ == "__main__":
    root = tk.Tk()
    app = CustomerSearchApp(root, "customers.csv")
    root.mainloop()
