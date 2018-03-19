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
    new_file = open(new_filename, mode='w')

    new_contents = ""

    # loop through each song
    for song in songs:
      title, artist = getSongInfo(song)
  
      result = api.search_song(title, artist)
      
      if not result is None:
        lyrics = result.lyrics
        lyrics = lyrics.replace("\n","\\")

        new_line = title + "\t" + artist + "\t\"" + lyrics + "\"\n"
        new_contents += new_line
  
  except KeyboardInterrupt as e:
    pass
  finally:
    # save the lyrics to file
    new_file.write(new_contents)
    return


def parseArgs():
  parser = argparse.ArgumentParser()

  parser.add_argument('token')

  args = parser.parse_args()

  return args.token

# main function
def main():
  
  token = parseArgs()

  getLyrics("../data/edelgrace.csv", token)

  getLyrics("../data/erzadel.csv", token)

main()