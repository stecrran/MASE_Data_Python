import tkinter as tk
from tkinter import ttk
import pandas as pd


class GenreSearch:
    def __init__(self, data):
        """
        Initialize the GenreSearch class with a DataFrame.
        :param data: Preprocessed DataFrame containing 'Year' and 'genres'.
        """
        self.data = data

    def count_genre_by_year(self, genre_name):
        """
        Count the occurrences of a specific genre for each year.
        :param genre_name: Genre name to count.
        :return: DataFrame with years and counts.
        """
        # Split the 'genres' column into individual genres
        self.data['genres_split'] = self.data['genres'].str.split(',')

        # Explode the DataFrame so that each genre has its own row
        exploded_data = self.data.explode('genres_split')

        # Strip whitespace from genre names to ensure accuracy
        exploded_data['genres_split'] = exploded_data['genres_split'].str.strip()

        # Filter for the specific genre and count occurrences per year
        genre_counts = (
            exploded_data[exploded_data['genres_split'] == genre_name]
            .groupby('Year')
            .size()
            .reset_index(name='Count')
        )
        return genre_counts

    def run(self):
        """
        Launch the Genre Search application.
        """
        root = tk.Tk()
        root.title("Search Movies by Genre")

        # Set window size
        root.geometry("500x500")

        # Create a frame for the genre selection and results
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Dropdown for genre selection
        tk.Label(self.main_frame, text="Select Genre:").grid(row=0, column=0, sticky=tk.W)
        self.genre_var = tk.StringVar()

        # Extract unique, trimmed genres for dropdown
        genres = sorted(
            set(
                genre.strip()
                for sublist in self.data['genres'].dropna().str.split(',')
                for genre in sublist
            )
        )
        self.genre_dropdown = ttk.Combobox(self.main_frame, textvariable=self.genre_var, values=genres, state="readonly")
        self.genre_dropdown.grid(row=0, column=1, padx=5)

        # Button to show counts
        search_button = tk.Button(self.main_frame, text="Search", command=self.show_genre_counts)
        search_button.grid(row=0, column=2, padx=5)

        # Table to display results
        self.tree = ttk.Treeview(self.main_frame, columns=("Year", "Count"), show="headings", height=20)
        self.tree.heading("Year", text="Year")
        self.tree.heading("Count", text="Count")
        self.tree.grid(row=1, column=0, columnspan=3, pady=5, sticky="nsew")

        # Vertical scrollbar for the table
        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=1, column=3, sticky="ns")

        # Run the main loop
        root.mainloop()

    def show_genre_counts(self):
        """
        Display the count of the selected genre by year in the table.
        """
        selected_genre = self.genre_var.get()
        if not selected_genre:
            print("No genre selected.")
            return

        # Get the genre counts
        genre_counts = self.count_genre_by_year(selected_genre)

        # Clear existing table data
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Insert data into the table
        for _, row in genre_counts.iterrows():
            self.tree.insert("", tk.END, values=(row['Year'], row['Count']))
