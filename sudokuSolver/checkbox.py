from Tkinter import *


class CheckBoxGrid(Frame):
    def __init__ (self, master, rows, cols, **kw):
        Frame.__init__(self, master)
        self.checks = []
        for nRows in range(rows):
            cCols = []
            for nCols in range(cols):
                currentCell = IntVar()
                cCols.append(currentCell)
                Checkbutton(self, variable=currentCell).grid(row=nRows, column=nCols)
            self.checks.append(cCols)
        btnOne = Button(root, text="One", command=self.ButtonOne)
        btnOne.grid()
        btnTwo = Button(root, text="Two", command=self.ButtonTwo)
        btnTwo.grid()
    def ButtonOne(self):
        print (self.getValue(1, 1))
    def ButtonTwo(self):
        for r in self.checks:
            for c in r:
                print(c.get())
    def getValue(self, row, column):
        return self.checks([row][column].get())

if __name__ == '__main__':
    root = Tk()
    root.geometry('{}x{}'.format(800, 480))
    c = CheckBoxGrid(root, 9, 9)
    c.grid()
    root.mainloop()
