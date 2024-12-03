import tkinter as tk
from tkinter import ttk
from sqlalchemy.sql import text
import re


class ActorSearch:
    # Initialize the ActorSearch class with a database connection.
    def __init__(self, db_connection):
        self.db_connection = db_connection
        self.character_window = None

    # Launch the Actor Search application.
    def run(self):
        root = tk.Tk()
        root.title("Search movie by Actor")

        # Set window size to 800x400
        root.geometry("800x400")

        # Create a frame for the search area and results
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Entry widget for wildcard search and Clear button
        tk.Label(self.main_frame, text="Search Actor Name:").grid(row=0, column=0, sticky=tk.W)
        self.search_entry = tk.Entry(self.main_frame)
        self.search_entry.grid(row=0, column=1, padx=5)
        self.search_entry.bind("<KeyRelease>", self.search_actor)  # Auto-update on typing

        # Clear button
        clear_button = tk.Button(self.main_frame, text="Clear", command=self.clear_search)
        clear_button.grid(row=0, column=2, padx=5)

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
        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)

        # Frame for movie titles and characters (to the right of the table)
        self.info_frame = tk.Frame(self.main_frame)
        self.info_frame.grid(row=1, column=2, padx=10, sticky="n")

        # Movie titles list
        tk.Label(self.info_frame, text="Movies:").grid(row=0, column=0, sticky=tk.W)
        self.movies_listbox = tk.Listbox(self.info_frame, width=50, height=20)
        self.movies_listbox.grid(row=1, column=0, sticky=tk.W)
        self.movies_listbox.bind("<<ListboxSelect>>", self.on_movie_select)

        # Display all actors initially
        self.display_actors(self.fetch_all_actors())

        # Run the main loop
        root.mainloop()

    # Fetch all actors from the database.
    def fetch_all_actors(self):
        query = text("SELECT actorid, name FROM actors")
        with self.db_connection.connect() as conn:
            return conn.execute(query).fetchall()

    # Fetch all movies and characters associated with a specific actor ID.
    def fetch_movies_and_characters_for_actor(self, actorid):
        # use SQL query for required joins
        query = text("""
        SELECT mov.title, mov_actor.as_character
        FROM movies mov
        INNER JOIN movies2actors mov_actor ON mov.movieid = mov_actor.movieid
        WHERE mov_actor.actorid = :actorid
        """)
        with self.db_connection.connect() as conn:
            results = conn.execute(query, {"actorid": actorid}).fetchall()

        # Extract character name from square brackets
        parsed_results = []
        for title, as_character in results:
            if as_character:
                character_match = re.search(r'\[([^\]]+)\]', as_character)
                character = character_match.group(1) if character_match else "Unknown Character"
            else:
                character = "Unknown Character"
            parsed_results.append((title, character))

        return parsed_results

    # Display actors
    def display_actors(self, actors):
        # Clear existing table data
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Insert data into the table
        for actorid, name in actors:
            self.tree.insert("", tk.END, values=(actorid, name))

    # Search for actors by name.
    def search_actor(self, event=None):
        search_text = self.search_entry.get()
        query = text("SELECT actorid, name FROM actors WHERE name LIKE :search_text")
        with self.db_connection.connect() as conn:
            actors = conn.execute(query, {"search_text": f"%{search_text}%"}).fetchall()
        self.display_actors(actors)

    # Clear the search field and reset the actor list.
    def clear_search(self):
        """
        Tkinter.Entry.delete [https://tedboy.github.io/python_stdlib/generated/generated/Tkinter.Entry.delete.html]
        [https://python-course.eu/tkinter/entry-widgets-in-tkinter.php]
        """
        self.search_entry.delete(0, tk.END)
        self.display_actors(self.fetch_all_actors())

    # Manage actor selection and display corresponding movies and characters.
    def on_row_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            actorid = self.tree.item(selected_item[0])["values"][0]

            # Fetch movies and characters for the selected actor
            self.movies_and_characters = self.fetch_movies_and_characters_for_actor(actorid)

            # Display movies in the listbox
            self.movies_listbox.delete(0, tk.END)
            for movie, character in self.movies_and_characters:
                self.movies_listbox.insert(tk.END, movie)

    # Manage movie selection and display the character name in a separate window.
    def on_movie_select(self, event):
        selected_index = self.movies_listbox.curselection()
        if selected_index:
            movie, character = self.movies_and_characters[selected_index[0]]

            # Create or update the character window
            if self.character_window is None or not self.character_window.winfo_exists():
                self.character_window = tk.Toplevel()
                self.character_window.title("Character Details")
                self.character_window.geometry("400x200")

            # Update the character window with the selected character
            for widget in self.character_window.winfo_children():
                widget.destroy()
            tk.Label(self.character_window, text=f"Movie: {movie}").pack(pady=10)
            tk.Label(self.character_window, text=f"Character: {character}").pack(pady=10)
