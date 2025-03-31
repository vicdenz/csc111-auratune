import csv
import numpy as np
from const import CategoryLevel, SONG_CATEGORIES

class Song:
    name: str
    artists: list[str]
    genre: str
    danceability: CategoryLevel
    energy: CategoryLevel
    instrumentalness: CategoryLevel
    valence: CategoryLevel
    loudness: CategoryLevel

    def __init__(self, name, artists, genre, danceability, energy, instrumentalness, valence, loudness):
        self.name = name
        self.artists = artists
        self.genre = genre
        self.danceability = danceability
        self.energy = energy
        self.instrumentalness = instrumentalness
        self.valence = valence
        self.loudness = loudness

    def __repr__(self):
        return f"Name: {self.name}, Artists: {";".join(self.artists)}, Genre: {self.genre}, Danceability: {self.danceability.name}, Energy: {self.energy.name}, Instrumentalness: {self.instrumentalness.name}, Valence: {self.valence.name}, Loudness: {self.loudness.name}"

class SongDecisionTree:
    def __init__(self):
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

    def search_tree(self, song_categories, depth=0):
        if depth == len(SONG_CATEGORIES):
            return self.songs

        if song_categories[depth] in self._subtrees:
            return self._subtrees[song_categories[depth]].search_tree(song_categories, depth + 1)
        else:
            return []

    def display_tree(self, depth=0):
        if self.songs:
            print("  " * depth + f"Songs: {[song.name for song in self.songs]}")

        for category, subtree in self._subtrees.items():
            print("  " * depth + f"{SONG_CATEGORIES[depth]}: {category.name}")
            subtree.display_tree(depth + 1)