from datetime import datetime
import argparse
import sys

def parse_csv(filename):
  content = ""

  with open(filename) as file:
    content = file.read()

  content = content.split("\n")

  for line in content:
    line = line.split("\t")
    date = line[0]

    try:
      new_date = datetime.fromtimestamp(float(int(date)))
      new_date = new_date.strftime('%Y-%m-%d %H:%M:%S')
      print(new_date + "\t" + line[1] + "\t" + line[2])

    except Exception as error:
      sys.stderr.write(date)
    except IndexError as err:
      sys.stderr.write(str(len(line)))
      
parser = argparse.ArgumentParser()
parser.add_argument('filename')
args = parser.parse_args()

parse_csv(args.filename)