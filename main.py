import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random
import string

# Spotify API credentials
SPOTIPY_CLIENT_ID = ''
SPOTIPY_CLIENT_SECRET = ''
SPOTIPY_REDIRECT_URI = ''

# Static part of the password
STATIC_PASSWORD = 'static_part_'

# Function to authenticate with Spotify API and get user ID
def authenticate_spotify(username=None):
    try:
        if username is None:
            username = input("Enter your Spotify username: ")

        scope = 'playlist-read-private playlist-read-collaborative playlist-modify-public playlist-modify-private user-read-private user-read-email user-library-read user-library-modify user-follow-read user-follow-modify user-top-read user-read-playback-state user-modify-playback-state user-read-currently-playing user-read-recently-played'

        sp_oauth = SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope=scope, username=username)
        sp = spotipy.Spotify(auth_manager=sp_oauth)

        user_info = sp.current_user()
        user_id = user_info['id']

        return sp, user_id

    except spotipy.SpotifyException as e:
        print(f"Spotify authentication failed: {e}")
        return None, None

# Function to deauthenticate the user
def deauthenticate_spotify(sp_oauth):
    try:
        sp_oauth._remove_token()
        print("User deauthenticated successfully.")

    except Exception as e:
        print(f"Error deauthenticating user: {e}")

# Function to generate a random inconspicuous playlist name
def generate_inconspicuous_playlist_name():
    music_phrases = [
        'Melody Mix', 'Harmony Haven', 'Rhythm Lounge', 'Sonata Selection',
        'Beat Bliss', 'Tune Treasury', 'Audiophile Anthems', 'Chord Chronicles',
        'Playlist 1', 'Music Collection', 'Favorite Songs', 'Mixtape',
        'Study Mix', 'Chill Playlist', 'Relaxing Tunes', 'Background Music',
        'My Playlist', 'Favorite Tracks', 'Background Music', 'Study Session',
        'Relaxing Vibes', 'Chill Out', 'Mood Booster', 'Easy Listening'
    ]
    
    return f'{random.choice(music_phrases)}_{generate_random_word(3)}'

# Function to generate a random word
def generate_random_word(length=8):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

# Function to convert a message to ASCII English alphabets with a password
def message_to_ascii_alphabets(message, password):
    random.seed(password)
    return [chr((ord(char) + random.randint(1, 26)) % 26 + ord('A')) if char != ' ' else ' ' for char in message.upper()]

# Function to convert ASCII English alphabets to characters
def ascii_alphabets_to_message(ascii_alphabets):
    return ''.join(ascii_alphabets)

# Function to embed ASCII English alphabets into playlist description
def embed_ascii_alphabets(sp, playlist_id, ascii_alphabets):
    playlist_description = ''.join(ascii_alphabets)
    try:
        sp.playlist_change_details(playlist_id, description=playlist_description)

    except spotipy.SpotifyException as e:
        print(f"Error embedding ASCII alphabets into playlist description: {e}")

# Function to add random tracks from a random genre to the playlist
def add_random_tracks_to_playlist(sp, playlist_id):
    try:
        genres = sp.recommendation_genre_seeds()['genres']
        random_genre = random.choice(genres)
        recommended_tracks = sp.recommendations(seed_genres=[random_genre], limit=50)['tracks']
        track_uris = [track['uri'] for track in recommended_tracks]
        sp.playlist_add_items(playlist_id, track_uris)

    except spotipy.SpotifyException as e:
        print(f"Error adding random tracks to the playlist: {e}")

# Function to add user's recommended tracks to the playlist in a randomized order
def add_user_recommended_tracks_to_playlist(sp, playlist_id):
    try:
        recommended_tracks = sp.current_user_top_tracks(limit=50)['items']
        track_uris = [track['uri'] for track in recommended_tracks]
        random.shuffle(track_uris)
        sp.playlist_add_items(playlist_id, track_uris)

    except spotipy.SpotifyException as e:
        print(f"Error adding user's recommended tracks to the playlist: {e}")

# Function to encode a message using ASCII English alphabets with a static and user-input part of the password
def encode_ascii_alphabets(sp, message):
    try:
        user_info = sp.current_user()
        user_id = user_info['id']
        user_password = input("Enter the user-input part of the password: ")
        password = STATIC_PASSWORD + user_password
        ascii_alphabets = message_to_ascii_alphabets(message, password)
        playlist_name = generate_inconspicuous_playlist_name()
        playlist = sp.user_playlist_create(user=user_id, name=playlist_name)
        add_user_recommended_tracks_to_playlist(sp, playlist['id'])
        embed_ascii_alphabets(sp, playlist['id'], ascii_alphabets)
        print(f'Message encoded in the inconspicuous playlist named "{playlist_name}" on Spotify with {playlist["tracks"]["total"]} tracks from user\'s recommendations.')

    except Exception as e:
        print(f"Error encoding message: {e}")

# Function to decode a message from a playlist with a static and user-input part of the password
def decode_ascii_alphabets(sp, playlist_id):
    try:

        # Fetch playlist details after getting the password
        playlist_details = sp.playlist(playlist_id)
        playlist_description = playlist_details.get('description', '')
        ascii_alphabets = list(playlist_description)
        decoded_message = ascii_alphabets_to_message(ascii_alphabets)
        print(f'Fetched Message: {decoded_message}')
        return decoded_message

    except Exception as e:
        print(f"Error decoding message: {e}")
        return None


# Function to convert the decoded message back to the encoded message using the password
def convert_decoded_to_encoded(decoded_message):
    try:
        user_password = input("Enter the user-input part of the password: ")
        password = STATIC_PASSWORD + user_password
        random.seed(password)
        encoded_message = [chr((ord(char) - random.randint(1, 26)) % 26 + ord('A')) if char != ' ' else ' ' for char in decoded_message.upper()]
        return ''.join(encoded_message)

    except Exception as e:
        print(f"Error converting decoded message back to encoded message: {e}")
        return None

# Main menu function with user input validation
def main_menu():
    try:
        username = input("Enter your Spotify username: ")
        sp, user_id = authenticate_spotify(username)

        while True:
            print("\nMenu:")
            print("1. Encode a message using ASCII English alphabets")
            print("2. Decode a message from a playlist")
            print("3. Deauthenticate user")
            print("4. Exit")

            try:
                choice = input("Enter your choice (1-4): ")

                if choice == '1':
                    message_to_encode = input("Enter the message to encode: ")
                    encode_ascii_alphabets(sp, message_to_encode)
                elif choice == '2':
                    playlist_id = input("Enter the playlist ID to decode: ")
                    decoded_message = decode_ascii_alphabets(sp, playlist_id)
                    if decoded_message:
                        converted_message = convert_decoded_to_encoded(decoded_message)
                        print(f'Converted message back to the encoded message: {converted_message}')
                elif choice == '3':
                    deauthenticate_spotify(sp._auth)
                    break
                elif choice == '4':
                    break
                else:
                    print("Invalid choice. Please enter a number between 1 and 4.")

            except ValueError:
                print("Invalid input. Please enter a valid number.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Main function with error handling for Spotify authentication
def main():
    try:
        main_menu()

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
