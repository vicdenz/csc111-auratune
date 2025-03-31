import pandas as pd
from const import SONG_DATA_FILE
from gui import GUIApp


if __name__ == "__main__":
    song_dataset = pd.read_csv(SONG_DATA_FILE)
    available_genres = song_dataset['track_genre'].unique().tolist()

    app = GUIApp(song_dataset, available_genres)
    app.mainloop()
