# Reflection: Profile Comparisons and Engineering Process

## Profile Pair Comparisons

**Pop vs. Lofi** — These profiles are complete opposites and the results reflect that. Pop/happy (energy=0.8) surfaces upbeat tracks with "Sunrise City" at #1; lofi/chill (energy=0.35) surfaces quiet study tracks with "Library Rain" at #1. All three scoring criteria flipped, so the recommendations flipped entirely. The system worked exactly as designed.

**Rock vs. Adversarial (r&b + sad + energy=0.9)** — Both want high energy and heavy emotion, but the outputs are very different. Rock gets a perfect #1 match ("Storm Runner", 4.48) because the catalog has one song that hits all three criteria. The adversarial r&b profile gets "Velvet Rain" at #1 — a slow ballad with energy=0.38 — because genre and mood together (+3.0 pts) overwhelm the energy penalty. The algorithm did not fail; the catalog just had no high-energy sad r&b track. This is the clearest example of data limiting results.

**Chill Lofi — no diversity vs. diversity ON** — Without diversity, LoRoom appears twice in the top 5 ("Midnight Coding" at #2, "Focus Flow" at #3). With diversity ON, Focus Flow is replaced by "Spacewalk Thoughts" from a different artist. The scores did not change — only the selection rule did. This makes the output feel more like a curated playlist than a sorted list.

**Default weights vs. weight experiment (pop/happy)** — Halving genre (2.0→1.0) and doubling energy (1.5→3.0) dropped "Gym Hero" from #2 to #4 and raised "Rooftop Lights" (indie pop/happy) to #2. One number change shifted the entire philosophy: the default rewards genre loyalty; the experiment rewards how a song actually feels.

---

## Why Does "Gym Hero" Keep Showing Up for Happy Pop Listeners?

"Gym Hero" is tagged as pop, so it earns the full +2.0 genre bonus. It is also tagged "intense" not "happy," which costs it the +1.0 mood point — but the genre bonus is so large that it still outscores every non-pop song, even ones tagged "happy." The system does not listen to music; it adds up points. As long as genre is worth double mood, any pop song beats any non-pop song regardless of how it actually sounds.

---

## Engineering Process

**Biggest learning moment:** Weights are design decisions. Changing genre from 2.0 to 1.0 reshuffled the entire top 5. Every number baked into a scoring system is a claim about what matters most — and engineers at Spotify or YouTube make those same choices at a scale that affects millions of listeners daily.

**How AI tools helped and when I double-checked:** AI was most useful for structure — CSV formatting, library suggestions, explaining `.sort()` vs `sorted()`. I had to verify the energy scoring formula by hand to confirm it rewarded closeness and not just high values. I also caught that an early version of the diversity penalty was too aggressive, which only became visible when I ran it against a real profile.

**What surprised me:** Three rules and 20 songs produced output that genuinely looked like real recommendations. The illusion comes from ranking (only the best appear) and explainability (the reasons feel logical). The system has no understanding of music — it counts matches and adds points — but it reads like it does.

**What I would try next:** Add valence to scoring (already in the CSV, captures positivity vs. negativity beyond mood labels), implement fuzzy genre matching so "indie pop" scores partial credit against "pop", and build a simple session feedback loop where a user rating nudges the weights over time.
