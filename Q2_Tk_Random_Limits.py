import random
import tkinter as tk
import tkinter.messagebox
from tkinter import *
from tkinter import font

root = tk.Tk()
root.title("TUS Midlands")
myfont1 = font.Font(family = "Calibri", size = 16, weight = "normal")
myfont2 = font.Font(family = "Calibri", size = 14, weight = "normal")
randVar = IntVar()

low = StringVar()
low.set(1)
high = StringVar()
high.set(100)

def generateRandomNumber(l, h):
    if (l > h):
        tkinter.messagebox.showinfo("Inversion of values", "Careful, the lower range must be a lower integer value"
                                                           " than the upper range value.\nI have swapped them around to resolve this.")
        low.set(h)
        high.set(l)
        return random.randint(int(h),int(l))
    else:
        return random.randint(l,h)


def newRandNum():
    lower = checkNumeric(low.get())
    upper = checkNumeric(high.get())
    if all([lower, upper]) ==False:
        tkinter.messagebox.showwarning("Oops.", "Something is wrong with the inputs, are they numberic?")
    else:
        randVar.set(generateRandomNumber(int(low.get()), int(high.get())))


def convertToNumeric(val):
    return int(val)


def checkNumeric(val):
    try:
        val = int(val)
        print("{0} \t {1} \t {2}".format(val, type(val), isinstance(val, int)))
        return val
    except ValueError:
        tkinter.messagebox.showwarning("Oops.", "Something went wrong with this entry: "
                                       + val + "\nIt does not seem to be an integer.")



def closeApplication():
    print('closing')
    root.destroy()

def main():
    # Code to add widgets will go here
    # Title label for the GUI
    l1 = tk.Label(root, text = "Random Number Generator", font = myfont1)
    l1.grid(row=0, column=0, columnspan=2, sticky = tk.N+tk.S+tk.E+tk.W)

    # label, entry pair (low)
    l2 = tk.Label(root, text = "Lower Limit", font = myfont2)
    l2.grid(row=1, column=0, sticky = tk.N+tk.S+tk.E+tk.W)
    e1 = tk.Entry(root, textvariable = low, font = myfont2)
    e1.grid(row=1, column=1, sticky=tk.W)

    # label, entry pair (high)
    l3 = tk.Label(root, text = "Upper Limit", font = myfont2)
    l3.grid(row=2, column=0, sticky = tk.N+tk.S+tk.E+tk.W)
    e2 = tk.Entry(root, textvariable = high, font = myfont2)
    e2.grid(row=2, column=1, sticky=tk.W)

    # label, entry pair
    l4 = tk.Label(root, text = "Random Number", font = myfont2)
    l4.grid(row=3, column=0, sticky = tk.N+tk.S+tk.E+tk.W)
    e3 = tk.Entry(root, textvariable = randVar, font = myfont2)
    e3.grid(row=3, column=1, sticky=tk.W)
    e3.configure(state="disabled")  # disable the entry field

    # Buttons to generate a new random number or close application
    newRand = tk.Button(root, text = "Generate New", font = myfont2, command = newRandNum)
    newRand.grid(row=4, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
    closeApp = tk.Button(root, text="Close App", font = myfont2, command = closeApplication)
    closeApp.grid(row=4, column=1, sticky=tk.N+tk.S+tk.E+tk.W)

    randVar.set(generateRandomNumber(1,100))
    root.mainloop()


if __name__ == "__main__":
    main()



