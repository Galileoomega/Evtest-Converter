###################################################################
#####                  Convert EventTest file data
#####                   to an Excel Sheet (.CSV)
###################################################################

import csv, re, datetime, os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
iHaveMyFile = False
count = 5
myFileName = ""
listOfTimestamp = []
listOfCodes = []
listOfValues = []
pathIsOk = True
writingPermission = True

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
    tempPressEvent = re.sub(".*code 58.*", "", tempPressEvent)
    #Find relevant data

    pressList = re.findall("Event: time..................|code 57.*|code 53.*|code 54.*|code 47.*", tempPressEvent)

    finalListOfData = []
    
    for u in pressList:
      u = re.sub("code | value| alue| time", "", u)
      u = re.sub("Event: ", "", u)

      if len(u) > 8:
            u = datetime.datetime.fromtimestamp(float(u)).isoformat()

      finalListOfData += re.split("\s", u)

  return finalListOfData

def convertDataToCsv(listOfTimestamp, listOfCodes, listOfValues):
  # Writing these data to an excel sheet
  with open(outputFilePath, 'w+', newline='') as f:
    fieldnames = ['Time', 'Code', 'Value',]
    theWriter = csv.DictWriter(f, fieldnames=fieldnames)

    theWriter.writeheader()

    for time, code, value in zip(listOfTimestamp, listOfCodes, listOfValues):
      theWriter.writerow({'Time': time, 'Code': code, 'Value': value})

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

while writingPermission:
  # Retrieve the path of the EvTest file And test if its good
  while pathIsOk is True:
    print("Please put the evtest file :")
    filePath = str(input())

    filePath = re.sub("\"", "", filePath)

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

  for item in cleanData:
    if len(item) > 8:
      listOfTimestamp.append(item)

  for item in cleanData:
    if item == "57" or item == "54" or item == "53":
      listOfCodes.append(item)
    
  for item in cleanData:
    if len(item) < 8:
      if item != "57" and item != "54" and item != "53":
        listOfValues.append(item)


  try:
    # Convert all data to a CSV format and write it to a file
    convertDataToCsv(listOfTimestamp, listOfCodes, listOfValues)
    writingPermission = False
  except PermissionError:
    print("Can't create the output file, maybe the file is already open in excel.")
    print("")

print("CSV File succesfully created at the folder \"Output-Files\".")
input()
