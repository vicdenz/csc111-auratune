import tkinter as tk
from tkinter import font, messagebox
from graph import SongTree

FEATURES = [
    ("Danceability", ["Low", "Medium", "High"]),
    ("Energy", ["Low", "Medium", "High"]),
    ("Instrumentalness", ["Low", "Medium", "High"]),
    ("Valence", ["Low", "Medium", "High"]),
    ("Loudness", ["Low", "Medium", "High"])
]

HOVER_BG = "#a87cdc"
NORMAL_BG = "white"

class AuraTuneApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AuraTune")
        self.attributes('-fullscreen', True)
        self.configure(bg="#6a0dad")

        self.title_font = font.Font(family="Georgia", size=48, weight="bold")
        self.option_font = font.Font(family="Helvetica", size=28)
        self.note_font = font.Font(family="Arial", size=36)

        self.current_step = 0
        self.user_choices = {}
        self.song_graph = self.build_song_graph()

        self.container = tk.Frame(self, bg="#6a0dad")
        self.container.pack(fill="both", expand=True)

        self.show_intro()

        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))
    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def hover_effects(self, btn):
        btn.bind("<Enter>", lambda e: btn.config(bg=HOVER_BG))
        btn.bind("<Leave>", lambda e: btn.config(bg=NORMAL_BG))

    def styled_button(self, parent, text, command):
        btn = tk.Button(
            parent,
            text=text,
            font=self.option_font,
            bg=NORMAL_BG,
            fg="#6a0dad",
            width=16,
            height=2,
            command=command
        )
        btn.pack(pady=20)
        self.hover_effects(btn)
        return btn

    def show_intro(self):
        self.clear_container()

        inner = tk.Frame(self.container, bg="#6a0dad")
        inner.pack(expand=True)

        tk.Label(
            inner,
            text="AuraTune",
            bg="#6a0dad",
            fg="white",
            font=self.title_font
        ).pack(pady=40)

        self.styled_button(inner, "Start", self.start_feature_selection)
        self.styled_button(inner, "Info", self.show_info)

    def show_info(self):
        messagebox.showinfo(
            "About AuraTune",
            "AuraTune recommends music based on your current mood and style preferences.\n\n"
            "You will be asked to choose song characteristics like danceability and energy.\n"
            "At the end, AuraTune will recommend a song that matches your vibe!"
        )

    def start_feature_selection(self):
        self.current_step = 0
        self.user_choices = {}
        self.show_feature_step()

    def show_feature_step(self):
        self.clear_container()

        feature, options = FEATURES[self.current_step]

        inner = tk.Frame(self.container, bg="#6a0dad")
        inner.pack(expand=True)

        tk.Label(
            inner,
            text="🎵 🎶 🎼 🎹 🎧",
            bg="#6a0dad",
            fg="white",
            font=self.note_font
        ).pack(pady=(10, 5))

        tk.Label(
            inner,
            text=f"Select {feature}:",
            bg="#6a0dad",
            fg="white",
            font=self.title_font
        ).pack(pady=20)

        button_frame = tk.Frame(inner, bg="#6a0dad")
        button_frame.pack(pady=20)

        for option in options:
            btn = tk.Button(
                button_frame,
                text=option,
                font=self.option_font,
                width=12,
                height=2,
                bg=NORMAL_BG,
                fg="#6a0dad",
                command=lambda opt=option: self.select_option(opt)
            )
            btn.pack(side="left", padx=30)
            self.hover_effects(btn)

        tk.Label(
            inner,
            text=f"Step {self.current_step + 1} of {len(FEATURES)}",
            bg="#6a0dad",
            fg="white",
            font=self.option_font
        ).pack(pady=(30, 10))

    def select_option(self, selection):
        feature_name = FEATURES[self.current_step][0]
        self.user_choices[feature_name] = selection

        self.current_step += 1
        if self.current_step < len(FEATURES):
            self.show_feature_step()
        else:
            self.show_recommendation()

    def show_recommendation(self):
        self.clear_container()

        recommended_song = self.recommend_song()

        inner = tk.Frame(self.container, bg="#6a0dad")
        inner.pack(expand=True)

        if recommended_song:
            tk.Label(
                inner,
                text="Recommended Music",
                bg="#6a0dad",
                fg="white",
                font=self.title_font
            ).pack(pady=40)

            tk.Label(
                inner,
                text=f"🎶 {recommended_song['title']} by {recommended_song['artist']}",
                bg="#6a0dad",
                fg="white",
                font=self.option_font
            ).pack(pady=20)
        else:
            tk.Label(
                inner,
                text="No matching song found!",
                bg="#6a0dad",
                fg="white",
                font=self.option_font
            ).pack(pady=40)

        self.styled_button(inner, "Back to Start", self.show_intro)
