try:
    from Tkinter import *
except:
    from tkinter import *

import threading
import pydbus

class MediaPlayer:
    def __init__(self):
        self.service = pydbus.SystemBus().get('org.bluez', '/')
        self.ConnectMediaPlayer()

    def ConnectMediaPlayer(self):
        obj_list = self.service.GetManagedObjects()
        for obj_name in obj_list.keys():
            if "player" in obj_name:
                self.media_player_object = obj_name
                print(" Device Address: " + obj_list[self.media_player_object]['org.bluez.MediaPlayer1']['Device'])
                print(" Player:         " + self.media_player_object)
                self.media_player = pydbus.SystemBus().get('org.bluez', self.media_player_object)
                break

    def Play(self,event):
        self.media_player.Play()

    def Pause(self,event):
        self.media_player.Pause()

    def Next(self,event):
        self.media_player.Next()

    def Previous(self,event):
        self.media_player.Previous()

player = MediaPlayer()

root = Tk()
root.geometry('250x125')
root.title('BTMediaControl')
frame = Frame(root,width=500,height=200)

#Buttons
PlayButton = Button(frame,text="Play")
PlayButton.bind('<Button-1>',player.Play)
PlayButton.pack(side=TOP,fill=X)

PauseButton = Button(frame,text="Pause")
PauseButton.bind('<Button-1>',player.Pause)
PauseButton.pack(side=TOP,fill=X)

PauseButton = Button(frame,text="Next")
PauseButton.bind('<Button-1>',player.Next)
PauseButton.pack(side=TOP,fill=X)

PauseButton = Button(frame,text="Previous")
PauseButton.bind('<Button-1>',player.Previous)
PauseButton.pack(side=TOP,fill=X)

root.resizable(0,0)
frame.pack()
root.mainloop()
