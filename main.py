# Import all necessary files/libraries

from DijkstrasAlgorithm import dijkstras
from DijkstrasAlgorithmWashrooms import dijkstrasWashroom
from DijkstrasAlgorithmTour import dijkstrasTour
from tkinter import *
import os
import sys


class bossgps:

    def __init__(self):
        # all attributes of "bossgps" class

        # These are general attributes/attributes responsible for the standard "Direction" option in the program
        self.window = Tk()
        self.window.geometry("500x850")
        self.window.resizable(False, False)
        self.window.title(string="BOSS GPS")
        self.window.iconbitmap(os.path.join(sys.path[0], r"Images\BOSSBulldogLogo.png"))
        self.startingRoom = None
        self.endingRoom = None
        self.currInd = 0
        self.path = None
        self.imageFrame = Frame(self.window)
        self.frame1 = Frame(self.window)
        self.frame2 = Frame(self.window)
        self.frame3 = Frame(self.window)
        self.frame4 = Frame(self.window)
        self.frame5 = Frame(self.window)
        self.directionsButton = Button(self.frame1, text="GET DIRECTIONS", command=self.page2, width=25, height=2)
        self.startingRoomEntry = Entry(self.frame1, width=40)
        self.endingRoomEntry = Entry(self.frame2, width=40)
        self.walkingSpeedEntry = Entry(self.frame3, width=40)
        self.labelForStartingRoomEntry = Label(self.frame1, text="Insert starting room number:", width=35)  # entire window should be around 70
        self.labelForEndingRoomEntry = Label(self.frame2, text="Insert ending room number:", width=35)
        self.labelForWalkingSpeedEntry = Label(self.frame3, text="Walking speed (km/h):", width=35)
        self.enterButton = Button(self.frame5, text="ENTER", command=self.getStartingAndEndingRooms, width=25)
        self.returnButton = Button(self.frame5, text="RETURN", command=self.page1, width=25)
        self.nextButton = Button(self.frame2, text="NEXT", command=self.addOneIndex, width=25, height=2)
        self.backButton = Button(self.frame2, text="BACK", command=self.minusOneIndex, width=25, height=2)
        self.resetButton = Button(self.frame5, text="RESET", command=self.page1, width=25, height=2)
        self.instructionText = Text(self.frame1, width=61, height=5, wrap=WORD)
        self.anImage = PhotoImage(file=os.path.join(sys.path[0], r"Images\BOSSGPS LOGO.png"))
        self.imageLabel = Label(self.imageFrame, image=self.anImage)
        self.pathFinder = dijkstras()
        self.pathFinder.getInfo()
        self.pathFinderWashroom = dijkstrasWashroom()
        self.pathFinderWashroom.getInfo()

        # these are the attributes responsible for the "find nearest washroom" option in the program
        self.washroomButton = Button(self.frame2, text="FIND NEAREST WASHROOM", command=self.page2washroom, width=25, height=2)
        self.maleIntVar = IntVar(self.frame2, value=0)
        self.genderCheckBoxMale = Checkbutton(self.frame2, text="Male", variable=self.maleIntVar)
        self.femaleIntVar = IntVar(self.frame2, value=0)
        self.genderCheckBoxFemale = Checkbutton(self.frame2, text="Female", variable=self.femaleIntVar)
        self.barrierFreeIntVar = IntVar(self.frame2, value=0)
        self.genderCheckBoxBarrierFree = Checkbutton(self.frame2, text="Barrier-free", variable=self.barrierFreeIntVar)
        self.studentOrStaffStringVar = StringVar(self.frame3, value="Any")
        self.studentRadioButton = Radiobutton(self.frame3, text="Student", variable=self.studentOrStaffStringVar, value="student")
        self.staffRadioButton = Radiobutton(self.frame3, text="Staff", variable=self.studentOrStaffStringVar, value="staff")
        self.bothRadioButton = Radiobutton(self.frame3, text="Both", variable=self.studentOrStaffStringVar, value="Any")
        self.enterWashroomButton = Button(self.frame5, text="ENTER", command=self.getStartingGenderStudentStaff, width=25)
        self.gender = None
        self.studentOrStaff = None

        # these are the attributes responsible for the "school tour" option in the program
        self.pathFinderTour = dijkstrasTour()
        self.pathFinderTour.getInfo()
        self.tourButton = Button(self.frame3, text="SCHOOL TOUR", command=self.page2tour, width=25, height=2)
        self.roomsToVisitTextBox = Text(self.frame4, width=61, height=5, wrap=WORD)
        self.roomsToVisitList = []
        self.tourEnterButton = Button(self.frame5, text="ENTER", command=self.getRoomsToVisit, width=25)





    def page1(self):

        # this is the home page, with the logo and the three options

        self.unpack()

        self.directionsButton.grid(row=0, column=2, sticky='nesw')
        self.washroomButton.grid(row=0, column=0, sticky='nesw')
        self.tourButton.grid(row=0, column=0, sticky='nesw')

        self.anImage = PhotoImage(file=os.path.join(sys.path[0], r"Images\BOSSGPS LOGO.png"))
        self.imageLabel = Label(self.imageFrame, image=self.anImage)
        self.imageLabel.grid(row=0, column=0, sticky='nesw')

        self.packFrames()

        self.window.mainloop()
        

    def page2(self):
        # this is the menu for the "directions" option
        
        self.unpack()

        self.startingRoomEntry.grid(row=0, column=1, sticky='e')
        self.endingRoomEntry.grid(row=0, column=1, sticky='e')
        self.walkingSpeedEntry.grid(row=0, column=1, sticky='e')
        self.labelForStartingRoomEntry.grid(row=0, column=0, sticky='w')
        self.labelForEndingRoomEntry.grid(row=0, column=0, sticky='w')
        self.labelForWalkingSpeedEntry.grid(row=0, column=0, sticky='w')
        self.enterButton.grid(row=0, column=1)
        self.returnButton.grid(row=0, column=0)

        self.packFrames()

    
    def getStartingAndEndingRooms(self):
        # this gets the starting and ending rooms from the "directions" menu
        self.startingRoom = self.startingRoomEntry.get()
        self.endingRoom = self.endingRoomEntry.get()
        self.walkingSpeed = self.walkingSpeedEntry.get()

        if self.startingRoom not in self.pathFinder.roomToIndex and self.startingRoom not in self.pathFinder.specialRoomToSpecialRoomNumber and self.startingRoom not in self.pathFinder.roomsWithMultipleEntrances:
            self.startingRoomEntry.delete(0, END)
            self.startingRoomEntry.insert(0, string=f"\"{self.startingRoom}\" is an invalid room number")
            return
        if self.endingRoom not in self.pathFinder.roomToIndex and self.endingRoom not in self.pathFinder.specialRoomToSpecialRoomNumber and self.endingRoom not in self.pathFinder.roomsWithMultipleEntrances:
            self.endingRoomEntry.delete(0, END)
            self.endingRoomEntry.insert(0, string=f"\"{self.endingRoom}\" is an invalid room number")
            return
        try:
            float(self.walkingSpeed)
        except:
            self.walkingSpeedEntry.delete(0, END)
            self.walkingSpeedEntry.insert(0, string=f"\"{self.walkingSpeed}\" is an invalid walking speed")
            return
        
        self.runPathFinder()



    def page2washroom(self):
        # this is the menu for the "find nearest washroom" option

        self.unpack()

        self.startingRoomEntry.grid(row=0, column=1, sticky='e')
        self.labelForStartingRoomEntry.grid(row=0, column=0, sticky='w')
        self.genderCheckBoxMale.grid(row=0, column=0)
        self.genderCheckBoxFemale.grid(row=1, column=0)
        self.genderCheckBoxBarrierFree.grid(row=2, column=0)
        self.studentRadioButton.grid(row=0, column=0)
        self.staffRadioButton.grid(row=1, column=0)
        self.bothRadioButton.grid(row=2, column=0)
        self.enterWashroomButton.grid(row=0, column=1)
        self.returnButton.grid(row=0, column=0)

        self.packFrames()
        

    def getStartingGenderStudentStaff(self):
        # this gets the starting room, gender of the user, and student/staff title of the user from the "find nearest washroom" option
        self.startingRoom = self.startingRoomEntry.get()
        
        if self.maleIntVar.get() == 1 and self.femaleIntVar.get() == 1 and self.barrierFreeIntVar.get() == 1:
            self.gender = "Any"
        elif self.maleIntVar.get() == 1:
            self.gender = "male"
        elif self.femaleIntVar.get() == 1:
            self.gender = "female"
        elif self.barrierFreeIntVar.get() == 1:
            self.gender = "BF"
        else:
            return

        if self.studentOrStaffStringVar.get() == "Any":
            self.studentOrStaff = "Any"
        elif self.studentOrStaffStringVar.get() == "student":
            self.studentOrStaff = "student"
        else:
            self.studentOrStaff = "staff"

        if self.startingRoom not in self.pathFinderWashroom.roomToIndex and self.startingRoom not in self.pathFinderWashroom.specialRoomToSpecialRoomNumber and self.startingRoom not in self.pathFinderWashroom.roomsWithMultipleEntrances:
            self.startingRoomEntry.delete(0, END)
            self.startingRoomEntry.insert(0, string=f"\"{self.startingRoom}\" is an invalid room number")
            return
        
        self.runPathFinderWashroom()

    
    def runPathFinder(self):
        # runs standard path finder in "DijkstrasAlgorithm.py" file for the "directions option"
        self.unpack()
        self.currInd = 0
        self.path = self.pathFinder.run(self.startingRoom, self.endingRoom, self.walkingSpeed)
        
        # this is used to display the photo/message to the user
        self.updateRoomAndPhoto()

    
    def runPathFinderWashroom(self):
        # runs altered path finder in "DijkstrasAlgorithmWashrooms.py" file for the "find nearest washroom" option
        self.unpack()
        self.currInd = 0
        self.path = self.pathFinderWashroom.run(self.startingRoom, self.gender, self.studentOrStaff)
        self.updateRoomAndPhoto()


    def addOneIndex(self):
        # this is just to increment through the photos/messages for the path to get to a room. "next" button calls this.

        self.currInd+=1
        self.updateRoomAndPhoto()


    def minusOneIndex(self):
        # this also increments through the photo/messages for the path to get to a room. "back" button calls this.

        self.currInd-=1
        self.updateRoomAndPhoto()


    def updateRoomAndPhoto(self):
        # this method updates the message and corresponding photo based on the index of the path we are on

        self.instructionText.delete(0.0, END)
        self.instructionText.insert(END, self.path[self.currInd][0])
        self.instructionText.grid(row=0, column=0)
        if self.path[self.currInd][1] == None:
            self.anImage = PhotoImage(file=os.path.join(sys.path[0], r"Images\BOSSGPS LOGO.png"))
        else:
            self.anImage = PhotoImage(file=os.path.join(sys.path[0], "Images\\"+self.path[self.currInd][1]+".png"))
        self.imageLabel = Label(self.imageFrame, image=self.anImage)
        self.imageLabel.grid(row=0, column=0)

        if self.currInd < len(self.path)-1:
            self.nextButton.grid(row=0, column=1)
        else:
            self.nextButton.grid_forget()

        if self.currInd > 0:
            self.backButton.grid(row=0, column=0)
        else:
            self.backButton.grid_forget()

        self.resetButton.grid(row=1, column=0)



    def page2tour(self):
        # this is the menu for the "tour school" option

        self.unpack()

        self.startingRoomEntry.grid(row=0, column=1, sticky='e')
        self.endingRoomEntry.grid(row=0, column=1, sticky='e')
        self.walkingSpeedEntry.grid(row=0, column=1, sticky='e')
        self.labelForStartingRoomEntry.grid(row=0, column=0, sticky='w')
        self.labelForEndingRoomEntry.grid(row=0, column=0, sticky='w')
        self.labelForWalkingSpeedEntry.grid(row=0, column=0, sticky='w')
        self.roomsToVisitTextBox.delete(0.0, END)
        self.roomsToVisitTextBox.insert(0.0, "Enter rooms to visit here, separated by a space (e.g. 1004 2015).")
        self.roomsToVisitTextBox.grid(row=0, column=0, stick='nesw')
        self.tourEnterButton.grid(row=0, column=1)
        self.returnButton.grid(row=0, column=0)

        self.packFrames()

    
    def getRoomsToVisit(self):
        # this method gets the list of rooms to visit on the tour from the textbox

        self.startingRoom = self.startingRoomEntry.get()
        self.endingRoom = self.endingRoomEntry.get()
        self.walkingSpeed = self.walkingSpeedEntry.get()
        self.roomsToVisitList = self.roomsToVisitTextBox.get(0.0, END).strip().split(' ')

        if self.startingRoom not in self.pathFinderTour.roomToIndex and self.startingRoom not in self.pathFinderTour.specialRoomToSpecialRoomNumber and self.startingRoom not in self.pathFinderTour.roomsWithMultipleEntrances:
            self.startingRoomEntry.delete(0, END)
            self.startingRoomEntry.insert(0, string=f"\"{self.startingRoom}\" is an invalid room number")
            return
        if self.endingRoom not in self.pathFinderTour.roomToIndex and self.endingRoom not in self.pathFinderTour.specialRoomToSpecialRoomNumber and self.endingRoom not in self.pathFinderTour.roomsWithMultipleEntrances:
            self.endingRoomEntry.delete(0, END)
            self.endingRoomEntry.insert(0, string=f"\"{self.endingRoom}\" is an invalid room number")
            return
        try:
            float(self.walkingSpeed)
        except:
            self.walkingSpeedEntry.delete(0, END)
            self.walkingSpeedEntry.insert(0, string=f"\"{self.walkingSpeed}\" is an invalid walking speed")
            return
        for aRoom in self.roomsToVisitList:
            if aRoom not in self.pathFinderTour.roomToIndex and aRoom not in self.pathFinderTour.specialRoomToSpecialRoomNumber and aRoom not in self.pathFinderTour.roomsWithMultipleEntrances:
                self.roomsToVisitTextBox.delete(0.0, END)
                self.roomsToVisitTextBox.insert(0.0, f"\"{aRoom}\" is invalid.")
                return
        
        self.runPathFinderTour()



    def runPathFinderTour(self):
        # this runs the altered path finding algorithm from "DijkstrasAlgorithmTour.py"
        self.unpack()
        self.currInd = 0
        self.path = self.pathFinderTour.run(self.startingRoom, self.endingRoom, self.walkingSpeed, self.roomsToVisitList)
        self.updateRoomAndPhoto()



    def unpack(self):
        # Helper method for unpacking everything except for frames. Used to reset the window.

        self.directionsButton.grid_forget()
        self.startingRoomEntry.grid_forget()
        self.endingRoomEntry.grid_forget()
        self.walkingSpeedEntry.grid_forget()
        self.enterButton.grid_forget()
        self.returnButton.grid_forget()
        self.nextButton.grid_forget()
        self.backButton.grid_forget()
        self.resetButton.grid_forget()
        self.instructionText.grid_forget()
        self.labelForStartingRoomEntry.grid_forget()
        self.labelForEndingRoomEntry.grid_forget()
        self.labelForWalkingSpeedEntry.grid_forget()
        self.washroomButton.grid_forget()
        self.genderCheckBoxMale.grid_forget()
        self.genderCheckBoxFemale.grid_forget()
        self.genderCheckBoxBarrierFree.grid_forget()
        self.studentRadioButton.grid_forget()
        self.staffRadioButton.grid_forget()
        self.bothRadioButton.grid_forget()
        self.enterWashroomButton.grid_forget()
        self.tourButton.grid_forget()
        self.roomsToVisitTextBox.grid_forget()
        self.tourEnterButton.grid_forget()


    def packFrames(self):
        # this method is used to pack the frames to update the window after changes have been made.

        self.imageFrame.grid(row=0, column=0)
        self.frame1.grid(row=1, column=0)
        self.frame2.grid(row=2, column=0)
        self.frame3.grid(row=3, column=0)
        self.frame4.grid(row=4, column=0)
        self.frame5.grid(row=5, column=0)



a = bossgps()
a.page1()
