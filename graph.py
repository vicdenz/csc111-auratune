"""CSC111 Project 2: Auratune - Genre Decision Tree

Instructions (READ THIS FIRST!)
===============================

This Python module contains the Song dataclass and SongDecisionTree class, to be imported and used by the `gui` module.

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
import numpy as np
from const import CategoryLevel, SONG_CATEGORIES


def get_songs_by_genre(song_dataset: pd.DataFrame, chosen_genre: str) -> pd.DataFrame:
    """Filter songs by the given genre and returns a pd.DataFrame with the filtered songs.

    Representation Invariants:
    - song_dataset must be a pandas DataFrame containing a 'track_genre' column.
    - chosen_genre must be a string representing a valid genre in song_dataset.
    """
    return song_dataset[song_dataset['track_genre'] == chosen_genre]


def categorize_attribute(value: float, thresholds: list[float]) -> CategoryLevel:
    """Categorize a numerical attribute based on threshold values and returns the corresponding CategoryLevel enum.

    Representation Invariants:
    - value must be a float.
    - thresholds must be a list of exactly two float values in ascending order: [low_threshold, high_threshold].
    """
    if value <= thresholds[0]:
        return CategoryLevel.LOW
    elif value <= thresholds[1]:
        return CategoryLevel.MEDIUM
    else:
        return CategoryLevel.HIGH


def compute_thresholds(song_dataset: pd.DataFrame, category: str) -> list[float]:
    """Compute threshold values for categorizing a song attribute.

    Representation Invariants:
    - song_dataset must be a pandas DataFrame containing numeric values for the given category.
    - category must be a string corresponding to a valid column in song_dataset.
    """
    return np.percentile(song_dataset[category], [33, 66]).tolist()


class Song:
    name: str
    artists: list[str]
    genre: str
    danceability: CategoryLevel
    energy: CategoryLevel
    instrumentalness: CategoryLevel
    valence: CategoryLevel
    loudness: CategoryLevel
    popularity: int

    def __init__(self, name: str, artists: list[str], genre: str, danceability: CategoryLevel, 
                 energy: CategoryLevel, instrumentalness: CategoryLevel, valence: CategoryLevel, 
                 loudness: CategoryLevel, popularity: int) -> None:
        self.name = name
        self.artists = artists
        self.genre = genre
        self.danceability = danceability
        self.energy = energy
        self.instrumentalness = instrumentalness
        self.valence = valence
        self.loudness = loudness
        self.popularity = popularity

    def __repr__(self):
        return (f"Song<Name: {self.name}, Artists: {';'.join(self.artists)}, Genre: {self.genre}, "
                f"Danceability: {self.danceability.name}, Energy: {self.energy.name}, "
                f"Instrumentalness: {self.instrumentalness.name}, Valence: {self.valence.name}, "
                f"Loudness: {self.loudness.name}, Popularity: {self.popularity}>")


class SongDecisionTree:
    def __init__(self):
        self.songs = []
        self._subtrees = {}

    def is_empty(self):
        return not (self.songs or self._subtrees)

    def clear_tree(self):
        self.songs = []
        self._subtrees = {}

    def insert_song(self, song: Song, depth: int = 0) -> bool:
        if depth == len(SONG_CATEGORIES):
            self.songs.append(song)
            return True

        song_category_level = getattr(song, SONG_CATEGORIES[depth], None)
        if song_category_level not in self._subtrees:
            self._subtrees[song_category_level] = SongDecisionTree()
        self._subtrees[song_category_level].insert_song(song, depth + 1)

        return False

    def search_tree(self, song_categories: list[CategoryLevel], sort_by_popularity: bool = True, depth: int = 0) -> list[Song]:
        if depth == len(SONG_CATEGORIES):
            if sort_by_popularity:
                return self.songs  # sorted(self.songs, key=lambda song: song.popularity)
            else:
                return self.songs

        if song_categories[depth] in self._subtrees:
            return self._subtrees[song_categories[depth]].search_tree(song_categories, depth=depth + 1)
        else:
            return []

    def display_tree(self, depth: int = 0) -> None:
        if self.songs:
            print("  " * depth + f"Songs: {[song.name for song in self.songs]}")

        for category, subtree in self._subtrees.items():
            print("  " * depth + f"{SONG_CATEGORIES[depth]}: {category.name}")
            subtree.display_tree(depth + 1)

    def build_genre_tree(self, song_dataset: pd.DataFrame, chosen_genre: str) -> None:
        genre_songs = get_songs_by_genre(song_dataset, chosen_genre)  # Get songs with the chosen_genre

        if not genre_songs.empty:
            genre_category_thresholds = {
                category: compute_thresholds(genre_songs, category) for category in SONG_CATEGORIES
            }

            for _, row in genre_songs.iterrows():
                song_data = {
                    'name': row['track_name'],
                    'artists': row['artists'].split(';'),
                    'genre': chosen_genre,
                    'popularity': row['popularity']
                }
                for category in SONG_CATEGORIES:
                    song_data[category] = categorize_attribute(row[category], genre_category_thresholds[category])

                self.insert_song(Song(**song_data))


if __name__ == "__main__":
    # pass
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['R1705', 'E9998', 'E9999']
    })
