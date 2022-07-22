import os
import sys

class dijkstrasWashroom:
    def __init__(self):
        self.roomToConnectedRooms = {}  # maps room to connected room. IMPORTANT: each connected room is [weight, connectedRoom] for the sake of sorting

        self.roomToIndex = {}  # maps a room to an index
        self.indexToRoom = {}  # maps an index to a room
        self.roomsWithMultipleEntrances = []
        self.specialRoomToSpecialRoomNumber = {}
        self.specialRoomNumberToSpecialRoom = {}
        self.cardinalDirectionToIndex = {}
        self.allDirections = []
        self.cardinalDirectionToAngle = {}
        self.roomNameToFinalName = {}  # index --> [finalName1, finalName2]
        self.allValidWashrooms = []

        self.roomToCoordinate = {}

        self.roomToPictures = {}

        self.numRooms = 0

        self.startingRoom = None
        self.endingRoom = None
        self.gender = None
        self.studentOrStaff = None

        
    def getInfo(self):
        self.getConnectedRooms()
        self.getRoomCoordinates()
        self.getRoomsWithMultipleEntrances()
        self.getSpecialRooms()
        self.getDirections()
        self.getCodeNameToFinalName()
        self.getRoomToPictures()


    def run(self, startingRoom, gender, studentOrStaff):
        self.getDirections()  # must reset

        # gets the staring and ending rooms
        self.startingRoom = startingRoom
        # self.startingRoom = self.startingRoom.lower()
        if self.startingRoom in self.specialRoomToSpecialRoomNumber:
            self.startingRoom = self.specialRoomToSpecialRoomNumber[self.startingRoom]
        elif self.startingRoom in self.roomsWithMultipleEntrances:
            self.startingRoom = self.startingRoom+"A"
        self.startingRoom = self.roomToIndex[self.startingRoom]

        self.gender = gender
        self.studentOrStaff = studentOrStaff

        self.getWashrooms()  # must get washrooms at runtime because we don't know which one's are valid untill gender and studentorstaff are provided

        dist, path = self.getShortestPath(self.roomToConnectedRooms, self.numRooms, self.startingRoom)
        finalMessagePlusEndPointPictures = self.translatePath(dist, path)
        return finalMessagePlusEndPointPictures



    def getConnectedRooms(self):
        indForRoom = 1;
        connectedRoomsFile = open(os.path.join(sys.path[0], "ConnectedRooms"), "r")
        for edge in connectedRoomsFile:
            
            if edge == "\n":
                continue

            if edge[0] == "/":
                continue
            edge = edge.strip()
            edge = edge.split(' ')
            edge[2] = float(edge[2])

            if edge[0] not in self.roomToIndex:
                self.roomToIndex[edge[0]] = indForRoom
                self.indexToRoom[indForRoom] = edge[0]
                self.roomToCoordinate[indForRoom] = []
                self.roomToConnectedRooms[indForRoom] = []
                indForRoom += 1

            if edge[1] not in self.roomToIndex:
                self.roomToIndex[edge[1]] = indForRoom
                self.indexToRoom[indForRoom] = edge[1]
                self.roomToConnectedRooms[indForRoom] = []
                self.roomToCoordinate[indForRoom] = []
                indForRoom+=1
            
            self.roomToConnectedRooms[self.roomToIndex[edge[1]]].append([edge[2], self.roomToIndex[edge[0]]])
            self.roomToConnectedRooms[self.roomToIndex[edge[0]]].append([edge[2], self.roomToIndex[edge[1]]])
        connectedRoomsFile.close()


    def getRoomCoordinates(self):
        '''
        self.roomToCoordinate = {self.roomToIndex[room] --> [x, y]}

        Note: Assumes you have run self.getConnectedRooms first
        
        '''

        roomCoordinatesFile = open(os.path.join(sys.path[0], "RoomCoordinates"), "r")
        for aCoordinate in roomCoordinatesFile:

            if aCoordinate == "\n":
                continue
            if aCoordinate[0] == "/":
                continue

            aCoordinate = aCoordinate.strip()
            aCoordinate = aCoordinate.split(' ')
            aCoordinate[1] = float(aCoordinate[1])
            aCoordinate[2] = float(aCoordinate[2])

            self.roomToCoordinate[self.roomToIndex[aCoordinate[0]]].append(aCoordinate[1])
            self.roomToCoordinate[self.roomToIndex[aCoordinate[0]]].append(aCoordinate[2])

        roomCoordinatesFile.close()


    
    def getRoomsWithMultipleEntrances(self):
        fileRoomWithMultipleEntrances = open(os.path.join(sys.path[0], "RoomsWithMultipleEntrances"), "r")
        for aRoom in fileRoomWithMultipleEntrances:
            if aRoom == "\n":
                continue
            if aRoom[0] == "/":
                continue
            aRoom = aRoom.strip()
            self.roomsWithMultipleEntrances.append(aRoom)


    def getSpecialRooms(self):
        fileSpecialRooms = open(os.path.join(sys.path[0], "SpecialRooms"), "r")
        for aSpecialRoom in fileSpecialRooms:
            if aSpecialRoom == "\n":
                continue
            if aSpecialRoom[0] == "/":
                continue
            aSpecialRoom = aSpecialRoom.strip()
            aSpecialRoom = aSpecialRoom.split(" ")
            self.specialRoomToSpecialRoomNumber[aSpecialRoom[0]] = aSpecialRoom[1]
            self.specialRoomNumberToSpecialRoom[aSpecialRoom[1]] = aSpecialRoom[0]
        fileSpecialRooms.close()

    
    def getDirections(self):
        self.cardinalDirectionToIndex = {"North" : 0, "North East" : 1, "East" : 2, "South East" : 3, "South" : 4,  "South West" : 5,  "West" : 6, "North West" : 7}
        self.allDirections = ["0 degrees", "45 degrees to the right", "90 degrees to the right", "135 degrees to the right", "180 degrees", "135 degrees to the left", "90 degrees to the left", "45 degrees to the left"]


    def getCodeNameToFinalName(self):
        tmp = None
        with open(os.path.join(sys.path[0], "CodeNameToFinalName"), "r") as codeNameToFinalName:
    
            ind = 0
            key = None
            for i in codeNameToFinalName:
                if i == "\n":
                    continue
                if i[0] == "/":
                    continue
                i = i.strip()
                if ind == 3:
                    ind = 0
                if ind == 0:
                    key = self.roomToIndex[i]
                    self.roomNameToFinalName[key] = []
                if ind == 1:
                    self.roomNameToFinalName[key].append(i)
                if ind == 2:
                    self.roomNameToFinalName[key].append(i)
                ind+=1

        
    def getRoomToPictures(self):
        with open(os.path.join(sys.path[0], "RoomToPicture"), "r") as fileRoomToPicture:
            ind = 0
            key = None
            for i in fileRoomToPicture:
                if i == "\n":
                    continue
                if i[0] == "/":
                    continue
                i = i.strip()
                if ind == 2:
                    ind = 0
                if ind == 0:
                    key = self.roomToIndex[i]
                    self.roomToPictures[key] = None
                if ind == 1:
                    self.roomToPictures[key] = i
                ind += 1

            for i in self.roomToConnectedRooms:
                if i not in self.roomToPictures:
                    self.roomToPictures[i] = None


    def getWashrooms(self):
        with open(os.path.join(sys.path[0], "Washrooms"), "r") as washrooms:
            for aWashroom in washrooms:
                if aWashroom == "\n":
                    continue
                if aWashroom[0] == "/":
                    continue
                
                aWashroom = aWashroom.strip()
                aWashroom = aWashroom.split(' ')
                room = self.roomToIndex[aWashroom[0]]
                if aWashroom[1] == self.gender or self.gender == "Any":
                    if aWashroom[2] == self.studentOrStaff or self.studentOrStaff == "Any":
                        self.allValidWashrooms.append(room)




    def SSSP(self, roomToConnectedRooms, numRooms, startingRoom):

        visited = {}
        for aRoom in roomToConnectedRooms:
            visited[aRoom] = False
        
        dist = {}
        for aRoom in roomToConnectedRooms:
            dist[aRoom] = 999

        previous = {}
        for aRoom in roomToConnectedRooms:
            previous[aRoom] = None

        visited[startingRoom] = True
        dist[startingRoom] = 0

        pq = []
        pq.append((0, startingRoom))

        while len(pq) > 0:
            weight, index = pq[0]
            pq = pq[1:]
            visited[index] = True
            if dist[index] < weight:
                continue
            for edge in roomToConnectedRooms[index]:
                if self.indexToRoom[edge[1]][0] in '12' and self.indexToRoom[edge[1]][:4] != self.indexToRoom[self.startingRoom][:4] and edge[1] not in self.allValidWashrooms:
                    continue
                if visited[edge[1]] == True:
                    continue
                newDistance = dist[index] + edge[0]
                if newDistance < dist[edge[1]]:
                    previous[edge[1]] = index
                    dist[edge[1]] = newDistance
                    pq.append((dist[edge[1]], edge[1]))
            if index in self.allValidWashrooms:
                self.endingRoom = index
                return (dist, previous)
            pq.sort()
        return (dist, previous)



    def getShortestPath(self, roomToConnectedRooms, numRooms, startingRoom):
        dist, previous = self.SSSP(roomToConnectedRooms, numRooms, startingRoom)
        path = []
        curr = self.endingRoom
        while curr != None:
            path.append(curr)
            curr = previous[curr]
        path.reverse()
        return (dist, path)


    def translatePath(self, dist, path):
        translatedPath = []  # ["direction", distance, "room to start at", "room to go to"]
        ind = 1
        while True:
            if ind == len(path) or len(path) == 0:
                break

            currentPath = []
            pastx, pasty = self.roomToCoordinate[path[ind-1]][0], self.roomToCoordinate[path[ind-1]][1]
            currx, curry = self.roomToCoordinate[path[ind]][0], self.roomToCoordinate[path[ind]][1]
            if currx - pastx > 0 and curry - pasty > 0:
                currentPath.append("North East")
            elif currx - pastx > 0 and curry - pasty < 0:
                currentPath.append("South East")
            elif currx - pastx < 0 and curry - pasty > 0:
                currentPath.append("North West")
            elif currx - pastx < 0 and curry - pasty < 0:
                currentPath.append("South West")
            elif currx - pastx > 0 and curry - pasty == 0:
                currentPath.append("East")
            elif currx - pastx < 0 and curry - pasty == 0:
                currentPath.append("West")
            elif currx - pastx == 0 and curry - pasty > 0:
                currentPath.append("North")
            elif currx - pastx == 0 and curry - pasty < 0:
                currentPath.append("South")
            currentPath.append(dist[path[ind]]-dist[path[ind-1]])
            currentPath.append(path[ind-1])
            currentPath.append(path[ind])
            translatedPath.append(currentPath)

            ind+=1

        cardinalTranslatedPath = []  # ["Direction", distance, "room to start walking at", "room to stop walking at"]
        currentDirection = None
        indForTranslatedPath = 0

        while True: 
            if indForTranslatedPath == len(translatedPath):
                break
            if translatedPath[indForTranslatedPath][0] != currentDirection:
                currentDirection = translatedPath[indForTranslatedPath][0]
                cardinalTranslatedPath.append([currentDirection, translatedPath[indForTranslatedPath][1], translatedPath[indForTranslatedPath][2], self.endingRoom])
                if len(cardinalTranslatedPath) > 1:
                    cardinalTranslatedPath[-2][3] = cardinalTranslatedPath[-1][2]                
            else:
                cardinalTranslatedPath[-1][1]+=translatedPath[indForTranslatedPath][1]
            indForTranslatedPath+=1
        finalMessage = []
        ind = 0

        if self.indexToRoom[self.startingRoom] in self.specialRoomNumberToSpecialRoom:
            self.indexToRoom[self.startingRoom] = self.specialRoomNumberToSpecialRoom[self.indexToRoom[self.startingRoom]]
        if self.indexToRoom[self.endingRoom] in self.specialRoomNumberToSpecialRoom:
            self.indexToRoom[self.endingRoom] = self.specialRoomNumberToSpecialRoom[self.indexToRoom[self.endingRoom]]
        
        finalMessage.append(["Start at room " + str(self.indexToRoom[self.startingRoom]) + ".\n", self.roomToPictures[self.startingRoom]])
        while True:
            if ind == len(cardinalTranslatedPath):
                break
            distanceToWalk = cardinalTranslatedPath[ind][1]
            if ind == 0:
                pastCardinalDirection = "North"
            else:
                pastCardinalDirection = cardinalTranslatedPath[ind-1][0]
            newCardinalDirection = cardinalTranslatedPath[ind][0]
            startingPoint = cardinalTranslatedPath[ind][2]
            endingPoint = cardinalTranslatedPath[ind][3]
            message = self.getTurningDirectionGivenCardinalDirection(pastCardinalDirection, newCardinalDirection, distanceToWalk, startingPoint, endingPoint)
            message = [message, self.roomToPictures[endingPoint]]
            finalMessage.append(message)
            ind+=1
        finalMessage.append([f"You have reached washroom {self.indexToRoom[self.endingRoom][:4]}!", self.roomToPictures[self.endingRoom]])
        return finalMessage


    def getTurningDirectionGivenCardinalDirection(self, pastCardinalDirection, newCardinalDirection, distance, startingPoint, endingPoint):
        pastCardinalIndex = self.cardinalDirectionToIndex[pastCardinalDirection]
        newCardinalIndex = self.cardinalDirectionToIndex[newCardinalDirection]
        shift = newCardinalIndex - pastCardinalIndex
        shift *= -1
        
        turningDirection = self.allDirections[self.cardinalDirectionToIndex[newCardinalDirection]]

        self.allDirections = self.allDirections[shift:] + self.allDirections[:shift]
        returnVal = f"{self.roomNameToFinalName[startingPoint][0]}, turn {turningDirection} and walk {newCardinalDirection} for {distance} m, {self.roomNameToFinalName[endingPoint][1]}\n"

        return returnVal
