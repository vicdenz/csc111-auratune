class SongNode:
    name: str
    artists: list[str]
    genre: list[str]
    danceability: int
    energy: int
    instrumentalness: int
    valence: int
    loudness: int
    
    def __init__(self, song_data=None):
        if song_data is None:
            self.name = None
            self.artists = None
            self.genre = None
            self.danceability = None
            self.energy = None
            self.instrumentalness = None
            self.valence = None
            self.loudness = None
            self._left = None
            self._right = None
        else:
            self.name = song_data['name']
            self.artists = song_data['artists']
            self.genre = song_data['genre']
            self.danceability = song_data['danceability']
            self.energy = song_data['energy']
            self.instrumentalness = song_data['instrumentalness']
            self.valence = song_data['valence']
            self.loudness = song_data['loudness']
            self._left = SongNode()
            self._right = SongNode()

class SongTree:
    def __init__(self):
        self.graph = {}

    def add_song(self, song_title, song_data):
        if song_title not in self.graph:
            self.graph[song_title] = {"data": song_data, "edges": []}

    def add_edge(self, song1_title, song2_title):
        if song1_title in self.graph and song2_title in self.graph:
            self.graph[song1_title]["edges"].append(song2_title)
            self.graph[song2_title]["edges"].append(song1_title)

    def get_neighbors(self, song_title):
        if song_title in self.graph:
            return self.graph[song_title]["edges"]
        return []