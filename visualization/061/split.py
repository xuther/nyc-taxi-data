with open('./heirarchical-clusters.csv', 'r') as f:
    for line in f:
       stuff = line.split("|")
       name = stuff[0].strip()
       lines = stuff[1].replace("'", "").replace("[", "").strip().replace("]}", "").replace("{","").split("],")
       with open('./clusters/' + name, "w+") as outFile:
           for line in lines:
               outFile.write(line.split(":")[1].strip() + "\n")

