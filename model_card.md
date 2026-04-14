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

Four user profiles were tested and the results were compared against what a human listener would expect.

**Profile 1 — High-Energy Pop** (genre=pop, mood=happy, energy=0.8)

"Sunrise City" ranked #1 with a score of 4.47 — it matched all three criteria (pop genre, happy mood, energy=0.82). This felt exactly right. The surprise was "Gym Hero" at #2 with a score of 3.30. It is a pop song with high energy, but its mood is "intense" — not "happy." It ranked that high purely because the genre bonus (+2.0) is so strong that it carried Gym Hero above every non-pop song even without a mood match. A real listener wanting happy pop probably would not want a workout song in their top 5, but the system cannot tell the difference between "pop-happy" and "pop-intense."

**Profile 2 — Chill Lofi** (genre=lofi, mood=chill, energy=0.35)

"Library Rain" and "Midnight Coding" scored 4.50 and 4.39 respectively — both perfect matches on all three criteria. This was the most accurate-feeling result of all four tests. The only mild surprise was "Focus Flow" at #3 (score 3.42): it is a lofi song but its mood is "focused," not "chill." It ranked #3 purely because genre match (+2.0) outweighed the missing mood point. Whether a focused lofi track is a good recommendation for someone who wants chill music is debatable — instrumentally it might fit, but the label mismatch shows how much the system relies on exact tags.

**Profile 3 — Intense Rock** (genre=rock, mood=intense, energy=0.9)

"Storm Runner" ranked #1 at 4.48 — the only rock song in the catalog, so this was expected. What was interesting was positions 2 and 3: "Gym Hero" (pop/intense) and "Iron Curtain" (metal/intense) both ranked on mood match alone. They have no genre overlap with rock at all, but their "intense" mood tag earned them +1.0 each. This shows the system can surface cross-genre recommendations when mood is shared — which sometimes makes sense, and sometimes does not. A rock listener probably welcomes metal but might be confused by a pop workout track at #2.

**Profile 4 — Adversarial (genre=r&b, mood=sad, energy=0.9)**

This was the most revealing test. "Velvet Rain" ranked #1 with a score of 3.72 — it matched genre (r&b) and mood (sad), so it earned +3.0 from those alone. But its actual energy is 0.38, which is nearly the opposite of the user's target of 0.9. The energy closeness score was only +0.72 out of a possible 1.5. Despite this penalty, genre and mood together were still enough to win. This is a genuine failure: the user asked for something intense and driving, and the system returned a slow ballad because the labels matched. It confirms that the +2.0 genre weight can override meaningful numeric signals when the catalog is small.

**Weight Shift Experiment** (genre weight halved to 1.0, energy weight doubled to 3.0)

Running the pop/happy profile with adjusted weights pushed "Rooftop Lights" (indie pop/happy) from #3 to #2, overtaking "Gym Hero." With genre worth less, a song that closely matches energy and mood but sits in a related genre can finally compete. "Sunrise City" still ranked #1 because it wins on all three criteria regardless of weights. This experiment confirmed that the default scoring is genre-dominant by design, and that small weight changes have outsized effects on diversity in the results.

---

## 8. Future Work

- **Softer genre matching:** Use genre similarity groups (e.g., pop ≈ indie pop ≈ dance pop) instead of exact string equality to reduce the genre wall effect.
- **Dynamic weights by context:** Let users specify whether they care more about mood, energy, or genre — and adjust weights accordingly rather than using one fixed set.
- **Diversity constraint:** Prevent the top 5 from being all the same genre by adding a small penalty for repeated genres in the ranked list.
- **More features in scoring:** Valence (musical positivity) and tempo_bpm are already loaded but unused. Adding them would give the system a better sense of a song's feel, not just its label.

---

## 9. Personal Reflection

**Biggest learning moment:** The biggest learning moment was realizing that weights are design decisions, not just numbers. When I halved the genre weight from +2.0 to +1.0, the entire top-5 list reshuffled — songs that previously had no chance suddenly competed because energy and mood could finally make a difference. That one change showed me that every recommender system is really a statement about what matters most to the people who built it, not just the people using it. Engineers at Spotify or YouTube are making those same choices at a scale that affects millions of listeners, often invisibly.

**How AI tools helped and when I double-checked:** AI tools helped most with boilerplate structure — generating the CSV format for new songs, suggesting the `tabulate` library for formatting, and explaining the difference between `.sort()` and `sorted()`. But I had to double-check the scoring logic carefully because the AI-suggested energy formula worked mathematically but I needed to verify it actually rewarded *closeness* and not just *highness*. I also had to validate that the diversity penalty correctly de-duplicated by artist rather than by genre, since an early version would have been too aggressive. The rule I learned: AI suggestions are a fast starting point, but the only way to trust them is to trace through an example by hand.

**What surprised me about simple algorithms feeling like recommendations:** The most surprising thing was how quickly the output started feeling "right" even with just three scoring rules. When the Chill Lofi profile returned Library Rain and Midnight Coding at the top with scores of 4.50 and 4.39, it genuinely looked like something Spotify might suggest. The illusion of intelligence comes from the combination of ranking (so only the best appear), explainability (so the reasons feel logical), and enough variety in the catalog that the top result isn't always obvious. The system has no understanding of music at all — it just counts matches — but presented in a clean table with reasons, it reads like it does.

**What I would try next:** If I extended this project, I would first add valence to the scoring function since it is already loaded from the CSV and captures whether a song sounds positive or negative — a dimension that mood labels alone miss. Second, I would implement fuzzy genre matching so that "indie pop" scores partial credit against a "pop" preference rather than zero. Third, I would build a simple feedback loop where the user rates the top recommendation and the weights adjust slightly based on their response, turning the static profile into something that learns over a session.
