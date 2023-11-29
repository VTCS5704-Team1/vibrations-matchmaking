from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from geopy.distance import geodesic  # Install geopy using: pip install geopy

class User:
    def __init__(self, user_id, first_name, last_name, fav_songs, fav_artists, fav_genres, latitude, longitude):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.fav_songs = fav_songs
        self.fav_artists = fav_artists
        self.fav_genres = fav_genres
        self.latitude = latitude
        self.longitude = longitude
        self.matches = []

def calculate_similarity(user1, user2):
    doc1 = " ".join(user1.fav_songs + user1.fav_artists + user1.fav_genres)
    doc2 = " ".join(user2.fav_songs + user2.fav_artists + user2.fav_genres)
    vectorizer = CountVectorizer().fit_transform([doc1, doc2])
    similarity = cosine_similarity(vectorizer)
    return similarity[0, 1]

def calculate_distance(user1, user2):
    coords1 = (user1.latitude, user1.longitude)
    coords2 = (user2.latitude, user2.longitude)
    return geodesic(coords1, coords2).kilometers

def find_matches_with_distance(user, user_list, threshold_similarity, threshold_distance):
    for potential_match in user_list:
        if user != potential_match:
            similarity_score = calculate_similarity(user, potential_match)
            distance = calculate_distance(user, potential_match)
            if similarity_score >= threshold_similarity and distance <= threshold_distance:
                user.matches.append(potential_match)

# Sample user profiles with latitude and longitude
user1 = User(1, "John", "Doe", ["Song1", "Song2", "Song3", "Song4", "Song5"],
             ["Artist1", "Artist2", "Artist3", "Artist4", "Artist5"],
             ["Genre1", "Genre2", "Genre3", "Genre4", "Genre5"], 40.7128, -74.0060)
user2 = User(2, "Jane", "Smith", ["Song1", "Song3", "Song6", "Song7", "Song8"],
             ["Artist2", "Artist3", "Artist6", "Artist7", "Artist8"],
             ["Genre2", "Genre3", "Genre6", "Genre7", "Genre8"], 34.0522, -118.2437)
user3 = User(3, "Alice", "Johnson", ["Song2", "Song4", "Song9", "Song10", "Song11"],
             ["Artist1", "Artist4", "Artist9", "Artist10", "Artist11"],
             ["Genre1", "Genre4", "Genre9", "Genre10", "Genre11"], 41.8781, -87.6298)
user4 = User(4, "Bob", "Brown", ["Song3", "Song5", "Song12", "Song13", "Song14"],
             ["Artist3", "Artist5", "Artist12", "Artist13", "Artist14"],
             ["Genre3", "Genre5", "Genre12", "Genre13", "Genre14"], 30.2500, -97.7500)

user_list = [user1, user2, user3, user4]

# Find matches for each user considering both similarity and distance
for user in user_list:
    find_matches_with_distance(user, user_list, threshold_similarity=0.2, threshold_distance=5000.0)  # Adjust thresholds as needed

# Print matches for each user
for user in user_list:
    print(f"{user.first_name} {user.last_name} Matches:")
    for match in user.matches:
        print(f"  - {match.first_name} {match.last_name}")
    print()
