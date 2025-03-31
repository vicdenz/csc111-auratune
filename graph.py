import numpy as np
from const import CategoryLevel, SONG_CATEGORIES

def get_songs_by_genre(song_dataset, chosen_genre):
    return song_dataset[song_dataset['track_genre'] == chosen_genre]

def categorize_attribute(value, thresholds):
	if value <= thresholds[0]:
		return CategoryLevel.LOW
	elif value <= thresholds[1]:
		return CategoryLevel.MEDIUM
	else:
		return CategoryLevel.HIGH

def compute_thresholds(song_dataset, category):
	return np.percentile(song_dataset[category], [33, 66])

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

    def __init__(self, name, artists, genre, danceability, energy, instrumentalness, valence, loudness, popularity):
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
        return f"Song<Name: {self.name}, Artists: {";".join(self.artists)}, Genre: {self.genre}, Danceability: {self.danceability.name}, Energy: {self.energy.name}, Instrumentalness: {self.instrumentalness.name}, Valence: {self.valence.name}, Loudness: {self.loudness.name}, Popularity: {self.popularity}>"

class SongDecisionTree:
    def __init__(self):
        self.songs = []
        self._subtrees = {}

    def is_empty(self):
        return not (self.songs or self._subtrees)

    def clear_tree(self):
        self.songs = []
        self._subtrees = {}

    def insert_song(self, song: Song, depth=0):
        if depth == len(SONG_CATEGORIES):
            self.songs.append(song)
            return True
        
        song_category_level = getattr(song, SONG_CATEGORIES[depth], None)
        if song_category_level not in self._subtrees:
            self._subtrees[song_category_level] = SongDecisionTree()
        self._subtrees[song_category_level].insert_song(song, depth + 1)

        return False

    def search_tree(self, song_categories, sort_by_popularity=True, depth=0):
        if depth == len(SONG_CATEGORIES):
            if sort_by_popularity:
                return self.songs #sorted(self.songs, key=lambda song: song.popularity)
            else:
                return self.songs

        if song_categories[depth] in self._subtrees:
            return self._subtrees[song_categories[depth]].search_tree(song_categories, depth=depth + 1)
        else:
            return []

    def display_tree(self, depth=0):
        if self.songs:
            print("  " * depth + f"Songs: {[song.name for song in self.songs]}")

        for category, subtree in self._subtrees.items():
            print("  " * depth + f"{SONG_CATEGORIES[depth]}: {category.name}")
            subtree.display_tree(depth + 1)

    def build_genre_tree(self, song_dataset, chosen_genre):
        genre_songs = get_songs_by_genre(song_dataset, chosen_genre)  # Get songs with the chosen_genre

        if not genre_songs.empty:
            genre_category_thresholds = {category: compute_thresholds(genre_songs, category) for category in SONG_CATEGORIES}

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