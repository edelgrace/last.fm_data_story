import lyricsgenius as genius
import argparse
import json

def getSongInfo(song):
  data = json.loads(song)

  title = data["Song_Title"]
  artist = data["Artist"]

  return title, artist

def getLyrics(filename, token):
  song_list = []

  # initialize api
  api = genius.Genius(token)

  # open the file
  file = open(filename, mode='r')
  contents = file.read()
  songs = contents.split("\n")
  
  # create a new file
  old_filename = filename.split(".csv")
  new_filename = old_filename[0] + "_lyrics.csv"
  new_file = open(new_filename, mode='a')

  # loop through each song
  for song in songs:
    title, artist = getSongInfo(song)

    if (title, artist) in song_list:
      continue

    song_list.append((title, artist))

    result = api.search_song(title, artist)
    
    if not result is None:
      lyrics = result.lyrics
      lyrics = lyrics.replace("\n","\\")

      new_line = title + "\t" + artist + "\t\"" + lyrics + "\"\n"

    else:
      new_line = title + "\t" + artist + "\t\n"

    new_file.write(new_line)

  return


def parseArgs():
  parser = argparse.ArgumentParser()

  parser.add_argument('token')
  parser.add_argument('file')

  args = parser.parse_args()

  return args

# main function
def main():
  
  args = parseArgs()

  getLyrics(args.file, args.token)

  return

main()