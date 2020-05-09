  xAdded = False
  yAdded = True
  indexChange = False
  oldX = ""
  oldY = ""
  makingListOfCoordinate = True
  loopList = 0    
  stopSpace = False
  notRepetition = False

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
          stopSpace = True
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
          if not(notRepetition):
            coordinatesOfLayer.append(oldX)
            coordinatesOfLayer.append(finalListOfData[loopList + 1])
          else:
            notRepetition = False
            


          oldY = finalListOfData[loopList + 1]
          yAdded = True
          xAdded = False
          stopSpace = False
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
          coordinatesOfLayer.append("0")
          #coordinatesOfLayer.append("0")
          stopSpace = False

        if stopSpace:
          stopSpace = False

      if indexChange:
        indexChange = False
        notRepetition = True
      else:
        loopList += 2
    except IndexError:
      makingListOfCoordinate = False
      
  return coordinatesOfLayer