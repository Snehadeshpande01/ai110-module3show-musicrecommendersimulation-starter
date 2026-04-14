"""
Command line runner for the Music Recommender Simulation.
"""

from tabulate import tabulate
from src.recommender import load_songs, recommend_songs, SCORING_MODES


def print_recommendations(profile_label: str, user_prefs: dict, songs: list,
                          mode: str = "default", diversity: bool = False) -> None:
    """Print a tabulate-formatted recommendation table for one user profile."""
    mode_label = f"mode={mode}" + (" + diversity=on" if diversity else "")
    print(f"\nProfile: {profile_label}  [{mode_label}]")
    print(f"  genre={user_prefs['genre']}, mood={user_prefs['mood']}, energy={user_prefs['energy']}")

    recommendations = recommend_songs(user_prefs, songs, k=5, mode=mode, diversity=diversity)

    # Challenge 4: Visual Summary Table via tabulate
    rows = []
    for i, (song, score, reasons_str) in enumerate(recommendations, 1):
        reasons_display = " | ".join(f"[{r}]" for r in reasons_str.split(", "))
        rows.append([i, song['title'], song['artist'], f"{score:.2f}", reasons_display])

    print(tabulate(rows, headers=["#", "Title", "Artist", "Score", "Reasons"],
                   tablefmt="outline"))


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded {len(songs)} songs from catalog.")

    user_prefs_pop   = {"genre": "pop",   "mood": "happy",   "energy": 0.8}
    user_prefs_lofi  = {"genre": "lofi",  "mood": "chill",   "energy": 0.35}
    user_prefs_rock  = {"genre": "rock",  "mood": "intense", "energy": 0.9}
    user_prefs_adv   = {"genre": "r&b",   "mood": "sad",     "energy": 0.9}

    # --- Default profile ---
    print_recommendations("High-Energy Pop", user_prefs_pop, songs)

    # --- Challenge 2: Scoring Modes ---
    print("\n" + "=" * 60)
    print("  CHALLENGE 2: Multiple Scoring Modes (pop/happy profile)")
    print("=" * 60)
    for mode in SCORING_MODES:
        print_recommendations(f"Pop/Happy - {mode}", user_prefs_pop, songs, mode=mode)

    # --- Challenge 3: Diversity Penalty ---
    print("\n" + "=" * 60)
    print("  CHALLENGE 3: Diversity Penalty (no repeat artists)")
    print("=" * 60)
    print_recommendations("Chill Lofi - no diversity", user_prefs_lofi, songs, diversity=False)
    print_recommendations("Chill Lofi - diversity ON", user_prefs_lofi, songs, diversity=True)

    # --- Other profiles ---
    print("\n" + "=" * 60)
    print("  Other Profiles")
    print("=" * 60)
    print_recommendations("Intense Rock",              user_prefs_rock, songs)
    print_recommendations("Adversarial (sad + 0.9)",   user_prefs_adv,  songs)


if __name__ == "__main__":
    main()
