import tkinter as tk
from tkinter import ttk
from sqlalchemy.sql import text
import re
import matplotlib.pyplot as plt

# Initialize the ActorSearch class with a database connection.
class ActorSearch:
    def __init__(self, db_connection):
        self.db_connection = db_connection
        self.character_window = None
        self.movies_and_characters = []


    # Launch the Actor Search application
    def run(self):
        root = tk.Tk()
        root.title("Search Movies by Actor")

        # Set window size to 800x400
        root.geometry("800x400")

        # Create a frame for the search area and results
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Entry widget for wildcard search and Clear button
        tk.Label(self.main_frame, text="Search Actor Name:").grid(row=0, column=0, sticky=tk.W)
        self.search_entry = tk.Entry(self.main_frame)
        self.search_entry.grid(row=0, column=1, padx=5)
        self.search_entry.bind("<KeyRelease>", self.searchActor)

        # Clear button
        clear_button = tk.Button(self.main_frame, text="Clear", command=self.clearSearch)
        clear_button.grid(row=0, column=2, padx=5, sticky=tk.W)

        # Top 10 Actors button
        top_actors_button = tk.Button(self.main_frame, text="Top 10 Actors", command=self.plotTop10Actors)
        top_actors_button.grid(row=0, column=2, padx=5, sticky=tk.E)

        # Table to display results with both horizontal and vertical scrollbars
        table_frame = tk.Frame(self.main_frame)
        table_frame.grid(row=1, column=0, columnspan=2, pady=5, sticky="nsew")
        self.tree = ttk.Treeview(table_frame, columns=("ActorID", "Name"), show="headings", height=10)
        self.tree.heading("ActorID", text="ActorID")
        self.tree.heading("Name", text="Name")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Vertical scrollbar for the table
        v_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=v_scrollbar.set)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind row selection event
        self.tree.bind("<<TreeviewSelect>>", self.selectByRow)

        # Frame for movie titles and characters (to the right of the table)
        self.info_frame = tk.Frame(self.main_frame)
        self.info_frame.grid(row=1, column=2, padx=10, sticky="n")

        # Movie titles list
        tk.Label(self.info_frame, text="Movies:").grid(row=0, column=0, sticky=tk.W)
        self.movies_listbox = tk.Listbox(self.info_frame, width=50, height=20)
        self.movies_listbox.grid(row=1, column=0, sticky=tk.W)
        self.movies_listbox.bind("<<ListboxSelect>>", self.selectByMovie)

        # Display all actors initially
        self.displayActors(self.fetchAllActors())

        # Run the main loop
        root.mainloop()


    # Fetch actors table data from imdb_full database
    def fetchAllActors(self):
        query = text("SELECT actorid, name FROM actors")
        with self.db_connection.connect() as conn:
            return conn.execute(query).fetchall()


    # Fetch character names for each actors role per movie
    def fetchMovieCharacterForActor(self, actorid):

        # Use direct SQL query as there was an issue returning character names due to text used
        query = text("""
        SELECT mov.title, mov_actor.as_character
        FROM movies mov
        INNER JOIN movies2actors mov_actor ON mov.movieid = mov_actor.movieid
        WHERE mov_actor.actorid = :actorid
        """)
        with self.db_connection.connect() as conn:
            results = conn.execute(query, {"actorid": actorid}).fetchall()

        parsed_results = []
        for title, as_character in results:
            if as_character:
                character_match = re.search(r'\[([^\]]+)\]', as_character)
                character = character_match.group(1) if character_match else "Unknown Character"
            else:
                character = "Unknown Character"
            parsed_results.append((title, character))

        return parsed_results


    #  Fetch the top 10 actors based on the number of films they appeared in
    def fetchTop10Actors(self):

        query = text("""
        SELECT a.name, COUNT(ma.movieid) AS film_count
        FROM actors a
        INNER JOIN movies2actors ma ON a.actorid = ma.actorid
        GROUP BY a.name
        ORDER BY film_count DESC
        LIMIT 10
        """)
        with self.db_connection.connect() as conn:
            return conn.execute(query).fetchall()


    # Display a bar chart of the top 10 actors based on the number of films they appeared in
    def plotTop10Actors(self):
        try:
            top_actors = self.fetchTop10Actors()
            if not top_actors:
                tk.messagebox.showinfo("Info", "No data available for top actors.")
                return

            names = [actor[0] for actor in top_actors]
            counts = [actor[1] for actor in top_actors]

            plt.figure(figsize=(10, 6))
            plt.barh(names, counts, color="skyblue")
            plt.xlabel("Number of Films")
            plt.ylabel("Actor Name")
            plt.title("Top 10 Actors by Number of Films")
            plt.gca().invert_yaxis()  # Invert y-axis to show the top actor at the top
            plt.tight_layout()
            plt.show()
        except Exception as e:
            tk.messagebox.showerror("Error", f"An error occurred while generating the plot: {e}")


    # Display actors in the treeview table
    def displayActors(self, actors):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for actorid, name in actors:
            self.tree.insert("", tk.END, values=(actorid, name))


    # Search for actors by name
    def searchActor(self, event=None):
        search_text = self.search_entry.get()
        query = text("SELECT actorid, name FROM actors WHERE name LIKE :search_text")
        with self.db_connection.connect() as conn:
            actors = conn.execute(query, {"search_text": f"%{search_text}%"}).fetchall()
        self.displayActors(actors)


    # Clear the search field and reset the actor list
    def clearSearch(self):
        self.search_entry.delete(0, tk.END)
        self.displayActors(self.fetchAllActors())


    # Handle actor selection and display their movies and characters
    def selectByRow(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            actorid = self.tree.item(selected_item[0])["values"][0]
            self.movies_and_characters = self.fetchMovieCharacterForActor(actorid)

            self.movies_listbox.delete(0, tk.END)
            for movie, character in self.movies_and_characters:
                self.movies_listbox.insert(tk.END, movie)


    # Display the selected movie and character in a separate window
    def selectByMovie(self, event):
        selected_index = self.movies_listbox.curselection()
        if selected_index:
            movie, character = self.movies_and_characters[selected_index[0]]

            if self.character_window is None or not self.character_window.winfo_exists():
                self.character_window = tk.Toplevel()
                self.character_window.title("Character Details")
                self.character_window.geometry("400x200")

            for widget in self.character_window.winfo_children():
                widget.destroy()
            tk.Label(self.character_window, text=f"Movie: {movie}").pack(pady=10)
            tk.Label(self.character_window, text=f"Character: {character}").pack(pady=10)
