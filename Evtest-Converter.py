###################################################################
#####                  Convert EventTest file data
#####                   to an Excel Sheet (.CSV)
###################################################################

import csv, re, datetime, os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
writingPermission = True
iHaveMyFile = False
count = 5
myFileName = ""
listOfTimestamp = []
listOfCodes = []
listOfValues = []
pathIsOk = True
coordinatesOfLayer = []
listIsInPoduction = True
listOfX = []
listOfY = []
loopList = 0
releaseSeparator = "000000"
makingCoordinates = True
cleanDataWithoutTime = []

def resetVar():
  iHaveMyFile = False
  count = 5
  myFileName = ""
  listOfTimestamp = []
  listOfCodes = []
  listOfValues = []
  pathIsOk = True
  coordinatesOfLayer = []
  listIsInPoduction = True

def fileOpenning(filePath):

  # Try to open the file, if it cannot an error is show
  try:
    myFile = open(filePath, "r")
    doesMyFileExist = True
    try:
      fileContent = myFile.read()
    except UnicodeDecodeError:
      doesMyFileExist = False
  except OSError:
    doesMyFileExist = False

  if doesMyFileExist:
    
    #---------------REG-EX PART---------------

    #Delete useless data
    tempPressEvent = re.sub("\(ABS_MT_TRACKING_ID\)..", "", fileContent)
    tempPressEvent = re.sub("\(ABS_MT_.............", "", tempPressEvent)
    tempPressEvent = re.sub("Event code.*", "", tempPressEvent)
    tempPressEvent = re.sub(".*SYN_REPORT.*", "", tempPressEvent)
    #tempPressEvent = re.sub(".*code 58.*", "", tempPressEvent)
    
    #Find relevant data
    pressList = re.findall("Event: time..................|code 57.*|code 53.*|code 54.*|code 47.*|code 58.*", tempPressEvent)

    cleanData = []
    
    for u in pressList:
      u = re.sub("value | alue| time| lue", "", u)
      u = re.sub("code ", "c", u)
      u = re.sub("Event: ", "", u)

      if len(u) > 13:
        u = datetime.datetime.fromtimestamp(float(u)).isoformat()

      cleanData += re.split("\s", u)

  return cleanData

def convertDataToCsv(listOfTimestamp, listOfCodes, listOfValues, listOfX, listOfY):
  # Writing these data to an excel sheet
  with open(outputFilePath, 'w+', newline='') as f:
    print(len(listOfTimestamp), len(listOfCodes), len(listOfValues), len(listOfX), len(listOfY))
    fieldnames = ['FullTime', 'DateHour', 'hour', 'Code', 'Value', 'X', 'Y']
    theWriter = csv.DictWriter(f, fieldnames=fieldnames)

    theWriter.writeheader()

    for time, code, value, x, y in zip(listOfTimestamp, listOfCodes, listOfValues, listOfX, listOfY):
      theWriter.writerow({'FullTime': time, 'Code': code, 'Value': value, 'X': x, 'Y': y})

def getNameOfFile(filePath, count, myFileName):
  iHaveMyFile = False
  # ------ GET THE NAME OF THE FILE ------
  while not(iHaveMyFile):
    try:
      for u in filePath[-count]:
        if u == "\\":
          iHaveMyFile = True
          break

        myFileName += u
        count += 1
    except IndexError:
      pass
      iHaveMyFile = True
  try:
    for i in myFileName[-1]:
      finalFileName = myFileName[::-1]
  except IndexError:
    pass
  finalFileName += ".csv"
  # ------------------------------------

  return finalFileName

