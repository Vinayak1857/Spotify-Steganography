# Spotify-Steganography
This Python script combines Spotify API integration with encoding and decoding messages using ASCII English alphabets. It allows users to encode a message into a Spotify playlist's description, decode a message from a playlist, and deauthenticate the user when desired.

## Prerequisites

- Python 3.x
- Spotipy library (`pip install spotipy`)

## Setup

1. **Spotify API Credentials:**
   - Obtain your Spotify API credentials by creating a new application on the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications).
   - Set the following environment variables with your credentials:
     - `SPOTIPY_CLIENT_ID`
     - `SPOTIPY_CLIENT_SECRET`
     - `SPOTIPY_REDIRECT_URI`

2. **Static Password:**
   - Modify the `STATIC_PASSWORD` variable in the script to your desired static password.

3. **Install Dependencies:**
   ```bash
   pip install spotipy

## Usage
   Run the script using the following command:
   
   bash
   Copy code
   python main.py
   Enter your Spotify username and follow the menu options.

## Menu Options
   Encode a Message (Option 1):

   Enter a message to encode, and follow the prompts to create a Spotify playlist with the encoded message.
   Decode a Message (Option 2):

   Enter the playlist ID to decode the message hidden in the playlist's description.
   Deauthenticate User (Option 3):

   Deauthenticate the user from the Spotify API.
   Exit (Option 4):
   
   Exit the program.

## License
   This project is licensed under the [MIT License]([https://github.com](https://opensource.org/license/mit)https://opensource.org/license/mit).
