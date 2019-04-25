#!/usr/bin/python

from __future__ import print_function
try:
    from Tkinter import *
except:
    from tkinter import *


import pydbus
from time import sleep

class MediaPlayer:
    def __init__(self):
        self.service = pydbus.SystemBus().get('org.bluez', '/')
        self.Start()

    def Start(self):
        print('Connecting to Media Player...')
        self.ConnectMediaPlayer()

    def ConnectMediaPlayer(self):
        player_connected = False
        while player_connected is not True:
            obj_list = self.service.GetManagedObjects()
            for obj_path in obj_list.keys():
                if "player" in obj_path:
                    self.player_path = obj_path
                    self.device_path = obj_list[self.player_path]['org.bluez.MediaPlayer1']['Device']
                    self.device_name = obj_list[self.device_path]['org.bluez.Device1']['Alias']
                    player_connected = obj_list[self.device_path]['org.bluez.MediaControl1']['Connected']
                    break
            sleep(0.2)

        self.media_player = pydbus.SystemBus().get('org.bluez', self.player_path)
        print('Media Player successfully Connected!     Device Name: ',end=' ')
        print(self.device_name)
        self.CreateWindow()

    def CheckConnection(self):
        obj_list = self.service.GetManagedObjects()
        if self.player_path in obj_list and obj_list[self.device_path]['org.bluez.MediaControl1']['Connected'] is True:
            self.root.after(200,self.CheckConnection)
        else:
            print('Media Player was disconnected!           Device Name: ',end=' ')
            print(self.device_name)
            print()
            self.root.destroy()
            self.Start()

    def Play(self,event):
        self.media_player.Play()

    def Pause(self,event):
        self.media_player.Pause()

    def Next(self,event):
        self.media_player.Next()

    def Previous(self,event):
        self.media_player.Previous()

    def CreateWindow(self):
        self.root = Tk()
        self.root.geometry('250x125')
        self.root.title('BTMediaControl')
        self.frame = Frame(self.root,width=500,height=200)

        #Buttons
        self.PlayButton = Button(self.frame,text="Play")
        self.PlayButton.bind('<Button-1>',self.Play)
        self.PlayButton.pack(side=TOP,fill=X)

        self.PauseButton = Button(self.frame,text="Pause")
        self.PauseButton.bind('<Button-1>',self.Pause)
        self.PauseButton.pack(side=TOP,fill=X)

        self.NextButton = Button(self.frame,text="Next")
        self.NextButton.bind('<Button-1>',self.Next)
        self.NextButton.pack(side=TOP,fill=X)

        self.PreviousButton = Button(self.frame,text="Previous")
        self.PreviousButton.bind('<Button-1>',self.Previous)
        self.PreviousButton.pack(side=TOP,fill=X)

        self.root.resizable(0,0)
        self.frame.pack()
        self.root.after(200,self.CheckConnection)
        self.root.mainloop()


player = MediaPlayer()
