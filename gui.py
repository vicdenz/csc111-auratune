import tkinter as tk
from tkinter import ttk, font, messagebox

# Theme Colors
BG_COLOR = "#6a0dad"
HOVER_BG = "#a87cdc"
NORMAL_BG = "white"

class GUIApp(tk.Tk):
    def __init__(self, available_genres, on_search_complete):
        super().__init__()
        self.available_genres = available_genres
        self.on_search_complete = on_search_complete

        self.user_inputs = {}
        self.categories = ["danceability", "energy", "instrumentalness", "valence", "loudness"]
        self.step_index = 0

        self.configure(bg=BG_COLOR)
        self.title("AuraTune")

        # Fonts
        self.title_font = font.Font(family="Georgia", size=48, weight="bold")
        self.option_font = font.Font(family="Helvetica", size=28)
        self.step_font = font.Font(family="Arial", size=24)

        self.container = tk.Frame(self, bg=BG_COLOR)
        self.container.pack(fill="both", expand=True)

        # Set window size and position
        self.set_window_geometry()

        # Event binding for resizing or moving the window
        self.bind("<Configure>", self.on_window_resize_or_move)

        self.show_home_page()

    def clear_container(self):
        """Removes all widgets from the UI."""
        for widget in self.container.winfo_children():
            widget.destroy()

    def styled_button(self, parent, text, command):
        """Creates a styled button."""
        btn = tk.Button(
            parent, text=text, font=self.option_font,
            bg=NORMAL_BG, fg=BG_COLOR, width=20, height=2,
            command=command
        )
        btn.pack(pady=20, ipadx=10, ipady=10)  # Add some padding inside the button
        return btn

    def show_home_page(self):
        """Displays the home screen."""
        self.clear_container()
        inner = tk.Frame(self.container, bg=BG_COLOR)
        inner.pack(fill="both", expand=True)

        tk.Label(inner, text="AuraTune", bg=BG_COLOR, fg="white", font=self.title_font).pack(pady=40)
        self.styled_button(inner, "Search Songs", self.next_step)
        self.styled_button(inner, "Info", self.show_info_page)

    def show_info_page(self):
        """Displays the info page with a back button."""
        self.clear_container()
        
        inner = tk.Frame(self.container, bg=BG_COLOR)
        inner.pack(fill="both", expand=True)

        # Display info content
        tk.Label(inner, text="About AuraTune", bg=BG_COLOR, fg="white", font=self.title_font).pack(pady=40)
        info_text = (
            "AuraTune recommends music based on your genre and song attribute preferences.\n\n"
            "We use a variety of factors like danceability, energy, and more to suggest songs that fit your mood."
        )
        tk.Label(inner, text=info_text, bg=BG_COLOR, fg="white", font=self.step_font, wraplength=500).pack(pady=20)

        # Back button
        self.styled_button(inner, "Back", self.show_home_page)

    def next_step(self):
        """Advances through genre and category selection steps."""
        self.clear_container()

        if self.step_index == 0:
            self._select_dropdown("Select a Genre", self.available_genres, "genre")
        elif self.step_index <= len(self.categories):
            category = self.categories[self.step_index - 1]
            self._select_button_row(f"Select level for {category}", ["Low", "Medium", "High"], category, lowercase=True)
        else:
            self.on_search_complete(self.user_inputs)
            self.show_home_page()
            return

        self.step_index += 1

    def _select_dropdown(self, title, options, key, lowercase=False):
        """Creates a dropdown selection screen."""
        inner = tk.Frame(self.container, bg=BG_COLOR)
        inner.pack(fill="both", expand=True)

        tk.Label(inner, text=title, bg=BG_COLOR, fg="white", font=self.title_font).pack(pady=20)

        var = tk.StringVar(value=options[0])
        dropdown = tk.OptionMenu(inner, var, *options)
        dropdown.config(font=self.option_font, bg=NORMAL_BG, fg=BG_COLOR)
        dropdown.pack(pady=10, fill='x', expand=True)

        tk.Label(inner, text=f"Step {self.step_index + 1} of {len(self.categories) + 1}",
                 bg=BG_COLOR, fg="white", font=self.step_font).pack(pady=10)

        self.styled_button(inner, "Next", lambda: self._save_and_continue(var.get(), key, lowercase))

    def _select_button_row(self, title, options, key, lowercase=False):
        """Creates horizontal buttons (Low, Medium, High)."""
        inner = tk.Frame(self.container, bg=BG_COLOR)
        inner.pack(fill="both", expand=True)

        tk.Label(inner, text=title, bg=BG_COLOR, fg="white", font=self.title_font).pack(pady=20)

        # Create buttons in a row (horizontally)
        button_frame = tk.Frame(inner, bg=BG_COLOR)
        button_frame.pack(pady=10)

        for option in options:
            btn = tk.Button(
                button_frame, text=option, font=self.option_font,
                bg=NORMAL_BG, fg=BG_COLOR, width=10, height=2,
                command=lambda option=option: self._save_and_continue(option, key, lowercase)
            )
            btn.pack(side="left", padx=10)

        tk.Label(inner, text=f"Step {self.step_index + 1} of {len(self.categories) + 1}",
                 bg=BG_COLOR, fg="white", font=self.step_font).pack(pady=10)

    def _save_and_continue(self, value, key, lowercase):
        """Saves the user input and moves to the next step."""
        self.user_inputs[key] = value.lower() if lowercase else value
        self.next_step()

    def set_window_geometry(self):
        """Set window size and center it on the screen."""
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = int(screen_width / 2)
        window_height = int(screen_height / 2)

        # Set window size and position it at the center
        self.geometry(f"{window_width}x{window_height}+{int((screen_width - window_width) / 2)}+{int((screen_height - window_height) / 2)}")

    def on_window_resize_or_move(self, event):
        """Recalculate and center window when moved or resized."""
        self.set_window_geometry()

if __name__ == '__main__':
    available_genres = ["Pop", "Rock", "Jazz", "Classical", "Hip-Hop"]
    def on_search_complete(user_inputs):
        print(user_inputs)  # Replace this with your own search functionality.

    app = GUIApp(available_genres, on_search_complete)
    app.mainloop()
