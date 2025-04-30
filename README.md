# AuraTune 🎧

_A personalized music recommendation application based on genre and musical preferences._

## Authors

David Daniliuc, Aaryan Patel, Victor Rizzo Choairy, Hayato Kukihara

---

## 📌 Overview

**AuraTune** is a desktop application that recommends songs based on a user’s preferred genre and desired audio characteristics levels. Rather than relying solely on genre tags, AuraTune uses audio characteristics like **danceability**, **energy**, **valence**, and **loudness** to match music to user-defined preferences. Users interact with the application via a Tkinter GUI and select _low_, _medium_, or _high_ levels for five audio characteristics.

---

## ⚙️ Features

-   🎵 Personalized music recommendations based on style preferences
-   🌳 Decision tree model to cluster songs by audio features
-   🧠 User input for five key attributes: danceability, energy, valence, loudness, instrumentalness
-   🎛 GUI built with Tkinter for ease of use
-   📂 Works with a pre-downloaded `.csv` Spotify dataset (no external API needed)

---

## 📁 Dataset

AuraTune uses a third-party Spotify track dataset available on [Kaggle](https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset).  
Features used include:

-   `track_name`, `artists`, `track_genre`, `danceability`, `energy`, `valence`, `loudness`, `instrumentalness`

Note: The dataset has been cleaned to remove incomplete entries, reducing it to ~75,000 usable tracks.

---

## 🛠 Installation

1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`

Note: tkinter is pre-installed with most Python distributions.

---

## 🚀 Usage

1. Run the main program: `python main.py`

---

## References

-   [NumPy Documentation](https://numpy.org/doc/)
-   [pandas Documentation](https://pandas.pydata.org/docs/)
-   [Spotify Tracks Dataset – Kaggle](https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset)
-   [W3Schools Decision Tree Guide](https://www.w3schools.com/python/python_ml_decision_tree.asp)
