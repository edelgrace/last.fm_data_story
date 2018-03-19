import sys
import json 
import time
import hashlib
import requests
from time import sleep

secret = "3b939f3508874176265c1b7d62974984"

# send a request to the musicbrainz database
def mb_request(url):
  request = requests.get(url)
  result = None

  try:
    result = json.loads(request.text)

  except Exception:
    print(request.text)
    
  return result

# get the artist
def get_artist_mbinfo(result):

  return result

# get the artist information
def get_artist(artist):
  result = []

  url = "http://ws.audioscrobbler.com/2.0/"
  url += "?method=artist.gettoptags"
  url += "&mbid="
  url += artist
  url += "&api_key=4d77e335d92f70180149d4ab6b896d9a"
  url += "&format=json"

  result.append(mb_request(url))

  url = "https://musicbrainz.org/ws/2/artist/"
  url += artist
  url += "?fmt=json"
  
  artist_info = get_artist_mbinfo(mb_request(url))

  result.append(artist_info)

  return result

# main loop
def main():
  artist_list = []

  # open the last.fm dataset
  file = open("../data/all_scrobbles_dates.csv", mode="r", encoding="utf8")

  # load the contents
  content = file.read()
  content = content.split("\n")

  # open a new file
  new_file = open ("../data/artists.csv", mode="a")

  # go through each line
  for line in content[1:]:

    # split the line
    data = line.split("\t")
    
    if len(data) > 1:
      date = data[0]
      song = data[1]
      artist = data[2]
      album = data[3]
      song_mbid = data[4]
      artist_mbid = data[5]
      album_mbid = data[6]

    # check if in artist list
    if artist in artist_list:
      continue

    artist_info = ""

    new_line = ""

    artist_list.append(artist)

    # get the artist info
    if artist_mbid != "":
      artist_info = get_artist(artist_mbid)

      if "error" in artist_info[0] or "error" in artist_info[1]:
        artist_info = ""

    if artist_info != "":
      tags = ""
      gender = artist_info[1]["gender"]
      country = artist_info[1]["country"]
      artist_type = artist_info[1]["type"]

      # tags
      if "toptags" in artist_info[0]:

        for tag in artist_info[0]["toptags"]["tag"]:
          tags += tag["name"] + ","
        
        tags = tags.strip(",")

      gender = gender if gender is not None else ""
      country = country if country is not None else ""
      artist_type = artist_type if artist_type is not None else ""

      new_line = artist + "\t" + gender + "\t"
      new_line += artist_type + "\t"
      new_line += country + "\t"
      new_line += tags + "\n"


    else:
      new_line = artist + "\t\t\t\t\n"
    
    new_file.write(new_line)
    print(new_line)

  new_file.close()
  return

# run
try:

  main()

except KeyboardInterrupt as e:

  print("=STOPPED=")
