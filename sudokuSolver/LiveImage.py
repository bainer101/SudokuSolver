import cv2
import numpy as np
import sys
import time
import math
import random as rn
import copy
from picamera.array import PiRGBArray
from picamera import PiCamera

class puzzleStatusClass:
    #this class defines the actual mathematical properties of the sudoku puzzle
    #and the associated methods used to solve the actual sudoku puzzle
    def __init__(self):
        #.current is a 9x9 grid of all solved values for the puzzle
        self.current = np.zeros((9,9),np.uint8) 
        self.currentBackup = np.zeros((9,9),np.uint8)
        #.last is used to compare to .current to evaluate whether two consecutive OCR results match
        self.last = np.zeros((9,9),np.uint8)
        #.orig is used to store the state of .current that is obtained from OCR,
        #but before solving for any new values
        self.orig = np.zeros((9,9),np.uint8)
        #.selected holds the user's selected answers
        self.selected = np.zeros((9,9),np.uint8)
        #.solve starts off by containing 1-9 in a 9 by 9 grid,
        #by process of elimination .solve will produce the final solution
        self.solve = [[[1,2,3,4,5,6,7,8,9] for x in range(9)] for y in range(9)]
        self.solveBackup = []
        #.change is True when the solver algorithm has made a change to .solve
        self.change = True
        #.guess is True when the solver has given up on analytical techniques
        #and has begun randomly guessing at the solution
        self.guess = False

    def prepSolve(self):
        #run once at beginning of solver
        #make sure .current and .solve are correctly corresponding
        for y in range(9):
            for x in range(9):
                if self.current[y,x] > 0:
                    self.solve[y][x] = [self.current[y,x]]

        selectedFile = open ("selected.data", "r")
        selectedData = str(selectedFile.read())
        selectedData = selectedData.split(" ")
        del selectedData[-1]
        a = 0
        b = 0
        isRunning = True
        elenum = 0
        while isRunning:
            if (b%9 == 0 and b!=0):
                a += 1
                b = 0
            if (a == 9 and a == 9):
                isRunning = False
                break
            self.selected[a, b] = selectedData[elenum]
            b += 1
            elenum += 1

    def newSolve(self):
        #make sure .current and .solve are correctly corresponding after any changes are made
        for y in range(9):
            for x in range(9):
                if len(self.solve[y][x]) == 1:
                    self.current[y,x] = self.solve[y][x][0]
                if self.current[y,x] > 0:
                    self.solve[y][x] = [self.current[y,x]]

    def checkSolution(self):
        #check puzzle using three main rules
        err = 0 #error code
        #1) no number shall appear more than once in a row
        for x in range(9): #for each row
            #count how many of each number exists
            check = np.bincount(self.current[x,:])
            for i in range(len(check)):
                if i==0:
                    if check[i]!=0:
                        err = 1 #incomplete, when the puzzle is complete no zeros should exist
                else:
                    if check[i]>1:
                        err = -1 #incorrect, there can't be more than one of any number
                        print "ERROR in row ",x," with ",i
                        return err
        #2) no number shall appear more than once in a column
        for y in range(9): #for each column
            check = np.bincount(self.current[:,y])
            for i in range(len(check)):
                if i==0:
                    if check[i]!=0:
                        err = 1 #incomplete
                else:
                    if check[i]>1:
                        err = -1 #incorrect
                        print "ERROR in col ",y," with ",i
                        return err
        #3) no number shall appear more than once in a 3x3 cell
        for x in range(3):
            for y in range(3):
                check = np.bincount(self.current[x*3:x*3+3,y*3:y*3+3].flatten())
                for i in range(len(check)):
                    if i==0:
                        if check[i]!=0:
                            err = 1 #incomplete
                    else:
                        if check[i]>1:
                            err = -1 #incorrect
                            print "ERROR in box ",x,y," with ",i
                            return err
        return err

    def removeRow(self,rem,y,exc=[]):
        #removes a list of numbers from a row
        #rem is a list of numbers to be removed, may contain zeros (ignored)
        #y is the current row being operated on
        #exc is an index of row y to exlude from this removal process
        while True:
            n = rem.count(0)
            if n==0:
                break
            rem.remove(0)
        for i in range(9): #index in row
            for q in rem: #for each number to be removed
                if self.solve[y][i].count(q)>0 and len(self.solve[y][i])!=1 and exc.count(i)==0:
                    self.solve[y][i].remove(q)
                    self.change = True


    def removeColumn(self,rem,x,exc=[]):
        #removes a list of numbers from a column
        #rem is a list of numbers to be removed, may contain zeros (ignored)
        #x is the current row being operated on
        #exc is an index of row y to exlude from this removal process
        while True:
            n = rem.count(0)
            if n==0:
                break
            rem.remove(0)
        for i in range(9): #index of the col
            for q in rem: #for each number to be removed
                if self.solve[i][x].count(q)>0 and len(self.solve[i][x])!=1 and exc.count(i)==0:
                    self.solve[i][x].remove(q)
                    self.change = True

    def removeCell(self,rem,xcell,ycell,exc=[]):
        #removes a list of numbers from a 3x3 cell
        #rem is a list of numbers to be removed, may contain zeros (ignored)
        #xcell is the current list of x cols to be removing from
        #ycell is the current list of y rows to be removing from
        #exc is an list of [y,x] pairs to exclude from this removal process
        go = True
        while True:
            n = rem.count(0)
            if n==0:
                break
            rem.remove(0)
        for x in xcell:
            for y in ycell:
                for q in rem: #for each number to be removed
                    if self.solve[y][x].count(q)>0 and len(self.solve[y][x])!=1 and exc.count([y,x])==0:
                        self.solve[y][x].remove(q)
                        self.change = True
        for i in range(3):
            ycell[i] += 3
        if ycell[0] == 9:
            for i in range(3):
                xcell[i] += 3
                ycell[i] -= 9
        if xcell[0] == 9:
            go = False
        return go

    def simpleElimination(self):
        #eliminates simply by using the three main rules
        print "---SIMPLE RULES ELIMINATION---"
        #row elimination
        for y in range(9):
            rem = list(self.current[y])
            self.removeRow(rem,y)
        #column elimination
        for x in range(9):
            rem = list(self.current[:,x])
            self.removeColumn(rem,x)  
        #cell elimination
        xcell = [0,1,2]
        ycell = [0,1,2]
        go = True
        while go:
            rem = []
            for x in xcell:
                for y in ycell:
                    rem.append(self.current[y,x])
            go = self.removeCell(rem,xcell,ycell)

    def pairsElimination(self):
        #removes any matching pairs from the spots not containing the matching pair,
        #for example if one row has a three blanks with [1,2,3,4] , [1,2] , [1,2] ...,
        #then you would eliminate [1,2] from the spot containing [1,2,3,4]
        print "---PAIR ELIMINATION---"
        for y in range(9):
            j_used = [] #initialize for the loop
            for i in range(9): #each index of the row
                if j_used.count(i)==0: #hasn't been searched yet
                    if self.solve[y].count(self.solve[y][i]) == 2 and len(self.solve[y][i]) == 2:
                        #list of length 2 repeats twice
                        j = self.solve[y][i+1:].index(self.solve[y][i])+i+1 #the other index
                        j_used.append(j)
                        tot = [0,0,0,0,0,0,0,0,0,0]
                        for k in range(9): #for each index in row
                            for p in range(len(self.solve[y][k])): #for each possible number in the index
                                tot[self.solve[y][k][p]]+=1 #store index of that number
                        if tot[self.solve[y][i][0]]!=2 and tot[self.solve[y][i][1]]!=2:
                            rem = self.solve[y][i]
                            exc = [i,j]
                            self.removeRow(rem,y,exc)
                            self.change = True
        for x in range(9):
            j_used = [] #initialize for the loop
            col_solve = [[],[],[],[],[],[],[],[],[]]
            for i in range(9): #each index of the column
                col_solve[i] = self.solve[i][x]
            for i in range(9): #each index of the column
                if j_used.count(i)==0: #hasn't been searched yet
                    if col_solve.count(col_solve[i]) == 2 and len(col_solve[i]) == 2:
                        #list of length 2 repeats twice
                        j = col_solve[i+1:].index(col_solve[i])+1+i #the other index
                        j_used.append(j)
                        tot = [0,0,0,0,0,0,0,0,0,0]
                        for k in range(9): #for each index in row
                            for p in range(len(col_solve[k])): #for each possible number in the index
                                tot[col_solve[k][p]]+=1 #store index of that number
                        if tot[col_solve[i][0]]!=2 and tot[col_solve[i][1]]!=2:
                            rem = col_solve[i]
                            exc = [i,j]
                            self.removeColumn(rem,x,exc)
                            self.change = True
        for x in range(3):
            for y in range(3):
                j_used = [] #initialize for the loop
                cell_solve = [[],[],[],[],[],[],[],[],[]]
                cell_solve[0:3] = self.solve[y*3][x*3:x*3+3]
                cell_solve[3:6] = self.solve[y*3+1][x*3:x*3+3]
                cell_solve[6:9] = self.solve[y*3+2][x*3:x*3+3]
                for i in range(9): #each index of the column
                    if j_used.count(i)==0: #hasn't been searched yet
                        if cell_solve.count(cell_solve[i]) == 2 and len(cell_solve[i]) == 2:
                            #list of length 2 repeats twice
                            j = cell_solve[i+1:].index(cell_solve[i])+1+i #the other index
                            j_used.append(j)
                            tot = [0,0,0,0,0,0,0,0,0,0]
                            for k in range(9): #for each index in row
                                for p in range(len(cell_solve[k])): #for each possible number in the index
                                    tot[cell_solve[k][p]]+=1 #store index of that number
                            if tot[cell_solve[i][0]]!=2 and tot[cell_solve[i][1]]!=2:
                                exc = [[y*3+i/3,x*3+i%3],[y*3+j/3,x*3+j%3]]
                                rem = cell_solve[i]
                                xcell = [x*3,x*3+1,x*3+2]
                                ycell = [y*3,y*3+1,y*3+2]
                                self.removeCell(rem,xcell,ycell,exc)
                                self.change = True

    def hiddenPairsElimination(self):
        #similar to pairsElimination but searches for hidden pairs instead, takes longer
        print "---HIDDEN PAIRS ELIMINATION---"
        for y in range(9): #for each row
            #represents where that number is possible in the row
            pos = [[],[],[],[],[],[],[],[],[],[]] #first index not used
            for i in range(9): #for each index in row
                for j in range(len(self.solve[y][i])): #for each possible number in the index
                    pos[self.solve[y][i][j]].append(i) #store index of that number
            j_used = [] #initialize for the loop
            for i in range(1,10): #for every number 1-9
                if j_used.count(i)==0: #hasn't been searched before
                    if pos.count(pos[i]) == 2 and len(pos[i])==2: #and there are two matching pairs
                        j = pos[i+1:].index(pos[i])+i+1
                        j_used.append(j)
                        #i.e. two different numbers can only appear in the same two spots
                        #now we know all other instances of that number anywhere else can be removed
                        keep = [i,j]
                        newchange = False
                        if self.solve[y][pos[i][0]] != keep:
                            self.solve[y][pos[i][0]] = keep
                            self.change = True
                            newchange = True
                        if self.solve[y][pos[i][1]] != keep:
                            self.solve[y][pos[i][1]] = keep
                            self.change = True
                            newchange = True
                            
        for x in range(9): #for each col
            #represents where that number is possible in the row
            pos = [[],[],[],[],[],[],[],[],[],[]] #first index not used
            for i in range(9): #for each index in col
                for j in range(len(self.solve[i][x])): #for each possible number in the index
                    pos[self.solve[i][x][j]].append(i) #store index of that number
            j_used = [] #initialize for the loop
            for i in range(1,10): #for every number 1-9
                if j_used.count(i)==0: #hasn't been searched before
                    if pos.count(pos[i]) == 2 and len(pos[i])==2: #and there are two matching pairs
                        j = pos[i+1:].index(pos[i])+i+1
                        j_used.append(j)
                        #ie. two different numbers can only appear in the same two spots
                        #now we know all other instances of that number anywhere else can be removed
                        keep = [i,j]
                        newchange = False
                        if self.solve[pos[i][0]][x] != keep:
                            self.solve[pos[i][0]][x] = keep
                            self.change = True
                            newchange = True
                        if self.solve[pos[i][1]][x] != keep:
                            self.solve[pos[i][1]][x] = keep
                            self.change = True
                            newchange = True
        xcell = [0,1,2]
        ycell = [0,1,2]
        go = True
        while go:
            #represents where that number is possible in the row
            pos = [[],[],[],[],[],[],[],[],[],[]] #first index not used
            for x in xcell:
                for y in ycell:
                    for j in range(len(self.solve[y][x])): #for each possible number in the index
                        pos[self.solve[y][x][j]].append([y,x]) #store [y,x] of that number
            j_used = []
            for i in range(1,10): #for every number 1-9
                if j_used.count(i)==0: #hasn't been searched before
                    if pos.count(pos[i]) == 2 and len(pos[i])==2: #and there are two matching pairs
                        j = pos[i+1:].index(pos[i])+i+1
                        j_used.append(j)
                        #ie. two different numbers can only appear in the same two spots
                        #now we know all other instances of that number anywhere else can be removed
                        keep = [i,j]
                        y1 = pos[i][0][0]
                        x1 = pos[i][0][1]
                        y2 = pos[i][1][0]
                        x2 = pos[i][1][1]
                        newchange = False
                        if self.solve[y1][x1] != keep:
                            self.solve[y1][x1] = keep
                            self.change = True
                            newchange = True
                        if self.solve[y2][x2] != keep:
                            self.solve[y2][x2] = keep
                            self.change = True
                            newchange = True
            #determine next cell or exit the while loop
            for i in range(3):
                ycell[i] += 3
                if ycell[0] == 9:
                    for i in range(3):
                        xcell[i] += 3
                        ycell[i] -= 9
                if xcell[0] == 9:
                    go = False

    def maskElimination(self,mask,x,y):
        #used with deep_elim
        mask[x,:] = -1 #change entire row to mask=-1
        mask[:,y] = -1 #change entire col to mask=-1
        mask[(x/3)*3:(x/3)*3+3,(y/3)*3:(y/3)*3+3] = -1

    def deepElimination(self):
        #DEEPER CROSS-CHECKING BETWEEN ROW/COL/BOX IS POSSIBLE
        #ALSO THIS COULD READ FROM SOLVE
        #analyzes entire puzzle once for each number 1-9 in an
        #attempt to combine row slicing, column slicing, and boxing methods
        print "---DEEP ELIMINATION---"
        for n in range(1,10): #for each number 1-9
            mask = np.zeros((9,9),np.int8)
            taken = np.transpose(np.nonzero(self.current)) #coordinate pairs of nonzeros
            for i in taken:
                x = i[0]
                y = i[1]
                mask[x,y] = -1 #if non zero change mask=-1
                if self.current[x,y] == n: #if non zero number is n
                    self.maskElimination(mask,x,y)
            x = 0 #initialize x
            while x<9: #search every row
                if np.count_nonzero(mask[x,:]) == 8: #if only one spot is open
                    y = np.argmax(mask[x,:]) #finds index of the single zero
                    mask[x,y] = -1
                    self.current[x,y] = n #set new number in main puzzle
                    self.change = True
                    self.maskElimination(mask,x,y)
                    x = -1 #start back from beginning
                x+=1
            y = 0 #initialize y
            while y<9: #search every col
                if np.count_nonzero(mask[:,y]) == 8: #if only one spot is open
                    x = np.argmax(mask[:,y]) #finds index of the single zero
                    mask[x,y] = -1
                    self.current[x,y] = n #set new number in main puzzle
                    self.change = True
                    self.maskElimination(mask,x,y)
                    y = -1 #start back from beginning
                y+=1
            newchange = True
            while newchange==True:
                newchange = False
                for x in range(3):
                    for y in range(3):
                        if np.count_nonzero(mask[x*3:x*3+3,y*3:y*3+3].flatten()) == 8:
                            i = np.argmax(mask[x*3:x*3+3,y*3:y*3+3].flatten())
                            xycd = [x*3+i/3,y*3+i%3]
                            mask[xycd[0],xycd[1]] = -1
                            self.current[xycd[0],xycd[1]] = n
                            self.change = True
                            self.maskElimination(mask,xycd[0],xycd[1])
                            newchange = True #start back from beginning
                            self.change = True

    def guessElimination(self,image):
        #brute force random guessing
        self.change = True
        if self.guess == False:
            self.guess = True
            self.solveBackup = copy.deepcopy(self.solve)
            self.currentBackup = np.copy(self.current)
        i = 0
        while True:
            i+=1
            ri = rn.randint(0,8)
            rj = rn.randint(0,8)
            if len(self.solve[ri][rj])==2:
                rpick = rn.randint(0,1)
                print "solve was:",self.solve[ri][rj]
                print "2:making new guess of",self.solve[ri][rj][rpick]," at ",ri,rj
                self.solve[ri][rj]=[self.solve[ri][rj][rpick]]
                break
            if len(self.solve[ri][rj])==3 and i>100:
                rpick = rn.randint(0,2)
                print "solve was:",self.solve[ri][rj]
                print "3:making new guess of",self.solve[ri][rj][rpick]," at ",ri,rj
                self.solve[ri][rj]=[self.solve[ri][rj][rpick]]
                break
            if len(self.solve[ri][rj])==4 and i>200:
                rpick = rn.randint(0,3)
                print "solve was:",self.solve[ri][rj]
                print "4:making new guess of",self.solve[ri][rj][rpick]," at ",ri,rj
                self.solve[ri][rj]=[self.solve[ri][rj][rpick]]
                break
            if i>300:
                self.change = False
                print "no guesses to be made?"
                break

    def guessRestart(self,image):
        #make a new guess after an initial guess proved incorrect
        print "bad guess made, restarting guess..."
        #restore backup
        self.solve = copy.deepcopy(self.solveBackup)
        self.current = np.copy(self.currentBackup)
        image.output = np.copy(image.outputBackup)
        #make a new guess
        self.guessElimination(image)


