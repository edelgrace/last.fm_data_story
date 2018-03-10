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

  except Exception as e:
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
  artist_list = {}

  # open the last.fm dataset
  file = open("../data/edelgrace.csv", mode="r", encoding="utf8")

  # load the contents
  content = file.read()
  content = content.split("\n")

  # go through each line
  for line in content:
    tags = ""

    # split the line
    data = line.strip().split("\t")

    # check how many params
    if len(data) <= 2:
      print("NOT FOUND\t" + data[0])

      continue

    timestamp = data[0]
    song = data[1]
    artist = data[2]

    try:
      album = data[3]
    except Exception as e:
      album = ""

    mbid = data[-1]

    if mbid == album or mbid == artist:
      print("NO MBID\t" + timestamp + "\t" + song + "\t" + artist + "\t" + album)
      continue

    # check if in artist list
    if artist in artist_list:
      if "toptags" in artist_list[artist][0]:
        tag_list = artist_list[artist][0]["toptags"]["tag"]    

        for tag in tag_list:
          tags += tag["name"] + ","

        tags = tags.strip(",")

      if "gender" in artist_list[artist][1]:
        gender = str(artist_list[artist][1]["gender"])
      
      if "country" in artist_list[artist][1]:
        country = str(artist_list[artist][1]["country"])

      if "type" in artist_list[artist][1]:
        artist_type = str(artist_list[artist][1]["type"])

      print("FOUND\t" + timestamp + "\t" + song + "\t" + artist + "\t" + album + "\t" + gender + "\t" + country + "\t" + artist_type + "\t" + tags) 
      continue

    # get the artist info
    artist_info = get_artist(mbid)

    tags = ""
    gender = ""
    country = ""
    artist_type = ""

    if "toptags" in artist_info[0]:
      tag_list = artist_info[0]["toptags"]["tag"]    

      for tag in tag_list:
        tags += tag["name"] + ","

      tags = tags.strip(",")

    if "gender" in artist_info[1]:
      gender = str(artist_info[1]["gender"])
    
    if "country" in artist_info[1]:
      country = str(artist_info[1]["country"])

    if "type" in artist_info[1]:
      artist_type = str(artist_info[1]["type"])

    print("FOUND\t" + timestamp + "\t" + song + "\t" + artist + "\t" + album + "\t" + gender + "\t" + country + "\t" + artist_type + "\t" + tags) 

    artist_list[artist] = artist_info
      
  return

# run
try:

  main()

except KeyboardInterrupt as e:

  print("=STOPPED=")