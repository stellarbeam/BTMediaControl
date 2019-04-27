#!/usr/bin/python3

from time import sleep
from threading import Thread
from gi.repository.GLib import MainLoop, timeout_add
from gui import Window

import pydbus

class MediaPlayer:
    def __init__(self):

        self.DefineFunctionArgList()

        self.service = pydbus.SystemBus().get('org.bluez', '/')
        self.Update_obj_list()

        self.player_connected = False
        self.TerminateFlag = False

        self.obj_list_updater_thread = Thread(target=self.ObjListUpdater)
        self.track_info_updater_thread = Thread(target=self.TrackInfoUpdater)

        self.obj_list_updater_thread.start()
        self.track_info_updater_thread.start()

        self.Start()

    def ObjListUpdater(self):
        self.system_bus = pydbus.SystemBus()
        self.system_bus.subscribe(sender='org.bluez',signal='PropertiesChanged',signal_fired=self.Update_obj_list)

        loop = MainLoop()
        timeout_add(100,self.checkTerminate,loop)
        loop.run()

    def Update_obj_list(self, *args):
        self.obj_list = self.service.GetManagedObjects()

    def TrackInfoUpdater(self): # To be used by gui
        while self.TerminateFlag is False:
            try:
                self.pos = self.media_player.Get('org.bluez.MediaPlayer1','Position')
                self.track_info = self.media_player.Get('org.bluez.MediaPlayer1','Track')
            except:
                self.pos = 0
                self.track_info = {
                    'Title'   :''  ,
                    'Duration':0   ,
                    'Album'   :''  ,
                    'Artist'  :''  ,
                    'Genre'   :''
                }

            sleep(0.2)

    def Start(self):
        self.ConnectMediaPlayer()

    def ConnectMediaPlayer(self):
        while self.player_connected is not True:
            for obj_path in self.obj_list.keys():
                if "player" in obj_path:
                    self.player_path = obj_path
                    self.device_path = self.obj_list[self.player_path]['org.bluez.MediaPlayer1']['Device']
                    self.device_name = self.obj_list[self.device_path]['org.bluez.Device1']['Alias']
                    self.player_connected = self.obj_list[self.device_path]['org.bluez.MediaControl1']['Connected']
                    break
            sleep(0.2)

        self.media_player = pydbus.SystemBus().get('org.bluez', self.player_path)
        self.CreateWindow()

    def CheckConnection(self):
        if self.player_path not in self.obj_list and \
        self.obj_list[self.device_path]['org.bluez.MediaControl1']['Connected'] is False:
            self.player_connected = False
            self.root.destroy()
            self.Start()

    def isPlayerConnected(self):
        return self.player_connected

    def Play(self,event):
        self.media_player.Play()

    def Pause(self,event):
        self.media_player.Pause()

    def Next(self,event):
        self.media_player.Next()

    def Previous(self,event):
        self.media_player.Previous()

    def Terminate(self):
        self.TerminateFlag = True

    def checkTerminate(self,loop):
        if self.TerminateFlag is True:
            loop.quit()
        else:
            timeout_add(100,self.checkTerminate,loop)

    def DefineFunctionArgList(self):
        self.func_list = {
            'Terminate':self.Terminate,
            'Play':self.Play,
            'Pause':self.Pause,
            'Next':self.Next,
            'Previous':self.Previous,
            'isPlayerConnected':self.isPlayerConnected,
            'CheckConnection':self.CheckConnection
        }

    def CreateWindow(self):
        self.root = Window(self.func_list)
        self.root.run()

if __name__ == '__main__':
    player = MediaPlayer()
