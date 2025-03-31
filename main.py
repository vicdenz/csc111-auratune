import pandas as pd
from const import SONG_DATA_FILE
from gui import GUIApp

# Run the program
if __name__ == "__main__":
    song_dataset = pd.read_csv(SONG_DATA_FILE)
    available_genres = song_dataset['track_genre'].unique().tolist()

    # genre_tree = SongDecisionTree()
    # genre_tree.build_genre_tree(song_dataset, "acoustic")
    # print(genre_tree.search_tree([CategoryLevel.MEDIUM, CategoryLevel.MEDIUM, CategoryLevel.MEDIUM, CategoryLevel.MEDIUM, CategoryLevel.MEDIUM]))

    app = GUIApp(song_dataset, available_genres)
    app.mainloop()