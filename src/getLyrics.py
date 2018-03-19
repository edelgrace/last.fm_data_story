import lyricsgenius as genius
import argparse

def getSongInfo(song):
  data = song.strip().split("\t")

  title = data[1]
  artist = data[2]

  return title, artist

def getLyrics(filename, token):
  try:

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

    new_contents = ""

    # loop through each song
    for song in songs:
      title, artist = getSongInfo(song)
  
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