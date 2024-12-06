import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

"""
Initialize the GenreSearch class with a DataFrame.
data = Preprocessed DataFrame containing 'Year', 'genres', 'title', and 'Adjusted_Gross_Revenue'.
"""
class GenreSearch:
    def __init__(self, data):
        self.data = data.copy()  # Avoid mutating the original DataFrame


    # Launch the Genre Search application, configure layout
    def run(self, parent=None):
        if parent is None:
            messagebox.showerror("Error", "No parent window provided.")
            return

        # Create a Toplevel window
        self.window = tk.Toplevel(parent)
        self.window.title("Search Movies by Genre")
        self.window.geometry("700x500")  # set window size

        self.main_frame = tk.Frame(self.window)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        tk.Label(self.main_frame, text="Select Genre:").grid(row=0, column=0, sticky=tk.W)
        self.genre_var = tk.StringVar()

        # Split out genres
        genres = sorted(
            set(
                genre.strip()
                for sublist in self.data['genres'].dropna().str.split(',')
                for genre in sublist
            )
        )

        # Use dropdown selection
        self.genre_dropdown = ttk.Combobox(self.main_frame, textvariable=self.genre_var, values=genres,
                                           state="readonly")
        self.genre_dropdown.grid(row=0, column=1, padx=5)

        search_button = tk.Button(self.main_frame, text="Search Movies", command=self.displayMoviesPerGenre)
        search_button.grid(row=0, column=2, padx=5)

        plot_button = tk.Button(self.main_frame, text="Plot Genre Count", command=self.generateGenreCountPlot)
        plot_button.grid(row=0, column=3, padx=5)

        revenue_plot_button = tk.Button(
            self.main_frame, text="Plot Genre Revenue", command=self.generateGenreRevenuePlot
        )
        revenue_plot_button.grid(row=0, column=4, padx=5)

        self.tree = ttk.Treeview(
            self.main_frame, columns=("Year", "Title", "Adjusted Gross Revenue"), show="headings", height=20
        )
        self.tree.heading("Year", text="Year")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Adjusted Gross Revenue", text="Adjusted Gross Revenue ($)")
        self.tree.grid(row=1, column=0, columnspan=5, pady=5, sticky="nsew")

        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=1, column=5, sticky="ns")


    # Retrieve movies and years for a specific genre, up to year 2000
    def getMoviesByGenre(self, genre_name):
        exploded_data = self.data.copy()
        exploded_data['genres_split'] = exploded_data['genres'].str.split(',')

        # Explode the DataFrame so that each genre has its own row
        exploded_data = exploded_data.explode('genres_split')

        # Remove whitespace from genre names
        exploded_data['genres_split'] = exploded_data['genres_split'].str.strip()

        # Ensure 'Year' is numeric
        exploded_data['Year'] = pd.to_numeric(exploded_data['Year'], errors='coerce')

        # Drop rows with non-numeric Year
        exploded_data = exploded_data.dropna(subset=['Year'])

        # Convert 'Year' to integer
        exploded_data['Year'] = exploded_data['Year'].astype(int)

        # Filter for the specific genre and cutoff year
        genre_movies = exploded_data[
            (exploded_data['genres_split'] == genre_name) & (exploded_data['Year'] <= 2000)
        ][['Year', 'title', 'Adjusted_Gross_Revenue']]
        return genre_movies


    # Count the number of movies for a specific genre by year, up to year 2000
    def getCountPerGenre(self, genre_name):
        exploded_data = self.data.copy()
        exploded_data['genres_split'] = exploded_data['genres'].str.split(',')
        exploded_data = exploded_data.explode('genres_split')
        exploded_data['genres_split'] = exploded_data['genres_split'].str.strip()

        exploded_data['Year'] = pd.to_numeric(exploded_data['Year'], errors='coerce')
        exploded_data = exploded_data.dropna(subset=['Year'])
        exploded_data['Year'] = exploded_data['Year'].astype(int)

        genre_counts = (
            exploded_data[
                (exploded_data['genres_split'] == genre_name) & (exploded_data['Year'] <= 2000)
            ]
            .groupby('Year')
            .size()
        )
        return genre_counts


    # Display the list of movies for the selected genre in the table
    def displayMoviesPerGenre(self):
        selected_genre = self.genre_var.get().strip()
        if not selected_genre:
            messagebox.showerror("Error", "No genre selected. Please select a genre from the dropdown.")
            return

        genre_movies = self.getMoviesByGenre(selected_genre)
        if genre_movies.empty:
            messagebox.showinfo("Info", f"No movies found for the genre: {selected_genre}.")
            return

        # Round Adjusted_Gross_Revenue to 2 decimal places for display
        if 'Adjusted_Gross_Revenue' in genre_movies.columns:
            genre_movies['Adjusted_Gross_Revenue'] = genre_movies['Adjusted_Gross_Revenue'].round(2)

        for row in self.tree.get_children():
            self.tree.delete(row)

        for _, row in genre_movies.iterrows():
            self.tree.insert("", tk.END, values=(row['Year'], row['title'], row['Adjusted_Gross_Revenue']))


    # Generate a graph for the selected genre showing the number of movies by year
    def generateGenreCountPlot(self):
        selected_genre = self.genre_var.get().strip()

        # In case no genre is selected
        if not selected_genre:
            messagebox.showerror("Error", "No genre selected. Please select a genre from the dropdown.")
            return

        genre_counts = self.getCountPerGenre(selected_genre)
        if genre_counts.empty:
            messagebox.showinfo("Info", f"No data to plot for the genre: {selected_genre}.")
            return

        # Ensure Year is an integer
        genre_counts.index = genre_counts.index.astype(int)

        # Use three-year intervals
        min_year = genre_counts.index.min()
        max_year = genre_counts.index.max()
        ticks = np.arange(min_year, max_year + 1, 3)

        # Plot with three-year x-axis intervals
        plt.figure(figsize=(10, 6))
        plt.plot(genre_counts.index, genre_counts.values, marker='o', label=f'{selected_genre} Movies')
        plt.xlabel('Year')
        plt.ylabel('Number of Movies')
        plt.title(f'Number of {selected_genre} Movies by Year')

        # Set x-axis ticks for three-year intervals
        plt.xticks(ticks=ticks, rotation=45)

        plt.grid(True, linestyle='--', linewidth=0.5)
        plt.legend()
        plt.tight_layout()
        plt.show()


    # Generate a graph for the selected genre showing adjusted gross revenue by year
    def generateGenreRevenuePlot(self):
        selected_genre = self.genre_var.get().strip()
        if not selected_genre:
            messagebox.showerror("Error", "No genre selected. Please select a genre from the dropdown.")
            return

        genre_movies = self.getMoviesByGenre(selected_genre)
        if genre_movies.empty:
            messagebox.showinfo("Info", f"No data to plot for the genre: {selected_genre}.")
            return

        # Group by year and calculate the total Adjusted Gross Revenue for each year
        revenue_by_year = genre_movies.groupby('Year')['Adjusted_Gross_Revenue'].sum().reset_index()

        # Use three-year intervals
        min_year = revenue_by_year['Year'].min()
        max_year = revenue_by_year['Year'].max()
        ticks = np.arange(min_year, max_year + 1, 3)  # 3-year increment

        # Plot the bar chart
        plt.figure(figsize=(10, 6))
        plt.bar(
            revenue_by_year['Year'],
            revenue_by_year['Adjusted_Gross_Revenue'],
            color='orange',
            label=f'{selected_genre} Revenue',
        )

        # Format y-axis to avoid scientific notation
        ax = plt.gca()
        ax.yaxis.set_major_formatter(ScalarFormatter(useOffset=False))
        plt.ticklabel_format(style='plain', axis='y')

        # Add labels and title
        plt.xlabel('Year')
        plt.ylabel('Adjusted Gross Revenue ($)')
        plt.title(f'Adjusted Gross Revenue for {selected_genre} by Year')
        plt.xticks(ticks, rotation=45)
        plt.grid(True, linestyle='--', linewidth=0.5)
        plt.legend()
        plt.tight_layout()
        plt.show()



