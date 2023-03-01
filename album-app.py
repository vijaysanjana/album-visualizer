import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError


# Get the username from terminal
username = input("Enter your username: ")
scope = 'user-read-private user-read-playback-state user-modify-playback-state'



# User ID: sanj132

# Erase cache and prompt for user permission
try:
    token = util.prompt_for_user_token(username,scope,client_id='5ab1a4b0b6194c9abbe0fe9b995ea348',client_secret='cff8d33c2f694b0c914257fc6c80bf8f',redirect_uri='http://google.com/')
except:
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username,scope,client_id='5ab1a4b0b6194c9abbe0fe9b995ea348',client_secret='cff8d33c2f694b0c914257fc6c80bf8f',redirect_uri='http://google.com/')

# Create spotifyObject
spotifyObject = spotipy.Spotify(auth=token)

user = spotifyObject.current_user()

displayName = user['display_name']
followers = user['followers']['total']

while True:

    print()
    print(">>> Hi " + displayName + "!")
    print(">>> Welcome to the Spotipy Album Visualizer, where you can find the album cover art for your favorite songs!")
    print(">>> A quick update for your account: You have " + str(followers) + " followers.")
    print()
    print(">>> What would you like to do?")
    print("0 - Search for an artist")
    print("1 - exit")
    print()
    choice = input("Your choice: ")

    #Search for artist
    if choice == "0":
        print()
        searchQuery = input("Ok, what's their name?: ")
        print()


        # Retrieve search results
        searchResults = spotifyObject.search(searchQuery,1,0,"artist")

        artist = searchResults['artists']['items'][0]
        print(artist['name'])
        print(str(artist['followers']['total']) + " followers")
        print(artist['genres'][0])
        print()
        webbrowser.open(artist['images'][0]['url'])
        artistID = artist['id']

        # Album details
        trackURIs = []
        trackArt = []
        z = 0

        # Extract album data
        albumResults = spotifyObject.artist_albums(artistID)
        albumResults = albumResults['items']

        for item in albumResults:
            print("ALBUM " + item['name'])
            albumID = item['id']
            albumArt = item['images'][0]["url"]

            # Extract track data
            trackResults = spotifyObject.album_tracks(albumID)
            trackResults = trackResults['items']

            for item in trackResults:
                print(str(z) + ": " + item['name'])
                trackURIs.append(item['uri'])
                trackArt.append(albumArt)
                z+=1
            print()

        # View album art
        while True:
            songSelection = input("Enter a song number to see the album art (or hit x to go back to the main menu): ")
            if songSelection == "x":
                break
            webbrowser.open(trackArt[int(songSelection)])
            
    # End the program       
    if choice == "1":
        print("Goodbye!")
        break



# print(json.dumps(VARIABLE, sort_keys=True, indent=4))
