from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import random
from sklearn.preprocessing import OneHotEncoder, StandardScaler, LabelEncoder

class User:
    def __init__(self, user_id, first_name, last_name, fav_songs, fav_artists, fav_genres):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.fav_songs = fav_songs
        self.fav_artists = fav_artists
        self.fav_genres = fav_genres
        self.matches = []

def create_feature_matrix(users):
    features = []
    for user in users:
        user_features = [
            user.user_id, user.first_name, user.last_name,
            *user.fav_songs, *user.fav_artists, *user.fav_genres
        ]
        features.append(user_features)

    # Convert features to NumPy array
    features = np.array(features)

    # Label encode categorical features
    label_encoder = LabelEncoder()
    features[:, 1] = label_encoder.fit_transform(features[:, 1])
    features[:, 2] = label_encoder.fit_transform(features[:, 2])

    # Identify numerical and non-numerical columns
    numerical_cols = [0, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    non_numerical_cols = [1, 2]

    # Normalize numerical features
    scaler = StandardScaler()
    numerical_features = features[:, numerical_cols]
    numerical_features_normalized = scaler.fit_transform(numerical_features)

    # Combine label encoded and normalized features
    feature_matrix = np.concatenate((numerical_features_normalized, features[:, non_numerical_cols]), axis=1)

    return feature_matrix

def calculate_cosine_similarity(user1, user2):
    feature_matrix = np.vstack([user1, user2])
    similarity_matrix = cosine_similarity(feature_matrix)
    return similarity_matrix[0, 1]

def find_matches_using_cosine_similarity(user, user_list, threshold=0.5):
    user_features = create_feature_matrix([user])[0]
    for potential_match in user_list:
        if user != potential_match:  # Avoid matching with oneself
            potential_match_features = create_feature_matrix([potential_match])[0]
            similarity_score = calculate_cosine_similarity(user_features, potential_match_features)
            if similarity_score >= threshold:
                user.matches.append(potential_match)

# Generate larger sample data
def generate_sample_data(num_users, num_songs, num_artists, num_genres):
    sample_data = []
    for i in range(1, num_users + 1):
        first_name = f"User{i}"
        last_name = "Smith"
        fav_songs = random.sample([f"Song{j}" for j in range(1, num_songs + 1)], 5)
        fav_artists = random.sample([f"Artist{j}" for j in range(1, num_artists + 1)], 5)
        fav_genres = random.sample([f"Genre{j}" for j in range(1, num_genres + 1)], 5)

        user = User(i, first_name, last_name, fav_songs, fav_artists, fav_genres)
        sample_data.append(user)
    return sample_data

# Larger sample data with 15 users, 5 songs, 5 artists, and 5 genres
user_list = generate_sample_data(num_users=15, num_songs=5, num_artists=5, num_genres=5)

# Calculate cosine similarity and find matches
feature_matrix = create_feature_matrix(user_list)

for i, user in enumerate(user_list):
    find_matches_using_cosine_similarity(user, user_list, threshold=0.5)

# Print matches for each user
for user in user_list:
    print(f"{user.first_name} {user.last_name} Matches:")
    for match in user.matches:
        print(f"  - {match.first_name} {match.last_name}")
    print()
