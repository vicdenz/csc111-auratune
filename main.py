import pandas as pd
import numpy as np
from graph import Song, SongDecisionTree
from const import SONG_DATA_FILE, CategoryLevel, SONG_CATEGORIES
from gui import AuraTuneApp

def get_available_genres(song_dataset):
    return set(song_dataset['track_genre'].unique())

def get_songs_by_genre(song_dataset, genre):
    return song_dataset[song_dataset['track_genre'] == genre]

def categorize_attribute(value, thresholds):
    if value <= thresholds[0]:
        return CategoryLevel.LOW
    elif value <= thresholds[1]:
        return CategoryLevel.MEDIUM
    else:
        return CategoryLevel.HIGH

def compute_thresholds(song_dataset, category):
    return np.percentile(song_dataset[category], [33, 66])

# Run the program
if __name__ == "__main__":
    song_dataset = pd.read_csv(SONG_DATA_FILE)

    available_genres = get_available_genres(song_dataset)

    chosen_genre = "edm"

    genre_tree = SongDecisionTree()

    songs_found = get_songs_by_genre(song_dataset, chosen_genre)

    if not songs_found.empty:
        genre_category_thresholds = {category: compute_thresholds(songs_found, category) for category in SONG_CATEGORIES}

        song_objs = []
        for _, row in songs_found.iterrows():
            song_data = {
                'name': row['track_name'],
                'artists': row['artists'].split(';'),
                'genre': chosen_genre
            }
            for category in SONG_CATEGORIES:
                song_data[category] = categorize_attribute(row[category], genre_category_thresholds[category])

            genre_song = Song(**song_data)

            song_objs.append(genre_song)
            genre_tree.insert_song(genre_song)

        # DEBUG
        for song in song_objs:
            song_categories = [getattr(song, category) for category in SONG_CATEGORIES]
            if song not in genre_tree.search_tree(song_categories):
                print(f"Error: {song.name}, {";".join(song.artists)}, {song_categories}")
                break

    app = AuraTuneApp()
    app.mainloop()