class imageClass:
    #this class defines all of the important image matrices, and information about the images.
    #also the methods associated with capturing input, displaying the output,
    #and warping and transforming any of the images to assist with OCR
    def __init__(self):
        #.captured is the initially captured image
        self.captured = []
        #.gray is the grayscale captured image
        self.gray = []
        #.thres is after adaptive thresholding is applied
        self.thresh = []
        #.contours contains information about the contours found in the image
        self.contours = []
        #.biggest contains a set of four coordinate points describing the
        #contours of the biggest rectangular contour found
        self.biggest = None;
        #.maxArea is the area of this biggest rectangular found
        self.maxArea = 0
        #.output is an image resulting from the warp() method
        self.output = []
        self.outputBackup = []
        self.outputGray = []
        #.mat is a matrix of 100 points found using a simple gridding algorithm
        #based on the four corner points from .biggest
        self.mat = np.zeros((100,2),np.float32)
        #.reshape is a reshaping of .mat
        self.reshape = np.zeros((100,2),np.float32)
        
    def captureImage(self,status):
        #captures the image and finds the biggest rectangle

        self.video_capture = cv2.VideoCapture(0)

        self.ret, self.frame = self.video_capture.read()
        
        self.captured = cv2.resize(self.frame, (600, 600))            
        #convert to grayscale
        self.gray = cv2.cvtColor(self.captured, cv2.COLOR_BGR2GRAY)

        #noise removal with gaussian blur
        self.gray = cv2.GaussianBlur(self.gray,(5,5),0)
        #then do adaptive thresholding
        self.thresh = cv2.adaptiveThreshold(self.gray,255,1,1,11,2)

        #find countours in threshold image
        self.contours, hierarchy = cv2.findContours(self.thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        #evaluate all blobs to find blob with biggest area
        #biggest rectangle in the image must be sudoku square
        self.biggest = None
        self.maxArea = 0
        for i in self.contours:
            area = cv2.contourArea(i)
            if area > 50000: #50000 is an estimated value for the kind of blob we want to evaluate
                peri = cv2.arcLength(i,True)
                approx = cv2.approxPolyDP(i,0.02*peri,True)
                if area > self.maxArea and len(approx)==4:
                    self.biggest = approx
                    self.maxArea = area
                    best_cont = i
        if self.maxArea > 0:
            status.noDetect = 0 #reset
            status.detect += 1
            print ("Puzzle Found!")
            #draw self.biggest approx contour
            if status.completed:
                cv2.polylines(self.captured,[self.biggest],True,(0,255,0),3) 
            elif status.puzzleFound:
                cv2.polylines(self.captured,[self.biggest],True,(0,255,255),3) 
            else:
                cv2.polylines(self.captured,[self.biggest],True,(0,0,255),3)
            self.reorder() #reorder self.biggest
        else:
            status.noDetect += 1
            if status.noDetect == 20:
                print "No sudoku puzzle detected!"
            if status.noDetect > 50:
                status.restart = True
        if status.detect == 20:
                status.puzzleFound = True
                print "Sudoku puzzle detected!"
        if status.beginSolver == False or self.maxArea == 0:
            self.capturedDisplay = cv2.resize(self.captured, (0, 0), fx=0.65, fy=0.65)
            cv2.imshow('sudoku', self.capturedDisplay)
            key = cv2.waitKey(10)
            if key==27:
                sys.exit()
    
    def reorder(self):
        #reorders the points obtained from finding the biggest rectangle
        #[top-left, top-right, bottom-right, bottom-left]
        a = self.biggest.reshape((4,2))
        b = np.zeros((4,2),dtype = np.float32)
     
        add = a.sum(1)
        b[0] = a[np.argmin(add)] #smallest sum
        b[2] = a[np.argmax(add)] #largest sum
             
        diff = np.diff(a,axis = 1) #y-x
        b[1] = a[np.argmin(diff)] #min diff
        b[3] = a[np.argmax(diff)] #max diff
        self.biggest = b

    def perspective(self):
        #create 100 points using "biggest" and simple gridding algorithm,
        #these 100 points define the grid of the sudoku puzzle
        #topLeft-topRight-bottomRight-bottomLeft = "biggest"
        b = np.zeros((100,2),dtype = np.float32)
        c_sqrt=10
        if self.biggest == None:
            self.biggest = [[0,0],[640,0],[640,480],[0,480]]
        tl,tr,br,bl = self.biggest[0],self.biggest[1],self.biggest[2],self.biggest[3]
        for k in range (0,100):
            i = k%c_sqrt
            j = k/c_sqrt
            ml = [tl[0]+(bl[0]-tl[0])/9*j,tl[1]+(bl[1]-tl[1])/9*j]
            mr = [tr[0]+(br[0]-tr[0])/9*j,tr[1]+(br[1]-tr[1])/9*j]
##            self.mat[k,0] = ml[0]+(mr[0]-ml[0])/9*i
##            self.mat[k,1] = ml[1]+(mr[1]-ml[1])/9*i
            self.mat.itemset((k,0),ml[0]+(mr[0]-ml[0])/9*i)
            self.mat.itemset((k,1),ml[1]+(mr[1]-ml[1])/9*i)
        self.reshape = self.mat.reshape((c_sqrt,c_sqrt,2))

    def warp(self):
        #take distorted image and warp to flat square for clear OCR reading
        mask = np.zeros((self.gray.shape),np.uint8)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(11,11))
        close = cv2.morphologyEx(self.gray,cv2.MORPH_CLOSE,kernel)
        division = np.float32(self.gray)/(close)
        result = np.uint8(cv2.normalize(division,division,0,255,cv2.NORM_MINMAX))
        result = cv2.cvtColor(result,cv2.COLOR_GRAY2BGR)
        output = np.zeros((450,450,3),np.uint8)
        c_sqrt=10
        for i,j in enumerate(self.mat):
            ri = i/c_sqrt
            ci = i%c_sqrt
            if ci != c_sqrt-1 and ri != c_sqrt-1:
                source = self.reshape[ri:ri+2, ci:ci+2 , :].reshape((4,2))
                dest = np.array( [ [ci*450/(c_sqrt-1),ri*450/(c_sqrt-1)],[(ci+1)*450/(c_sqrt-1),
                            ri*450/(c_sqrt-1)],[ci*450/(c_sqrt-1),(ri+1)*450/(c_sqrt-1)],
                            [(ci+1)*450/(c_sqrt-1),(ri+1)*450/(c_sqrt-1)] ], np.float32)
                trans = cv2.getPerspectiveTransform(source,dest)
                warp = cv2.warpPerspective(result,trans,(450,450))
                output[ri*450/(c_sqrt-1):(ri+1)*450/(c_sqrt-1) , ci*450/(c_sqrt-1):(ci+1)*450/
                       (c_sqrt-1)] = warp[ri*450/(c_sqrt-1):(ri+1)*450/(c_sqrt-1) ,
                        ci*450/(c_sqrt-1):(ci+1)*450/(c_sqrt-1)].copy()
        output_backup = np.copy(output)
        key = cv2.waitKey(1)
        self.output = output
        self.outputBackup = output_backup

    def virtualImage(self,puzzle):
        #output known sudoku values to the real image
        j = 0
        tsize = (math.sqrt(self.maxArea))/400
        w = int(20*tsize)
        h = int(25*tsize)
        for i in range(100):
