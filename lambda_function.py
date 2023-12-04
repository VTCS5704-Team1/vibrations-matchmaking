import os
import psycopg2
from math import radians, sin, cos, sqrt, atan2
import json

# host: deb-vib-db-postgres.cdgaxjglrdw7.us-east-2.rds.amazonaws.com
# port: 5432
# name:postgres
# username=davidfc
# password=VirginiaTechRocks!

# PostgreSQL Connection Details
DB_HOST = os.environ.get("DB_HOST", "deb-vib-db-postgres.cdgaxjglrdw7.us-east-2.rds.amazonaws.com")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_NAME = os.environ.get("DB_NAME", "postgres")
DB_USER = os.environ.get("DB_USER", "davidfc")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "VirginiaTechRocks!")


# User Rows:
# id: int (PK)
# first_name: String
# last_name: String
# bio: String
# email: String
# phone_number: bigint
# fav_song: String[]
# fav_artist: String []
# max_distance: double
# latitude: double
# longitude: double
# gender: String
# matches: String

class User:
    def __init__(self, id, first_name, last_name, bio, email, phone_number, fav_song, fav_artist, max_distance,
                 latitude, longitude, gender, matches):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.bio = bio
        self.email = email
        self.phone_number = phone_number
        self.fav_song = fav_song
        self.fav_artist = fav_artist
        self.max_distance = max_distance
        self.latitude = latitude
        self.longitude = longitude
        self.gender = gender
        self.matches = []


def calculate_match_score(user1, user2):
    score = 0
    s = 1.6
    a = 1.2
    # Check common songs and update the score
    score += sum(s for song in user1.fav_song if song in user2.fav_song)
    # Check common artists and update the score
    score += sum(a for artist in user1.fav_artist if artist in user2.fav_artist)
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


def calculate_average(user1, user2):
    maximum_d = (user1.max_distance + user2.max_distance) / 2
    return maximum_d


def find_matches(user, user_list, min_score):
    for potential_match in user_list:
        if user != potential_match:  # Avoid matching with oneself
            match_score = calculate_match_score(user, potential_match)
            max_distance = calculate_average(user, potential_match)
            distance = calculate_distance(user, potential_match)
            if match_score >= min_score and distance <= max_distance:
                # if match_score >= min_score:
                if user.matches is not None:
                    user.matches.append(potential_match)


def get_user_profiles_from_db():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM vibrations_backend.users")  # Adjust the SQL query based on your schema
    rows = cursor.fetchall()

    user_profiles = []
    for row in rows:
        user_profiles.append(User(*row))  # Assuming your database schema matches the User class

    cursor.close()
    conn.close()

    return user_profiles


def lambda_handler(event, context):
    try:
        # Parse the JSON input from the request body
        request_body = json.loads(event['body'])

        # Access the 'email' property from the JSON input
        email = request_body.get('email')

        # Print the email (or perform any other logic)
        print('Received email:', email)

        # Return a response
        response = {
            'statusCode': 200,
            'body': json.dumps({'message': 'Email processed successfully'})
        }
    except Exception as e:
        # Handle any errors, such as invalid JSON or missing email parameter
        print('Error processing email:', str(e))

        # Return an error response
        response = {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid JSON or missing email parameter'})
        }

    print(response)
    # Fetch user profiles from the database
    user_list = get_user_profiles_from_db()

    for user in user_list:
        find_matches(user, user_list, min_score=1)  # Adjust min_score for the result

    # Print matches for each user
    for user in user_list:
        print(f"{user.first_name} {user.last_name} Matches:")
        print(user.matches)
        print("dfdfsdf")
        if user.matches != None:
            for match in user.matches:
                print(f"  - {match.first_name} {match.last_name}")
            print()

    # Generate JSON:
    matches = dict()

    for user in user_list:
        matches[user.email] = []
        if user.matches != None:
            for match in user.matches[:5]:
                matches[user.email].append(match.email)
                matches[user.email].append(match.phone_number)

    print(matches)

    return {
        'statusCode': 200,
        'statusMessage': 'Matches were succesfully generated',
        'body': matches
    }
