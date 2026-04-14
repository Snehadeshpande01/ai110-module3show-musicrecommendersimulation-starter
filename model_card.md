# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

This system suggests up to 5 songs from a 20-song catalog based on a user's preferred genre, mood, and energy level. It is designed for classroom exploration of how content-based recommenders work — not for real users or production use. It assumes the user can be described by a single fixed profile with one genre, one mood, and one energy target.

---

## 3. How the Model Works

For every song in the catalog, the system asks three questions:

1. Does this song's genre match what the user likes? If yes, it adds 2 points.
2. Does this song's mood match what the user wants to feel? If yes, it adds 1 point.
3. How close is the song's energy level to what the user wants? Songs that are closer get up to 1.5 points; songs far away get fewer.

After scoring all songs, it sorts them from highest to lowest score and returns the top 5. Each result comes with a plain-language explanation of which criteria it matched — so you can always see why a song was recommended.

---

## 4. Data

The catalog contains 20 songs stored in `data/songs.csv`. The 10 starter songs cover pop, lofi, rock, ambient, jazz, synthwave, and indie pop. Ten additional songs were added to expand coverage into edm, hip-hop, country, classical, r&b, and metal — with moods including euphoric, nostalgic, calm, romantic, and sad. Each song has numeric fields for energy (0–1), tempo, valence, danceability, and acousticness, though only energy is used in scoring. The dataset skews toward Western popular genres and does not represent global music traditions like afrobeats, K-pop, or Latin styles.

---

## 5. Strengths

- Works well for users whose taste matches a clearly defined genre. The Chill Lofi profile returned near-perfect scores (4.50, 4.39) because the catalog has dedicated lofi songs that match on all three criteria.
- The system is fully transparent — every recommendation comes with a reason, which makes it easy to understand and debug.
- Simple enough to reason about by hand. You can predict the top result just by knowing the weights.
- The Intense Rock profile correctly surfaced "Storm Runner" first (genre + mood + energy all match), which matched intuition immediately.

---

## 6. Limitations and Bias

- **Genre dominance:** The +2.0 genre bonus is so large that a song with a matching genre but wrong mood and low energy can still outrank a song that closely matches energy and mood in a different genre. This was confirmed in the adversarial test — "Velvet Rain" (r&b/sad, energy=0.38) ranked #1 for a user who wanted sad r&b at energy=0.9, despite being an energy mismatch.
- **Exact string matching:** "indie pop" and "pop" are treated as completely different genres even though they overlap musically. A user who likes pop will never see indie pop songs unless they happen to match on mood.
- **No diversity:** The top 5 often cluster around the same genre. A lofi user gets all lofi songs at the top with little variety.
- **Fixed profile:** Real users have shifting moods and contexts. This system treats every session identically.
- **Small catalog:** With only 20 songs, some genre searches return mostly energy-only matches in positions 3–5, not because the system failed but because there are simply no better options in the data.

---

## 7. Evaluation

Four user profiles were tested:

- **High-Energy Pop** (genre=pop, mood=happy, energy=0.8): Results matched intuition. Sunrise City ranked #1 on all three criteria. Gym Hero ranked #2 with genre match and high energy despite being "intense" not "happy."
- **Chill Lofi** (genre=lofi, mood=chill, energy=0.35): Both lofi/chill songs ranked 1–2. Focus Flow ranked #3 on genre alone despite a "focused" mood. Results felt accurate.
- **Intense Rock** (genre=rock, mood=intense, energy=0.9): Only one rock song exists, so #1 was obvious. Positions 2–3 (Gym Hero, Iron Curtain) both have "intense" mood, which felt right. Positions 4–5 were energy-only matches from unrelated genres.
- **Adversarial (r&b + sad + energy=0.9)**: Revealed the biggest weakness. "Velvet Rain" won despite low energy because genre+mood outweigh the energy gap. This is a real failure case for the scoring logic.

Weight shift experiment: halving genre weight and doubling energy weight pushed "Rooftop Lights" (indie pop/happy) ahead of "Gym Hero" (pop/intense), showing the system is sensitive to weight changes and that the default weights strongly favor genre over energy feel.

---

## 8. Future Work

- **Softer genre matching:** Use genre similarity groups (e.g., pop ≈ indie pop ≈ dance pop) instead of exact string equality to reduce the genre wall effect.
- **Dynamic weights by context:** Let users specify whether they care more about mood, energy, or genre — and adjust weights accordingly rather than using one fixed set.
- **Diversity constraint:** Prevent the top 5 from being all the same genre by adding a small penalty for repeated genres in the ranked list.
- **More features in scoring:** Valence (musical positivity) and tempo_bpm are already loaded but unused. Adding them would give the system a better sense of a song's feel, not just its label.

---

## 9. Personal Reflection

The biggest surprise was how much the weights matter. Changing genre from +2.0 to +1.0 was a single number change, but it visibly reshuffled the top results — songs that felt "right" by energy suddenly competed with songs that felt "right" by genre. That made it real: every recommendation system has numbers like these baked in, and the people who set them are making decisions about what "good" means for everyone using the product.

The adversarial test was also humbling. A user who wants sad r&b at high energy gets "Velvet Rain" — a slow, low-energy song — because the genre and mood labels match. The system did exactly what it was told to do, and the output was still wrong. That gap between "follows the rules" and "actually helpful" is probably the most important thing to carry forward when thinking about real AI recommenders.
