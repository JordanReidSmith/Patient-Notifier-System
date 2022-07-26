#function that does initial handling on raw line string
def parseLine(file, line, titles, depth):
    line = line.strip()
    skip = False
    #if line is empty, skip handling
    if line == "":
        skip = True
        
    if skip == False:
        #get first character of line to find handling method
        firstChar = line[0]
        match firstChar:
            #if it's an object open, increase depth continue on
            case "{":
                depth = depth + 1
            #if it's an object closer, decrease depth continue on
            case "}":
                #if this is the final depth, end of file reached, end recursion
                if depth == 1:
                    return
                #print line to seperate objects
                print("-"*45)
                depth = depth - 1
            #if line represents end of list, remove last list titles
            case "]":
                titles.pop()
            #if line begins with a string, it's a key/value pair, continue on processing
            case "\"":
                processLine(file, line, titles, depth)
                #return
    #go next line
    parseLine(file, file.readline(), titles, depth)

#fuction used to for detailed processing of key/value pairs and list starts
def processLine(file, line, titles, depth):
    #remove trailing commas
    if line[-1] == ",":
        line = line[0:-1]
    #split the key/value or name/list begin then clean strings
    value = line.split(":")
    value[0] = value[0].strip().replace("\"", "")
    value[1] = value[1].strip().replace("\"", "")
    match value[1].isnumeric():
        #if the value of the pair is a number then multiply the value by 10 before printing
        case True:
            print(" - ".join(titles) + " - " + value[0] + ": " + str(float(value[1])*10).rstrip("0").rstrip("."))
        #if the value of the pair is not a number
        case False:
            #check for beginning of list, if yes append it's key to titles
            if value[1] == "[":
                titles.append(value[0])
            #otherwise print the key/value pair as a string
            else:
                print(" - ".join(titles) + " - " + value[0] + ": " + value[1])

#def processLine(file, line, titles, depth):
#    if line[-1] == ",":
#        line = line[0:-1]
#    value = line[-1]
#    match value:
#        case "[":
#            titles.append(line.split("\"")[1])
#        case "\"":
#            print(" - ".join(titles) + " - " + line.split("\"")[1] + ": " + line.split("\"")[3])
#
#    parseLine(file, file.readline(), titles, depth)

file = open("sample file.json", "r")
firstLine = file.readline() 
parseLine(file, firstLine, [], 0)