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

def convertDataToCsv(cleanData):
  # Writing these data to an excel sheet
  with open(outputFilePath, 'w+', newline='') as f:
    fieldnames = ['FullTime', 'DateHour', 'hour', 'Code', 'Value', 'X', 'Y']
    theWriter = csv.DictWriter(f, fieldnames=fieldnames)

    theWriter.writeheader()

    addingData = True
    loopValue = 0

    while addingData:

      # Check if error happenned
      try:
        if len(cleanData[loopValue]) < 10:
          break
        if len(cleanData[loopValue + 1]) > 5 or len(cleanData[loopValue + 3]) > 5:
          break
      except IndexError:
        break


      try:
        theWriter.writerow(
          {
          'FullTime': cleanData[loopValue], 'Code': cleanData[loopValue + 1], 'Value': cleanData[loopValue + 2], 'X': cleanData[loopValue + 3], 'Y': cleanData[loopValue + 4]
          })
      except IndexError:
        break

      loopValue += 5

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
  
  loopList = 0
  xAdded = False
  yAdded = True
  oldX = ""
  oldY = ""

  while True:
    try:
      item = finalListOfData[loopList]
      secondItem = finalListOfData[loopList + 1]
    except IndexError:
      break

    if item == 'c53':

      xAdded = True

      # Try to look if after theres a code 54
      if finalListOfData[loopList + 2] == 'c54':
        xAdded = True
      else:
        if xAdded:
          coordinatesOfLayer.append(oldY)
        xAdded = False

      coordinatesOfLayer.append(secondItem)

      oldX = secondItem


    elif item == 'c54':
      if xAdded:
        coordinatesOfLayer.append(secondItem)
      else:
        coordinatesOfLayer.append(oldX)
        coordinatesOfLayer.append(secondItem)
        xAdded = False
      oldY = secondItem

      # Does before was a c53 ?
      if finalListOfData[loopList - 2] == 'c53':
        coordinatesOfLayer.append(oldX)
        coordinatesOfLayer.append(oldY)
        xAdded = False


    else:
      xAdded = False
      yAdded = False
      coordinatesOfLayer.append("0")
    
    loopList += 2
  
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
      if coordinatesOfLayer[loopList] == "0":
        listOfX.append("0")
        listOfY.append("0")
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
  
  ## ADDING X AND Y TO ORIGINAL LIST
  addingValue = True
  valueItem = ""
  loopValue = 3
  xIndex = 0
  yIndex = 0
  while addingValue:

    if xIndex > len(listOfX):
      break

    try:
      cleanData.insert(loopValue, listOfY[yIndex])
      cleanData.insert(loopValue, listOfX[xIndex])
    except IndexError:
      addingValue = False
      break

    xIndex += 1
    yIndex += 1
    loopValue += 5

  try:
    # Convert all data to a CSV format and write it to a file
    convertDataToCsv(cleanData)
    writingPermission = False
  except PermissionError:
    print("Can't create the output file, maybe the file is already open in excel.")
    print("")

print("CSV File succesfully created at the folder \"Output-Files\" !")
input()
