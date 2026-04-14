"""
Command line runner for the Music Recommender Simulation.
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded {len(songs)} songs from catalog.\n")

    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
    print(f"User Profile: genre={user_prefs['genre']}, mood={user_prefs['mood']}, energy={user_prefs['energy']}")

    WIDTH = 72
    print("=" * WIDTH)
    print(f"  {'#':<4} {'Title':<24} {'Score':<8} Reasons")
    print("-" * WIDTH)

    recommendations = recommend_songs(user_prefs, songs, k=5)
    for i, (song, score, reasons_str) in enumerate(recommendations, 1):
        reasons_display = " | ".join(f"[{r}]" for r in reasons_str.split(", "))
        print(f"  {i:<4} {song['title']:<24} {score:<8.2f} {reasons_display}")

    print("=" * WIDTH)


if __name__ == "__main__":
    main()
