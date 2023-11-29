import random
from math import radians, sin, cos, sqrt, atan2

class User:
    def __init__(self, user_id, first_name, last_name, fav_songs, fav_artists, fav_genres, latitude, longitude, distance):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.fav_songs = fav_songs
        self.fav_artists = fav_artists
        self.fav_genres = fav_genres
        self.latitude = latitude
        self.longitude = longitude
        self.distance = distance
        self.matches = []

def calculate_match_score(user1, user2):
    score = 0
    s=1.6
    a=1.2
    g=0.8
    # Check common songs and update the score
    score += sum(s for song in user1.fav_songs if song in user2.fav_songs)
    # Check common artists and update the score
    score += sum(a for artist in user1.fav_artists if artist in user2.fav_artists)
    # Check common genres and update the score
    score += sum(g for genre in user1.fav_genres if genre in user2.fav_genres)
    return score


def calculate_distance(user1, user2):
    # Haversine formula to calculate the distance between two points on the Earth's surface
    R = 6371  # Earth radius in kilometers
    lat1, lon1 = radians(user1.latitude), radians(user1.longitude)
    lat2, lon2 = radians(user2.latitude), radians(user2.longitude)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance


def find_matches(user, user_list, max_distance,min_score):
    for potential_match in user_list:
        if user != potential_match:  # Avoid matching with oneself
            match_score = calculate_match_score(user, potential_match)
            # print(user, " ", match_score)
            distance = calculate_distance(user, potential_match)
            if match_score >= min_score and distance <= max_distance:
                user.matches.append(potential_match)

# Sample user profiles with latitude and longitude
user1 = User(1, "John", "Doe", ["Song1", "Song2", "Song3", "Song4", "Song5"],
             ["Artist1", "Artist2", "Artist3", "Artist4", "Artist5"],
             ["Genre1", "Genre2", "Genre3", "Genre4", "Genre5"],
             34.0522, -118.2437,3000)  # Los Angeles, CA
user2 = User(2, "Jane", "Smith", ["Song1", "Song3", "Song6", "Song7", "Song8"],
             ["Artist2", "Artist3", "Artist6", "Artist7", "Artist8"],
             ["Genre2", "Genre3", "Genre6", "Genre7", "Genre8"],
             40.7128, -74.0060,2500)  # New York, NY
user3 = User(3, "Alice", "Johnson", ["Song2", "Song4", "Song9", "Song10", "Song11"],
             ["Artist1", "Artist4", "Artist9", "Artist10", "Artist11"],
             ["Genre1", "Genre4", "Genre9", "Genre10", "Genre11"],
             41.8781, -87.6298,4500)  # Chicago, IL
user4 = User(4, "Bob", "Brown", ["Song3", "Song5", "Song12", "Song13", "Song14"],
             ["Artist3", "Artist5", "Artist12", "Artist13", "Artist14"],
             ["Genre3", "Genre5", "Genre12", "Genre13", "Genre14"],
             29.7604, -95.3698,3200)  # Houston, TX

user_list = [user1, user2, user3, user4]
# Find matches for each user with a maximum distance of max_distance kilometers
for user in user_list:
    find_matches(user, user_list,max_distance=3000,min_score=5) #Adjust min_score for the result
# Print matches for each user
for user in user_list:
    print(f"{user.first_name} {user.last_name} Matches:")
    for match in user.matches:
        print(f"  - {match.first_name} {match.last_name}")
    print()