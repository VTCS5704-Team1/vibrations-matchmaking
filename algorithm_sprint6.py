class User:
    def __init__(self, user_id, first_name, last_name, fav_song, fav_artist, fav_genre):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.fav_song = fav_song
        self.fav_artist = fav_artist
        self.fav_genre = fav_genre
        self.matches = []

def calculate_match_score(user1, user2):
    score = 0

    # Check common songs and update the score
    score += sum(1 for song in user1.fav_song if song in user2.fav_song)

    # Check common artists and update the score
    score += sum(1 for artist in user1.fav_artist if artist in user2.fav_artist)

    # Check common genres and update the score
    score += sum(1 for genre in user1.fav_genre if genre in user2.fav_genre)

    return score

def find_matches(user, user_list):
    for potential_match in user_list:
        if user != potential_match:  # Avoid matching with oneself
            match_score = calculate_match_score(user, potential_match)
            if match_score >= 4:  # Adjust the threshold as needed
                user.matches.append(potential_match)

# Sample user profiles with favorite songs, artists, and genres as lists
user1 = User(1, "John", "Doe", ["Song1", "Song2"], ["Artist1", "Artist2"], ["Genre1", "Genre2"])
user2 = User(2, "Jane", "Smith", ["Song1", "Song3"], ["Artist2", "Artist3"], ["Genre2", "Genre3"])
user3 = User(3, "Alice", "Johnson", ["Song1", "Song3"], ["Artist2", "Artist3"], ["Genre1", "Genre4"])
user4 = User(4, "Bob", "Brown", ["Song3", "Song4"], ["Artist3", "Artist4"], ["Genre3", "Genre4"])

user_list = [user1, user2, user3, user4]

# Find matches for each user
for user in user_list:
    find_matches(user, user_list)

# Print matches for each user
for user in user_list:
    print(f"{user.first_name} {user.last_name} Matches:")
    for match in user.matches:
        print(f"  - {match.first_name} {match.last_name}")
    print()
