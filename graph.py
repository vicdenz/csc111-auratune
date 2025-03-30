import csv

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
        """
        Add a song as a node in the graph.
        """
        if song_title not in self.graph:
            self.graph[song_title] = {"data": song_data, "edges": []}

    def add_edge(self, song1_title, song2_title):
        """
        Add an edge between two songs if they share a similar genre or features.
        """
        if song1_title in self.graph and song2_title in self.graph:
            self.graph[song1_title]["edges"].append(song2_title)
            self.graph[song2_title]["edges"].append(song1_title)

    def get_neighbors(self, song_title):
        """
        Get all neighboring songs connected to the given song.
        """
        if song_title in self.graph:
            return self.graph[song_title]["edges"]
        return []

    def display_graph(self):
        """
        Print the graph structure for debugging.
        """
        for song, details in self.graph.items():
            print(f"Song: {song}")
            print(f"  Data: {details['data']}")
            print(f"  Edges: {details['edges']}")
            print()


def read_song_data(filepath):
    """
    Reads song data from a CSV file and returns a list of dictionaries.
    """
    songs = []
    try:
        with open(filepath, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                song = {
                    "name": row["name"],
                    "artists": row["artists"].split(", "),  # Assuming artists are comma-separated
                    "genre": row["genre"].split(", "),  # Assuming genres are comma-separated
                    "danceability": float(row["danceability"]),
                    "energy": float(row["energy"]),
                    "instrumentalness": float(row["instrumentalness"]),
                    "valence": float(row["valence"]),
                    "loudness": float(row["loudness"])
                }
                songs.append(song) 
    return songs


def build_graph_from_csv(filepath):
    """
    Reads song data from a CSV file and builds a SongTree graph.
    """
    songs = read_song_data(filepath)

    song_tree = SongTree()

    for song in songs:
        song_node = SongNode(song)
        song_tree.add_song(song_node.name, song_node)

    for song1 in songs:
        for song2 in songs:
            if song1["name"] != song2["name"] and song1["genre"] == song2["genre"]:
                song_tree.add_edge(song1["name"], song2["name"])

    return song_tree
