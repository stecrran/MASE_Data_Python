import tkinter as tk
from tkinter import font, messagebox, simpledialog
from PIL import ImageTk, Image


class AppGUI(tk.Frame):
    def __init__(self, master=None, actor_search_app=None, genre_search_app=None, data_analysis_app=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.actor_search_app = actor_search_app
        self.genre_search_app = genre_search_app
        self.data_analysis_app = data_analysis_app

        self.master.title("Movie Data Application")

        # Define fonts before calling other UI methods
        self.font_1 = font.Font(family="Calibri", size=16, weight="normal")
        self.font_2 = font.Font(family="Calibri", size=12, weight="normal")

        # Define log file
        self.log_file = "log_output.txt"

        # Call initialize_ui to set up the UI
        self.initialize_ui()

        # Set up logging for DataAnalysis
        if data_analysis_app:
            self.data_analysis_app.log_function = self.writeToLog

    def initialize_ui(self):
        # Log window
        self.log = tk.Text(self.master, state="disabled", height=10, width=60)
        self.log.grid(row=4, column=0, columnspan=2, sticky=tk.W)
        self.scrollB = tk.Scrollbar(self.master, command=self.log.yview)
        self.scrollB.grid(row=4, column=2, sticky=tk.N + tk.S + tk.E + tk.W)
        self.log['yscrollcommand'] = self.scrollB.set

        # Image
        img_path = 'movie.png'
        try:
            image = Image.open(img_path)
            self.image = ImageTk.PhotoImage(image)
            self.image_label = tk.Label(self.master, image=self.image)
            self.image_label.grid(row=0, column=0, columnspan=2, pady=10)
        except Exception as e:
            self.writeToLog(f"Error loading image: {e}")

        # Title label
        self.label_title = tk.Label(
            self.master, text="Choose an Option", font=self.font_1
        )
        self.label_title.grid(row=1, column=0, columnspan=2, sticky=tk.N + tk.S + tk.E + tk.W)

        # Buttons
        self.actor_button = tk.Button(
            self.master,
            text="Actor Search",
            command=self.launch_actor_search,
            font=self.font_2,
        )
        self.actor_button.grid(row=2, column=0, sticky=tk.N + tk.S + tk.E + tk.W)

        self.genre_button = tk.Button(
            self.master,
            text="Genre Search",
            command=self.launch_genre_search,
            font=self.font_2,
        )
        self.genre_button.grid(row=2, column=1, sticky=tk.N + tk.S + tk.E + tk.W)

        self.analysis_button = tk.Button(
            self.master,
            text="Run Data Analysis",
            command=self.launch_data_analysis,
            font=self.font_2,
        )
        self.analysis_button.grid(row=3, column=0, columnspan=2, sticky=tk.N + tk.S + tk.E + tk.W)

        self.close_button = tk.Button(
            self.master, text="Close", command=self.close_application, font=self.font_2
        )
        self.close_button.grid(row=5, column=0, columnspan=2, sticky=tk.N + tk.S + tk.E + tk.W)

    def writeToLog(self, msg):
        """
        Writes a message to the log window.
        """
        try:
            if isinstance(msg, str):
                log_msg = msg
            else:
                log_msg = str(msg)

            with open(self.log_file, "a") as file:
                file.write(log_msg + "\n")

            self.log['state'] = 'normal'
            self.log.insert(tk.END, log_msg + "\n")
            self.log['state'] = 'disabled'
            self.log.see(tk.END)
        except Exception as e:
            print(f"Error writing to log: {e}")

    def launch_actor_search(self):
        if self.actor_search_app:
            self.actor_search_app.run()
        else:
            messagebox.showerror("Error", "Actor Search app not initialized.")

    def launch_genre_search(self):
        if self.genre_search_app:
            self.genre_search_app.run(parent=self.master)
        else:
            messagebox.showerror("Error", "Genre Search app not initialized.")

    def launch_data_analysis(self):
        if self.data_analysis_app:
            table_name = simpledialog.askstring(
                "Table Selection",
                "Enter the table name for analysis:",
                parent=self.master
            )
            if table_name:
                self.writeToLog(f"Selected table: {table_name}")
                self.data_analysis_app.selectTable(table_name)
                self.writeToLog("Data analysis completed.")
            else:
                self.writeToLog("No table name provided.")
        else:
            messagebox.showerror("Error", "Data Analysis app not initialized.")

    def close_application(self):
        self.master.destroy()
