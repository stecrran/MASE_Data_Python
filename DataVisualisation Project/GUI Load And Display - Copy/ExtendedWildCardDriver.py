import tkinter as tk
from tkinter import ttk, Label
import pandas as pd
from PIL import Image, ImageTk
import os

class CustomerSearchApp:
    def __init__(self, root, csv_file):
        self.root = root
        self.root.title("Customer Search")

        # Set window size to 600x600
        self.root.geometry("1000x800")

        # Load data from CSV file
        self.data = pd.read_csv(csv_file)

        # Create a frame for the search area and results
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Entry widget for wildcard search
        tk.Label(self.main_frame, text="Search Name:").grid(row=0, column=0, sticky=tk.W)
        self.search_entry = tk.Entry(self.main_frame)
        self.search_entry.grid(row=0, column=1, padx=5)
        self.search_entry.bind("<KeyRelease>", self.search_customer)  # Auto-update on typing

        # Table to display results with both horizontal and vertical scrollbars
        table_frame = tk.Frame(self.main_frame)
        table_frame.grid(row=1, column=0, columnspan=2, pady=5, sticky="nsew")
        self.tree = ttk.Treeview(table_frame, columns=("CustomerID", "Name"), show="headings", height=10)
        self.tree.heading("CustomerID", text="CustomerID")
        self.tree.heading("Name", text="Name")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Vertical scrollbar for the table
        v_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=v_scrollbar.set)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind row selection event
        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)

        # Frame for additional information (to the right of the table)
        self.info_frame = tk.Frame(self.main_frame)
        self.info_frame.grid(row=1, column=2, padx=10, sticky="n")

        # Additional information fields
        tk.Label(self.info_frame, text="Email:").grid(row=0, column=0, sticky=tk.W)
        self.email_entry = tk.Entry(self.info_frame, width=25)
        self.email_entry.grid(row=0, column=1, padx=5)

        tk.Label(self.info_frame, text="Phone:").grid(row=1, column=0, sticky=tk.W)
        self.phone_entry = tk.Entry(self.info_frame, width=25)
        self.phone_entry.grid(row=1, column=1, padx=5)

        tk.Label(self.info_frame, text="Address:").grid(row=2, column=0, sticky=tk.W)
        self.address_entry = tk.Entry(self.info_frame, width=25)
        self.address_entry.grid(row=2, column=1, padx=5)

        # Image label for customer photo positioned to the right of entry fields
        self.image_label = Label(self.info_frame, text="No Image", width=150, height=150)
        self.image_label.grid(row=0, column=2, rowspan=3, padx=10, pady=5)

        # Display all customers initially
        self.display_customers(self.data)

    def display_customers(self, data):
        # Clear existing table data
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Insert data into the table
        for _, row in data.iterrows():
            self.tree.insert("", tk.END, values=(row["CustomerID"], row["Name"]))

    def search_customer(self, event=None):
        # Get search text and filter data
        search_text = self.search_entry.get()
        if search_text:
            filtered_data = self.data[self.data["Name"].str.contains(search_text, case=False, na=False)]
        else:
            filtered_data = self.data  # Show all if search is empty

        # Display filtered data in the table
        self.display_customers(filtered_data)

    def on_row_select(self, event):
        # Get selected row data
        selected_item = self.tree.selection()
        if selected_item:
            customer_id = self.tree.item(selected_item[0])["values"][0]

            # Fetch customer details
            customer_data = self.data[self.data["CustomerID"] == customer_id].iloc[0]

            # Populate entry fields with additional information
            self.email_entry.delete(0, tk.END)
            self.email_entry.insert(0, customer_data["Email"])

            self.phone_entry.delete(0, tk.END)
            self.phone_entry.insert(0, customer_data["Phone"])

            self.address_entry.delete(0, tk.END)
            self.address_entry.insert(0, customer_data["Address"])

            # Load and display image if available
            image_path = "images/" + customer_data["Image"]
            print(image_path)
            if os.path.exists(image_path):
                try:
                    image = Image.open(image_path)
                    image = image.resize((150, 150))
                    photo = ImageTk.PhotoImage(image)
                    self.image_label.config(image=photo, text="")  # Clear the "No Image" text
                    self.image_label.image = photo  # Keep a reference to avoid garbage collection
                except Exception as e:
                    self.image_label.config(text="Error loading image")
                    self.image_label.image = None
                    print(f"Error loading image {image_path}: {e}")
            else:
                self.image_label.config(text="Image not found")
                self.image_label.image = None


if __name__ == "__main__":
    root = tk.Tk()
    app = CustomerSearchApp(root, "customers_extended.csv")
    root.mainloop()
