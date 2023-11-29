import random
from math import radians, sin, cos, sqrt, atan2

class User:
    def __init__(self, user_id, first_name, last_name, profile_picture_link, email, phone_no, fav_songs, fav_artists, fav_genres, latitude, longitude, max_dist):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.profile_picture_link = profile_picture_link
        self.email = email
        self.phone_no = phone_no
        self.fav_songs = fav_songs
        self.fav_artists = fav_artists
        self.fav_genres = fav_genres
        self.latitude = latitude
        self.longitude = longitude
        self.max_dist = max_dist
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

def calculate_average(user1,user2):
    maximum_d = (user1.max_dist+user2.max_dist)/2
    return maximum_d

def find_matches(user, user_list,min_score):
    for potential_match in user_list:
        if user != potential_match:  # Avoid matching with oneself
            match_score = calculate_match_score(user, potential_match)
            max_distance = calculate_average(user,potential_match)
            # print(user, " ", match_score)
            distance = calculate_distance(user, potential_match)
            if match_score >= min_score and distance <= max_distance:
                user.matches.append(potential_match)

def generate_user_profiles(num_profiles):
    user_profiles = []

    for i in range(1, num_profiles + 1):
        user_id = i
        first_name = f"User{i}"
        last_name = f"LastName{i}"
        profile_picture_link = f"https://example.com/profile_picture{i}.jpg"
        email = f"user{i}@example.com"
        phone_no = f"+123456789{i}"
        fav_songs = [f"Song{j}" for j in range(1, 6)]
        fav_artists = [f"Artist{j}" for j in range(1, 6)]
        fav_genres = [f"Genre{j}" for j in range(1, 6)]
        latitude = random.uniform(-90, 90)
        longitude = random.uniform(-180, 180)
        max_dist = random.uniform(2000, 5000)

        user = User(user_id, first_name, last_name, profile_picture_link, email, phone_no, fav_songs, fav_artists, fav_genres, latitude, longitude, max_dist)
        user_profiles.append(user)

    return user_profiles

# Place the Data here
user_list = generate_user_profiles(100)


for user in user_list:
    find_matches(user, user_list,min_score=5) #Adjust min_score for the result
# Print matches for each user
for user in user_list:
    print(f"{user.first_name} {user.last_name} Matches:")
    for match in user.matches:
        print(f"  - {match.first_name} {match.last_name}")
    print()