def whereToDrawLine(finalListOfData, coordinatesOfLayer):
  xAdded = False
  yAdded = True
  indexChange = False
  oldX = ""
  oldY = ""
  makingListOfCoordinate = True
  loopList = 0    
  stopSpace = False

  while makingListOfCoordinate:
    try:
      # Try to found if its a X position
      if finalListOfData[loopList] == "c53":
        # If its not already added 
        if not(xAdded):
          coordinatesOfLayer.append(finalListOfData[loopList + 1])
          oldX = finalListOfData[loopList + 1]
          xAdded = True
          yAdded = False
        # If it already added
        else:
          coordinatesOfLayer.append(oldY)

          # When duo is complete
          #coordinatesOfLayer.append(oldX)
          #coordinatesOfLayer.append(oldY)

          indexChange = True
          yAdded = True
          xAdded = False
      elif finalListOfData[loopList] == "c54":
        if not(yAdded):

          coordinatesOfLayer.append(finalListOfData[loopList + 1])

          # When duo is complete
          coordinatesOfLayer.append(oldX)
          coordinatesOfLayer.append(finalListOfData[loopList + 1])


          oldY = finalListOfData[loopList + 1]
          yAdded = True
          xAdded = False
        else:
          coordinatesOfLayer.append(oldX)
          xAdded = True
          yAdded = False
          indexChange = True   
      else:
        if xAdded and not(yAdded):
          coordinatesOfLayer.append(oldY)

          # When duo is complete
          #coordinatesOfLayer.append(oldX)
          #coordinatesOfLayer.append(oldY)

          indexChange = True
          yAdded = True
          xAdded = False
          stopSpace = True

        if xAdded == False and yAdded == True and stopSpace == False:
          coordinatesOfLayer.append("")
          stopSpace = False

        if stopSpace:
          stopSpace = False

      if indexChange:
        indexChange = False
      else:
        loopList += 2
    except IndexError:
      makingListOfCoordinate = False

  with open("C:\\Users\\alexi\\Desktop\\Work\Work\\1ere annee\\Python\\EvTest-Converter\\Output-Files\\debug.txt", 'w+') as f:
    for u in coordinatesOfLayer:
      f.write(u + "\n")
  return coordinatesOfLayer

while writingPermission:
  
  resetVar()

  # Retrieve the path of the EvTest file And test if its good
  while pathIsOk is True:
    # INPUT
    print("Please put the evtest file :")
    filePath = str(input())
    
    # Remove double quotes
    filePath = re.sub("\"", "", filePath)

    # CHECK IF PATH IS OK
    try:
      finalFileName = getNameOfFile(filePath, count, myFileName)
      pathIsOK = False
      break
    except NameError:
      print("Error: Wrong path")

  # Make the output path
  outputFilePath = THIS_FOLDER + "\\Output-Files\\" + finalFileName

  print("")
  print("Creating CSV file...")

  # Remove useless data 
  cleanData = fileOpenning(filePath)


  # LIST OF ALL DATA BUT WITHOUT TIME
  for u in cleanData:
    if len(u) < 8: 
      cleanDataWithoutTime.append(u)


  coordinatesOfLayer = whereToDrawLine(cleanDataWithoutTime, coordinatesOfLayer)

  cleanCoordinatesOfLayer = []
  for u in coordinatesOfLayer:
    if u != "":
      cleanCoordinatesOfLayer.append(u)

  spaceAdded = False

  # SPLIT coordinateOfLayer
  # TO A LIST OF X AND Y
  while makingCoordinates:
    try:
      if coordinatesOfLayer[loopList] == "":
        listOfX.append("")
        listOfY.append("")
        spaceAdded = True
      else:
        try:
          listOfX.append(coordinatesOfLayer[loopList])
          listOfY.append(coordinatesOfLayer[loopList + 1])
          spaceAdded = False
        except IndexError:
          makingCoordinates = False
          break
    except IndexError:
      break

    if spaceAdded:
      loopList += 1
    else:
      loopList += 2

  # LIST OF TIME
  for item in cleanData:
    if len(item) > 8:
      listOfTimestamp.append(item)

  # LIST OF CODES
  for item in cleanData:
    if item == "c57" or item == "c54" or item == "c53" or item == "c58":
      listOfCodes.append(item)
  
  # LIST OF VALUE
  loopValue = 0
  addingValue = True

  while addingValue:
    try:
      item = cleanDataWithoutTime[loopValue]
    except IndexError:
      break

    if item != 'c57' and item != 'c54' and item != 'c53' and item != 'c58':
      listOfValues.append(cleanDataWithoutTime[loopValue])
    
    loopValue += 1


  try:
    # Convert all data to a CSV format and write it to a file
    convertDataToCsv(listOfTimestamp, listOfCodes, listOfValues, listOfX, listOfY)
    writingPermission = False
  except PermissionError:
    print("Can't create the output file, maybe the file is already open in excel.")
    print("")

print("CSV File succesfully created at the folder \"Output-Files\" !")
input()
