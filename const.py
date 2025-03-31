from enum import Enum

SONG_DATA_FILE = "song_data.csv"

class CategoryLevel(Enum):
    LOW = 0
    MEDIUM = 1
    HIGH = 2

SONG_CATEGORIES = ("danceability", "energy", "instrumentalness", "valence", "loudness")