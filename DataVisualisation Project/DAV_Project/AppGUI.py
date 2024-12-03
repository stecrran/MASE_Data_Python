import tkinter as tk
from tkinter import font
from PIL import ImageTk, Image


class AppGUI(tk.Frame):
    def __init__(self, master=None, actor_search_app=None, genre_search_app=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.actor_search_app = actor_search_app
        self.genre_search_app = genre_search_app

        self.master.title("Movie Data Application")
        self.font_1 = font.Font(family="Calibri", size=16, weight="normal")
        self.font_2 = font.Font(family="Calibri", size=12, weight="normal")

        # Load and display the image
        img_path = 'movie.png'
        image = Image.open(img_path)
        self.image = ImageTk.PhotoImage(image)
        self.image_label = tk.Label(master, image=self.image)
        self.image_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Title label
        self.label_title = tk.Label(
            master, text="Choose an Option", font=self.font_1
        )
        self.label_title.grid(row=1, column=0, columnspan=2, sticky=tk.N + tk.S + tk.E + tk.W)

        # Buttons for different applications
        self.actor_button = tk.Button(
            master,
            text="Actor Search",
            command=self.launch_actor_search,
            font=self.font_2,
        )
        self.actor_button.grid(row=2, column=0, sticky=tk.N + tk.S + tk.E + tk.W)

        self.genre_button = tk.Button(
            master,
            text="Genre Search",
            command=self.launch_genre_search,
            font=self.font_2,
        )
        self.genre_button.grid(row=2, column=1, sticky=tk.N + tk.S + tk.E + tk.W)

        # Close application button
        self.close_button = tk.Button(
            master, text="Close", command=self.close_application, font=self.font_2
        )
        self.close_button.grid(row=3, column=0, columnspan=2, sticky=tk.N + tk.S + tk.E + tk.W)

    def launch_actor_search(self):
        """
        Launch the ActorSearch application.
        """
        if self.actor_search_app:
            self.actor_search_app.run()
        else:
            tk.messagebox.showerror("Error", "Actor Search app not initialized.")

    def launch_genre_search(self):
        """
        Launch the GenreSearch application.
        """
        if self.genre_search_app:
            self.genre_search_app.run(parent=self.master)  # Pass the root as parent
        else:
            tk.messagebox.showerror("Error", "Genre Search app not initialized.")

    def close_application(self):
        """
        Close the application.
        """
        self.master.destroy()
