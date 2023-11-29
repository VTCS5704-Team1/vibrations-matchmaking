class User:
    def __init__(self, user_id, first_name, last_name, fav_songs, fav_artists, fav_genres):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.fav_songs = fav_songs
        self.fav_artists = fav_artists
        self.fav_genres = fav_genres
        self.matches = []

def calculate_match_score(user1, user2):
    score = 0

    # Check common songs and update the score
    score += sum(1 for song in user1.fav_songs if song in user2.fav_songs)

    # Check common artists and update the score
    score += sum(1 for artist in user1.fav_artists if artist in user2.fav_artists)

    # Check common genres and update the score
    score += sum(1 for genre in user1.fav_genres if genre in user2.fav_genres)

    return score

def find_matches(user, user_list):
    for potential_match in user_list:
        if user != potential_match:  # Avoid matching with oneself
            match_score = calculate_match_score(user, potential_match)
            if match_score >=5:  # Adjust the threshold as needed
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

# Find matches for each user
for user in user_list:
    find_matches(user, user_list)

# Print matches for each user
for user in user_list:
    print(f"{user.first_name} {user.last_name} Matches:")
    for match in user.matches:
        print(f"  - {match.first_name} {match.last_name}")
    print()
