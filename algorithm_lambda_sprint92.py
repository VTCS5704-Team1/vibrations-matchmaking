import random
from math import radians, sin, cos, sqrt, atan2
import psycopg2  # Import PostgreSQL driver


class User:
    def __init__(self, user_id, first_name, last_name, profile_picture_link, email, phone_no, fav_songs, fav_artists,
                 latitude, longitude, max_dist):
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
    s = 1.6
    a = 1.2
    score += sum(s for song in user1.fav_songs if song in user2.fav_songs)
    score += sum(a for artist in user1.fav_artists if artist in user2.fav_artists)
    return score


def calculate_distance(user1, user2):
    R = 6371
    lat1, lon1 = radians(user1.latitude), radians(user1.longitude)
    lat2, lon2 = radians(user2.latitude), radians(user2.longitude)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance


def calculate_average(user1, user2):
    maximum_d = (user1.max_dist + user2.max_dist) / 2
    return maximum_d


def create_db_connection():
    # Establish a connection to the PostgreSQL database
    connection = psycopg2.connect(
        host="your_database_host",
        port="your_database_port",
        database="your_database_name",
        user="your_database_user",
        password="your_database_password"
    )
    return connection


def fetch_users_from_db():
    # Establish a connection to the database
    connection = create_db_connection()

    try:
        # Create a cursor
        with connection.cursor() as cursor:
            # Fetch user data from the 'users' table
            cursor.execute("SELECT * FROM users")
            user_data = cursor.fetchall()

        # Convert the fetched data into User objects
        user_list = []
        for data in user_data:
            user = User(*data)
            user_list.append(user)

    finally:
        # Close the database connection
        connection.close()

    return user_list


def find_matches_and_store(user, user_list, min_score):
    # Establish a connection to the database
    connection = create_db_connection()

    try:
        # Create a cursor
        with connection.cursor() as cursor:
            for potential_match in user_list:
                if user != potential_match:
                    match_score = calculate_match_score(user, potential_match)
                    max_distance = calculate_average(user, potential_match)
                    distance = calculate_distance(user, potential_match)

                    # Modify the following lines to store the matches in the database
                    if match_score >= min_score and distance <= max_distance:
                        # Store the match in the database
                        cursor.execute(
                            "INSERT INTO matches (user_id, match_id) VALUES (%s, %s)",
                            (user.user_id, potential_match.user_id)
                        )

        # Commit the changes to the database
        connection.commit()

    finally:
        # Close the database connection
        connection.close()


# Fetch user data from the database
user_list = fetch_users_from_db()

# Call the modified function for each user
for user in user_list:
    find_matches_and_store(user, user_list, min_score=5)
