"""CSC111 Project 2: Auratune - Main Interface

===============================

This Python module contains the main function to run the program.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2025 CSC111 Teaching Team
"""
import pandas as pd
from const import SONG_DATA_FILE
from gui import GUIApp


if __name__ == "__main__":
    song_dataset = pd.read_csv(SONG_DATA_FILE)
    available_genres = song_dataset['track_genre'].unique().tolist()

    app = GUIApp(song_dataset, available_genres)
    app.mainloop()
