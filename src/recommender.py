from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        scored = []
        for song in self.songs:
            score = 0.0
            
            if song.genre == user.favorite_genre:
                score += 2.0
            
            if song.mood == user.favorite_mood:
                score += 1.0
            
            energy_diff = abs(song.energy - user.target_energy)
            energy_points = 1.5 * (1 - energy_diff)
            score += energy_points
            
            # Optional: acoustic preference
            if user.likes_acoustic:
                score += song.acousticness * 0.5  # small bonus
            
            scored.append((song, score))
        
        # Sort by score descending
        scored.sort(key=lambda x: x[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        reasons = []
        
        if song.genre == user.favorite_genre:
            reasons.append("genre match (+2.0)")
        
        if song.mood == user.favorite_mood:
            reasons.append("mood match (+1.0)")
        
        energy_diff = abs(song.energy - user.target_energy)
        energy_points = 1.5 * (1 - energy_diff)
        reasons.append(f"energy closeness (+{energy_points:.1f})")
        
        if user.likes_acoustic and song.acousticness > 0.5:
            reasons.append("acoustic preference")
        
        return "This song " + ", ".join(reasons) + "."

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and return a list of dicts with numeric fields cast to float/int."""
    import csv
    songs = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            song = {
                'id': int(row['id']),
                'title': row['title'],
                'artist': row['artist'],
                'genre': row['genre'],
                'mood': row['mood'],
                'energy': float(row['energy']),
                'tempo_bpm': float(row['tempo_bpm']),
                'valence': float(row['valence']),
                'danceability': float(row['danceability']),
                'acousticness': float(row['acousticness'])
            }
            songs.append(song)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a single song against user preferences; returns (total_score, list_of_reason_strings)."""
    score = 0.0
    reasons = []
    
    if song['genre'] == user_prefs['genre']:
        score += 2.0
        reasons.append("genre match (+2.0)")
    
    if song['mood'] == user_prefs['mood']:
        score += 1.0
        reasons.append("mood match (+1.0)")
    
    energy_diff = abs(song['energy'] - user_prefs['energy'])
    energy_points = 1.5 * (1 - energy_diff)
    score += energy_points
    reasons.append(f"energy closeness (+{energy_points:.1f})")
    
    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song in the catalog and return the top-k results sorted from highest to lowest score."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = ", ".join(reasons)
        scored.append((song, score, explanation))
    
    # Sort by score descending (highest to lowest)
    scored = sorted(scored, key=lambda x: x[1], reverse=True)
    return scored[:k]
