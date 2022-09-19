from tkinter import *
from tkinter import ttk
import ScreenManager
import time, threading
import math
class Overlay():
    def __init__(self) -> None:
        self.root = Tk()
        self.text = ""
        self.animationDone = False
        # tkinter set wndows at specified location 
        self.root.geometry("287x81")
        self.root.resizable(False, False)
        # hide action bar
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        #change background color to red to make it visible
        self.root.configure(background='green')
        
        self.width = 257
        self.height = 81
        #update screen size
        ScreenManager.UpdateScreenSize()
        self.settings = {
            "x": int("-" + str(self.width)),
            "y": 10,
        }
        self.root.geometry("+{}+{}".format(self.settings["x"], self.settings["y"]))

    def setting(self, name, value):
        self.settings[name] = value

    def SetBackgroundImage(self, imagePath):
        # set background image
        Label(self.root, image=imagePath).pack()

    def Animation(self):
        # make sure the window is on top and visible
        self.root.update()
        self.root.deiconify()
        self.root.lift()

        self.root.attributes("-topmost", True)
        #get fraction result without decimal
        fraction = math.floor(self.width /4 )
        for _ in range(fraction):
            #get actual x and add 1 to it
            self.settings["x"] = self.settings["x"] + 4
            self.root.geometry("+{}+{}".format(self.settings["x"], self.settings["y"]))
            self.root.update()
            self.root.after(2)
        time.sleep(3)
        for _ in range(fraction):
            #get actual x and add 1 to it
            self.settings["x"] = self.settings["x"] - 4
            self.root.geometry("+{}+{}".format(self.settings["x"], self.settings["y"]))
            self.root.update()
            self.root.after(2)
        self.root.quit()

    def SetText(self, text):
        self.text = text
        
    def show(self):
        #set the text in center of the window and set background color to the same as the window
        
        Label(self.root, text=self.text, font=("Helvetica", 5+(20-(len(self.text)))), fg="#FFF", bg=self.root.cget("bg")).place(relx=0.5, rely=0.5, anchor=CENTER)

        """self.root.update()
        self.root.deiconify()
        self.root.lift()"""
        threading.Thread(target=self.Animation).start()
        self.root.mainloop()
