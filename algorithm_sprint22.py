from sklearn.cluster import KMeans
import numpy as np

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

# Sample user profiles with 5 favorite songs, 5 favorite artists, and 5 favorite genres as lists
user1 = User(1, "John", "Doe", ["Song1", "Song2", "Song3", "Song4", "Song5"],
             ["Artist1", "Artist2", "Artist3", "Artist4", "Artist5"],
             ["Genre1", "Genre2", "Genre3", "Genre4", "Genre5"])
user2 = User(2, "Jane", "Smith", ["Song1", "Song3", "Song6", "Song7", "Song8"],
             ["Artist2", "Artist3", "Artist6", "Artist7", "Artist8"],
             ["Genre2", "Genre3", "Genre6", "Genre7", "Genre8"])
user3 = User(3, "Alice", "Johnson", ["Song2", "Song4", "Song9", "Song10", "Song11"],
             ["Artist1", "Artist4", "Artist9", "Artist10", "Artist11"],
             ["Genre1", "Genre4", "Genre9", "Genre10", "Genre11"])
user4 = User(4, "Bob", "Brown", ["Song3", "Song5", "Song12", "Song13", "Song14"],
             ["Artist3", "Artist5", "Artist12", "Artist13", "Artist14"],
             ["Genre3", "Genre5", "Genre12", "Genre13", "Genre14"])

user_list = [user1, user2, user3, user4]

# Perform clustering with 3-4 clusters
num_clusters = 3  # You can adjust the number of clusters based on your needs (e.g., 3 or 4)
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
