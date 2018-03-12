def parsefile(filename):
  file = open(filename, mode='r')

  contents = file.read()

  contents = contents.split("\n")

  new_filename = filename.split(".csv")

  new_filename = new_filename[0] + "_nodates.csv"

  new_file = open(new_filename, mode="w")

  new_contents = ""

  for line in contents:
    line = line.split("\t")

    line = line[2:]

    line = "\t".join(line)

    line += "\n"

    new_contents += line

  new_file.write(new_contents)

parsefile("../data/scrobbles.csv")
parsefile("../data/scrobbles-erzadel.csv")