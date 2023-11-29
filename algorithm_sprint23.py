from sklearn.cluster import KMeans
import numpy as np
import random

class User:
    def __init__(self, user_id, first_name, last_name, fav_songs, fav_artists, fav_genres):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.fav_songs = fav_songs
        self.fav_artists = fav_artists
        self.fav_genres = fav_genres
        self.matches = []


def create_feature_vector(users):
    features = []
    for user in users:
        feature_vector = [len(user.fav_songs), len(user.fav_artists), len(user.fav_genres)]
        features.append(feature_vector)
    return np.array(features)

def clustering(users, num_clusters=2):
    feature_matrix = create_feature_vector(users)
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    kmeans.fit(feature_matrix)
    labels = kmeans.labels_

    clusters = {}
    for i, user in enumerate(users):
        cluster_label = labels[i]
        if cluster_label not in clusters:
            clusters[cluster_label] = []
        clusters[cluster_label].append(user)

    return clusters

def find_matches_in_cluster(user, cluster):
    for potential_match in cluster:
        if user != potential_match:  # Avoid matching with oneself
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

# Perform clustering with 3 clusters
num_clusters = 3  # You can adjust the number of clusters based on your needs
clusters = clustering(user_list, num_clusters)

# Find matches within each cluster
for cluster_id, users_in_cluster in clusters.items():
    for user in users_in_cluster:
        find_matches_in_cluster(user, users_in_cluster)

# Print matches for each user
for user in user_list:
    print(f"{user.first_name} {user.last_name} Matches:")
    for match in user.matches:
        print(f"  - {match.first_name} {match.last_name}")
    print()
