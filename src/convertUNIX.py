import datetime
import argparse
import sys

def valid_date(date):
  six = datetime.time(6, 0, 0, 0)
  midnight = datetime.time.max

  new_date = datetime.datetime.time(date)
  
  ONT_START = datetime.datetime(2017, 9, 15)
  ONT_END = datetime.datetime(2017, 9, 17)


  if ((new_date > six and new_date < midnight) and
    (date > ONT_END or date < ONT_START)):
    return True
  
  return False


def time_zone(date):
  new_date = date

  # Philippines trips
  MNL_TRIP_1_START = datetime.datetime(2013, 5, 9)
  MNL_TRIP_1_END = datetime.datetime(2013, 5, 29)

  MNL_TRIP_2_START = datetime.datetime(2015, 7, 5)
  MNL_TRIP_2_END = datetime.datetime(2013, 8, 7)

  # Waterloo trips
  ONT_START = datetime.datetime(2017, 9, 15)
  ONT_END = datetime.datetime(2017, 9, 17)

  # if certain date, change to philippines time
  if ((date > MNL_TRIP_1_START and date < MNL_TRIP_1_END) or
      (date > MNL_TRIP_2_START and date < MNL_TRIP_2_END)):
    new_date = date + datetime.timedelta(hours=12)

  # if certain date, change to ontario time
  elif date > ONT_START and date < ONT_END:
    new_date = date + datetime.timedelta(hours=2)

  return new_date

def parse_csv(filename):
  content = ""

  with open(filename) as file:
    content = file.read()

  content = content.split("\n")

  new_file = open("all_scrobbles_dates.csv", mode="a")

  for line in content:
    line = line.split("\t")
    date = line[0]

    new_line = ""

    try:

      new_date = datetime.datetime.fromtimestamp(float(int(date)))

      new_date = time_zone(new_date)

      if not valid_date(new_date):
        continue

      new_date = new_date.strftime('%Y-%m-%d %H:%M:%S')
      
      new_line += new_date + "\t"
      new_line += "\t".join(line[1:]) + "\n"

      print(new_line)

      new_file.write(new_line)

    except IndexError as i:
      print(str(len(line)))
      print(i)
    except Exception as e:
      print(date)
      print(e)
      
parser = argparse.ArgumentParser()
parser.add_argument('filename')
args = parser.parse_args()

parse_csv(args.filename)