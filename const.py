"""CSC111 Project 2: Auratune - Global Constants

===============================

This Python module contains global variables used throughout the project.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2025 CSC111 Teaching Team
"""

from enum import Enum

SONG_DATA_FILE = "song_data.csv"


class CategoryLevel(Enum):
    """
    An enumeration for categorizing song attributes (i.e. danceability, energy, instrumentalness, etc).

    - CategoryLevel (Enum): Represents intensity levels for song attributes.
        - LOW (0): Represents a low level of the attribute.
        - MEDIUM (1): Represents a medium level of the attribute.
        - HIGH (2): Represents a high level of the attribute.
    """
    LOW = 0
    MEDIUM = 1
    HIGH = 2


SONG_CATEGORIES = ("danceability", "energy", "instrumentalness", "valence", "loudness")

if __name__ == "__main__":
    pass
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['R1705', 'E9998', 'E9999']
    # })
