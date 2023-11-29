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

    # Check if favorite song matches
    if user1.fav_song == user2.fav_song:
        score += 1

    # Check if favorite artist matches
    if user1.fav_artist == user2.fav_artist:
        score += 1

    # Check if favorite genre matches
    if user1.fav_genre == user2.fav_genre:
        score += 1

    return score

def find_matches(user, user_list):
    for potential_match in user_list:
        if user != potential_match:  # Avoid matching with oneself
            match_score = calculate_match_score(user, potential_match)
            if match_score >= 2:  # Adjust the threshold as needed
                user.matches.append(potential_match)

# Sample user profiles
user1 = User(1, "John", "Doe", "Song1", "Artist1", "Genre1")
user2 = User(2, "Jane", "Smith", "Song1", "Artist2", "Genre2")
user3 = User(3, "Alice", "Johnson", "Song2", "Artist1", "Genre1")
user4 = User(4, "Bob", "Brown", "Song3", "Artist3", "Genre3")

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