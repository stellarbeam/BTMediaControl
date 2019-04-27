#!/usr/bin/python

try:
    from tkinter import Tk, Frame, Button
    from tkinter import TOP, BOTH, LEFT, RIGHT
except ImportError: #python2
    from Tkinter import Tk, Frame, Button
    from tkinter import TOP, BOTH, LEFT, RIGHT

class Window(Tk):
    def __init__(self,arg_list):
        super().__init__()
        self.arg_list = arg_list

    def run(self):
        self.protocol("WM_DELETE_WINDOW", self.on_delete)
        self.title('BTMediaControl')

        self.top_frame = Frame(self,width=350,height=100)
        self.top_frame.pack_propagate(0)

        self.left_frame = Frame(self.top_frame,width=175,height=50)
        self.left_frame.pack_propagate(0)

        self.right_frame = Frame(self.top_frame,width=175,height=50)
        self.right_frame.pack_propagate(0)

        #Buttons
        self.PlayButton = Button( self.left_frame, text="Play")
        self.PlayButton.pack( side=TOP, fill=BOTH, expand=True)

        self.PauseButton = Button( self.right_frame, text="Pause")
        self.PauseButton.pack( side=TOP, fill=BOTH, expand=True)

        self.NextButton = Button( self.right_frame, text="Next")
        self.NextButton.pack( side=TOP, fill=BOTH, expand=True)

        self.PreviousButton = Button( self.left_frame, text="Previous")
        self.PreviousButton.pack( side=TOP, fill=BOTH, expand=True)

        self.PlayButton.bind('<Button-1>',self.arg_list['Play'])
        self.PauseButton.bind('<Button-1>',self.arg_list['Pause'])
        self.NextButton.bind('<Button-1>',self.arg_list['Next'])
        self.PreviousButton.bind('<Button-1>',self.arg_list['Previous'])

        self.left_frame.pack( fill=BOTH, side=LEFT)
        self.right_frame.pack( fill=BOTH, side=RIGHT)
        self.top_frame.pack( fill=BOTH, side=TOP)

        self.resizable(0,0)

        self.after(200,self.scheduled_caller)

        self.mainloop()

    def on_delete(self):
        self.arg_list['Terminate']()
        self.destroy()

    def scheduled_caller(self):
        self.arg_list['CheckConnection']()
        self.after(200,self.scheduled_caller)
