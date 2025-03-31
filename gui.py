import tkinter as tk
from tkinter import font
from graph import SongDecisionTree
from const import SONG_CATEGORIES, CategoryLevel

class GUIApp(tk.Tk):
    
    def __init__(self, song_dataset, available_genres):
        super().__init__()
        self.song_dataset = song_dataset
        self.genre_tree = SongDecisionTree()
        self.available_genres = available_genres
        self.max_songs_found = 5

        self.genre_selected = ''
        self.categories_selected = []
        self.category_index = 0

        # Theme Colors
        self.bg_color = "#6a0dad"
        self.hover_color = "#a87cdc"
        self.text_color = "white"

        self.configure(bg=self.bg_color)
        self.title("AuraTune")

        # Fonts
        self.title_font = font.Font(family="Georgia", size=48, weight="bold")
        self.option_font = font.Font(family="Helvetica", size=28)
        self.text_font = font.Font(family="Arial", size=24)

        self.container = tk.Frame(self, bg=self.bg_color)
        self.container.pack(fill="both", expand=True)

        # Set window size and position
        self.set_window_geometry()

        # Event binding for resizing or moving the window
        self.bind("<Configure>", self.window_resize_event)

        self.show_home_page()

    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def clear_user_selection(self):
        self.genre_selected = ''
        self.categories_selected = []
        self.category_index = 0
        self.genre_tree.clear_tree()

    def styled_button(self, parent, text, command):
        btn = tk.Button(
            parent, text=text, font=self.option_font,
            bg=self.text_color, fg=self.bg_color, width=20, height=2,
            command=command
        )
        btn.pack(pady=20, ipadx=10, ipady=10)  # Add some padding inside the button
        return btn

    def show_home_page(self):
        self.clear_container()
        inner = tk.Frame(self.container, bg=self.bg_color)
        inner.pack(fill="both", expand=True)

        tk.Label(inner, text="AuraTune", bg=self.bg_color, fg="white", font=self.title_font).pack(pady=40)
        self.styled_button(inner, "Search Songs", self.show_next_decision_page)
        self.styled_button(inner, "Info", self.show_info_page)

    def show_info_page(self):
        self.clear_container()
        
        inner = tk.Frame(self.container, bg=self.bg_color)
        inner.pack(fill="both", expand=True)

        # Display info content
        tk.Label(inner, text="About AuraTune", bg=self.bg_color, fg="white", font=self.title_font).pack(pady=40)
        info_text = "AuraTune recommends music based on your genre and song attribute preferences.\n\nWe use a variety of factors like danceability, energy, and more to suggest songs that fit your mood."
        tk.Label(inner, text=info_text, bg=self.bg_color, fg="white", font=self.text_font, wraplength=500).pack(pady=20)

        # Back button
        self.styled_button(inner, "Back To Home", self.show_home_page)

    def show_next_decision_page(self):
        self.clear_container()

        if self.category_index == 0:
            self._select_dropdown("Select a Genre", self.available_genres)
        elif self.category_index <= len(SONG_CATEGORIES):
            category = SONG_CATEGORIES[self.category_index - 1]
            self._select_button_row(f"Select level for {category}", ["Low", "Medium", "High"])
        else:
            self.show_songs_page()
            return

        self.category_index += 1

    def show_songs_page(self):
        self.clear_container()
        
        inner = tk.Frame(self.container, bg=self.bg_color)
        inner.pack(fill="both", expand=True)

        found_songs = self.genre_tree.search_tree(self.categories_selected)
        self.clear_user_selection()

        # Display info content
        tk.Label(inner, text="Recommended Songs", bg=self.bg_color, fg="white", font=self.title_font).pack(pady=20)
        info_text = ""
        for song in found_songs[0:self.max_songs_found]:
            info_text += f"{song.name} by {", ".join(song.artists)}\n\n"
        tk.Label(inner, text=info_text, bg=self.bg_color, fg="white", font=self.text_font, wraplength=500).pack(pady=10)

        # Back button
        self.styled_button(inner, "Back To Home", self.show_home_page)

    def _select_dropdown(self, title, options):
        inner = tk.Frame(self.container, bg=self.bg_color)
        inner.pack(fill="both", expand=True)

        tk.Label(inner, text=title, bg=self.bg_color, fg="white", font=self.title_font).pack(pady=20)

        var = tk.StringVar(value=options[0])
        dropdown = tk.OptionMenu(inner, var, *options)
        dropdown.config(font=self.option_font, bg=self.text_color, fg=self.bg_color)
        dropdown.pack(pady=10, expand=True)

        tk.Label(inner, text=f"Step {self.category_index + 1} of {len(SONG_CATEGORIES) + 1}",
                 bg=self.bg_color, fg="white", font=self.text_font).pack(pady=10)

        self.styled_button(inner, "Next", lambda: self._save_genre(var.get()))

    def _select_button_row(self, title, options):
        inner = tk.Frame(self.container, bg=self.bg_color)
        inner.pack(fill="both", expand=True)

        tk.Label(inner, text=title, bg=self.bg_color, fg="white", font=self.title_font).pack(pady=20)

        # Create buttons in a row (horizontally)
        button_frame = tk.Frame(inner, bg=self.bg_color)
        button_frame.pack(pady=10)

        for option in options:
            btn = tk.Button(
                button_frame, text=option, font=self.option_font,
                bg=self.text_color, fg=self.bg_color, width=10, height=2,
                command=lambda option=option: self._save_category(option)
            )
            btn.pack(side="left", padx=10)

        tk.Label(inner, text=f"Step {self.category_index + 1} of {len(SONG_CATEGORIES) + 1}",
                 bg=self.bg_color, fg="white", font=self.text_font).pack(pady=10)

    def _save_genre(self, genre):
        self.genre_selected = genre.lower()
        self.genre_tree.build_genre_tree(self.song_dataset, self.genre_selected)
        self.show_next_decision_page()

    def _save_category(self, category):
        self.categories_selected.append(CategoryLevel[category.upper()])
        self.show_next_decision_page()

    def set_window_geometry(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = int(screen_width / 3) * 2
        window_height = int(screen_height / 3) * 2

        # Set window size and position it at the center
        self.geometry(f"{window_width}x{window_height}+{int((screen_width - window_width) / 2)}+{int((screen_height - window_height) / 2)}")

    def window_resize_event(self, event):
        self.set_window_geometry()