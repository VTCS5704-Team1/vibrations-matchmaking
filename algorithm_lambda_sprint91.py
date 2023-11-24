import psycopg2
import random
from math import radians, sin, cos, sqrt, atan2


class User:
    def __init__(self, user_id, first_name, last_name, profile_picture_link, email, phone_no, fav_songs, fav_artists, latitude, longitude, max_dist):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.profile_picture_link = profile_picture_link
        self.email = email
        self.phone_no = phone_no
        self.fav_songs = fav_songs
        self.fav_artists = fav_artists
        self.latitude = latitude
        self.longitude = longitude
        self.max_dist = max_dist
        self.matches = []

def calculate_match_score(user1, user2):
    score = 0
    s=1.6
    a=1.2
    # Check common songs and update the score
    score += sum(s for song in user1.fav_songs if song in user2.fav_songs)
    # Check common artists and update the score
    score += sum(a for artist in user1.fav_artists if artist in user2.fav_artists)
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


# Establish a connection to the PostgreSQL database
def connect_to_db():
    conn = psycopg2.connect(
        dbname='your_db_name',
        user='your_username',
        password='your_password',
        host='your_host',
        port='your_port'
    )
    return conn

# Retrieve user data from the PostgreSQL database
def retrieve_user_data():
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("SELECT user_id, first_name, last_name, profile_picture_link, email, phone_no, fav_songs, fav_artists, latitude, longitude, max_dist FROM users_table")
    rows = cur.fetchall()
    user_profiles = []
    for row in rows:
        user = User(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])
        user_profiles.append(user)
    conn.close()
    return user_profiles

# Main Lambda function to run the algorithm
def lambda_handler(event, context):
    user_list = retrieve_user_data()
    for user in user_list:
        find_matches(user, user_list, min_score=5)  # Adjust min_score for the result
    # Print matches for each user
    for user in user_list:
        print(f"{user.first_name} {user.last_name} Matches:")
        for match in user.matches:
            print(f"  - {match.first_name} {match.last_name}")
        print()