##            x = int(self.mat[i][0]+8*tsize)
##            y = int(self.mat[i][1]+8*tsize)
            x = int(self.mat.item(i,0)+8*tsize)
            y = int(self.mat.item(i,1)+8*tsize)
            if i%10!=9 and i/10!=9:
                yc = j%9
                xc = j/9
                j+=1
                if puzzle.original[xc,yc]==0 and puzzle.current[xc,yc]!=0 and puzzle.selected[xc, yc] == 1:
                    string = str(puzzle.current[xc,yc])
                    cv2.putText(self.captured,string,(x+w/4,y+h),0,tsize,(0,0,0),2)
        self.capturedDisplay = cv2.resize(self.captured, (0, 0), fx=0.65, fy=0.65)
        cv2.imshow('sudoku',self.capturedDisplay)
        key = cv2.waitKey(10)
        if key==27:
            sys.exit()

class OCRmodelClass:
    #this class defines the data used for OCR,
    #and the associated methods for performing OCR
    def __init__(self):
        samples = np.loadtxt('generalsamples.data',np.float32)
        responses = np.loadtxt('generalresponses.data',np.float32)
        responses = responses.reshape((responses.size,1))
        #.model uses kNearest to perform OCR
        self.model = cv2.KNearest()
        self.model.train(samples,responses)
        #.iterations contains information on what type of morphology to use
        self.iterations = [-1,0,1,2]
        self.lvl = 0 #index of .iterations
        
    def OCR(self,status,image,puzzle):
        #preprocessing for OCR
        #convert image to grayscale
        gray = cv2.cvtColor(image.output, cv2.COLOR_BGR2GRAY)
        #noise removal with gaussian blur
        gray = cv2.GaussianBlur(gray,(5,5),0)
        image.outputGray = gray
        
        #attempt to read the image with 4 different morphology values and find the best result
        self.success = [0,0,0,0]
        self.errors = [0,0,0,0]
        for self.lvl in self.iterations:
            image.output = np.copy(image.outputBackup)
            self.OCR_read(status,image,puzzle)
            if self.errors[self.lvl+1]==0:
                self.errors[self.lvl+1] = puzzle.checkSolution()
        best = 8
        for i in range(4):
            if self.success[i] > best and self.errors[i]>=0:
                best = self.success[i]
                ibest = i
        print "success:",self.success
        print "errors:",self.errors
        
        if best==8:
            print "ERROR - OCR FAILURE"
            status.restart = True
        else:
            print "final morph erode iterations:",self.iterations[ibest]
            image.output = np.copy(image.outputBackup)
            self.lvl = self.iterations[ibest]
            self.OCR_read(status,image,puzzle)
            key = cv2.waitKey(1)

    def OCR_read(self,status,image,puzzle):
        #perform actual OCR using kNearest model
        thresh = cv2.adaptiveThreshold(image.outputGray,255,1,1,7,2)
        if self.lvl >= 0:
            morph = cv2.morphologyEx(thresh,cv2.MORPH_ERODE,None,iterations = self.lvl)
        elif self.lvl == -1:
            morph = cv2.morphologyEx(thresh,cv2.MORPH_DILATE,None,iterations = 1)

        thresh_copy = morph.copy()
        #thresh2 changes after findContours
        contours,hierarchy = cv2.findContours(morph,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        thresh = thresh_copy

        puzzle.current = np.zeros((9,9),np.uint8)

        # testing section
        for cnt in contours:
            if cv2.contourArea(cnt)>20:
                [x,y,w,h] = cv2.boundingRect(cnt)
                if  h>20 and h<40 and w>8 and w<40:
                    if w<20:
                        diff = 20-w
                        x -= diff/2
                        w += diff
                    sudox = x/50
                    sudoy = y/50
                    cv2.rectangle(image.output,(x,y),(x+w,y+h),(0,0,255),2)
                    #prepare region of interest for OCR kNearest model
                    roi = thresh[y:y+h,x:x+w]
                    roismall = cv2.resize(roi,(25,35))
                    roismall = roismall.reshape((1,875))
                    roismall = np.float32(roismall)
                    #find result
                    retval, results, neigh_resp, dists = self.model.find_nearest(roismall, k = 1)
                    #check for read errors
                    if results[0][0]!=0:
                        string = str(int((results[0][0])))
                        if puzzle.current[sudoy,sudox]==0:
                            puzzle.current[sudoy,sudox] = int(string)
                        else:
                            self.errors[self.lvl+1]=-2 #double read error
                        self.success[self.lvl+1]+=1
                        cv2.putText(image.output,string,(x,y+h),0,1.4,(255,0,0),3)
                    else:
                        self.errors[self.lvl+1]=-3 #read zero error
                    

class solverStatusClass:
    #this class defines the status of the main loop
    def __init__(self):
        #.beginSolver becomes true when the puzzle is completely captured and ready to solve
        self.beginSolver = False
        #.puzzleFound becomes true when the puzzle is thought to be found but not yet read with OCR
        self.puzzleFound = False
        #.puzzleRead becomes true when OCR has confirmed the puzzle
        self.puzzleRead = False
        #.restart becomes true when the main loop needs to restart
        self.restart = False
        #.completed becomes true when the puzzle has been solved
        self.completed = False
        #.number of times imageClass.captureImage() detects no puzzle
        self.noDetect = 0
        #.number of times imageClass.captureImage() detects a puzzle
        self.detect = 0

def main():
    reader = OCRmodelClass()
    while True:
        status = solverStatusClass()
        while status.beginSolver == False:
            status = solverStatusClass()
            puzzle = puzzleStatusClass()
            image = imageClass()
            print "Waiting for puzzle..."
            while status.puzzleFound == False:
                image.captureImage(status)
                if status.restart == True:
                    break
            while status.puzzleRead == False and status.puzzleFound == True:
                image.captureImage(status)
                image.perspective()
                image.warp()
                reader.OCR(status,image,puzzle)
                if status.restart == True:
                    print "Restarting..."
                    break
                elif np.array_equal(puzzle.current,puzzle.last):
                    status.beginSolver = True
                    status.puzzleRead = True
                else:
                    print "Rechecking for Puzzle Match..."
                    puzzle.last = np.copy(puzzle.current)

        print "Starting Solver..."
        start_time = time.time()
        puzzle.original = np.copy(puzzle.current)
        puzzle.prepSolve()
        
        while puzzle.change:
            t1 = time.time()
            image.captureImage(status)
            t2 = time.time()
            image.perspective()
            t3 = time.time()
            image.virtualImage(puzzle)
            t4 = time.time()
            if np.count_nonzero(puzzle.current) == 81 and puzzle.guess==False:
                break
            puzzle.change = False
            puzzle.simpleElimination()
            print "Change:",puzzle.change
            if puzzle.change:
                puzzle.newSolve()
                err = puzzle.checkSolution()
                print "exit flag:",err
                if err == -1:
                    if puzzle.guess == False:
                        break
                    else:
                        puzzle.guessRestart(image)
            else:
                puzzle.deepElimination()
                print "Change:",puzzle.change
                if puzzle.change:
                    puzzle.newSolve()
                    err = puzzle.checkSolution()
                    print "exit flag:",err
                    if err == -1:
                        if puzzle.guess == False:
                            break
                        else:
                            puzzle.guessRestart(image)
                else:
                    puzzle.pairsElimination()
                    print "Change:",puzzle.change
                    if puzzle.change:
                        puzzle.newSolve()
                        err = puzzle.checkSolution()
                        print "exit flag:",err
                        if err == -1:
                            if puzzle.guess == False:
                                break
                            else:
                                puzzle.guessRestart(image)
                    else:
                        puzzle.hiddenPairsElimination()
                        print "Change:",puzzle.change
                        if puzzle.change:
                            puzzle.newSolve()
                            err = puzzle.checkSolution()
                            print "exit flag:",err
                            if err == -1:
                                if puzzle.guess == False:
                                    break
                                else:
                                    puzzle.guessRestart(image)
                        else:
                            err = puzzle.checkSolution()
                            if err == 0:
                                break
                            else:
                                puzzle.guessElimination(image)
                                puzzle.newSolve()
                                err = puzzle.checkSolution()
                                print "exit flag:",err
                                while err == -1:
                                    puzzle.guessRestart(image)
                                    puzzle.newSolve()
                                    err = puzzle.checkSolution()
                                    print "exit flag:",err
                                    
            #continuation of: while puzzle.change:
            t5 = time.time()
            print "capture time: ",t2-t1
            print "perspective time: ",t3-t2
            print "virtual time: ",t4-t3
            print "solve loop time: ", t5-t4
            
        #continuation of: while True::                     
        err = puzzle.checkSolution()
        print "exit flag:",err
        elapsed = time.time() - start_time
        print "elapsed time: ",elapsed
        if err==0:
            print "SOLVED!"
            status.completed = True
        while status.completed == True:
            #final loop to be run after puzzle is solved
            t1 = time.time()
            image.captureImage(status)
            if status.restart == True:
                print "Restarting..."
                break
            t2 = time.time()
            print "capture time: ",t2-t1
            if image.maxArea > 0:
                image.perspective()
                t3 = time.time()
                print "perspective time: ",t3-t2
                image.virtualImage(puzzle)
                t4 = time.time()
                print "virtual time: ",t4-t3


if __name__ == '__main__': main()
