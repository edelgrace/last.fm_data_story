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

    new_line = ""

    try:
      new_date = datetime.fromtimestamp(float(int(date)))
      new_date = new_date.strftime('%Y-%m-%d %H:%M:%S')
      
      new_line += new_date
      new_line += "\t".join(line[1:])

      print(new_line)

    except IndexError:
      sys.stderr.write(str(len(line)))
    except Exception:
      sys.stderr.write(date)
      
parser = argparse.ArgumentParser()
parser.add_argument('filename')
args = parser.parse_args()

parse_csv(args.filename)