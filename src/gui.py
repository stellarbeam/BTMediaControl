#!/usr/bin/python3

try:
    import tkinter as tk
    from tkinter import ttk
except: # Python 2
    import Tkinter as tk
    import ttk

class Window(tk.Tk):
    def __init__(self,func_list):
        try:
            super().__init__()
        except TypeError: # Python 2
            tk.Tk.__init__(self)

        self.func_list = func_list

    def gui_update(self):
        self.track_info = self.func_list['GetTrackInfo']()
        try:
            position = self.track_info['Position']
            duration = self.track_info['Duration']
            status = self.track_info['Status']

            self.position_var.set(self.timify(position))
            self.duration_var.set(self.timify(duration))
            self.title_var.set(self.track_info['Title'])
            self.album_var.set(self.track_info['Album'])
            self.artist_var.set(self.track_info['Artist'])
            self.progressbar['value']= (position/duration)*100

            if 'playing' in status:
                self.play_button.configure(image=self.pause_button_image, command=self.func_list['Pause'])
            elif 'paused' in status:
                self.play_button.configure(image=self.play_button_image, command=self.func_list['Play'])

        except:
            pass

    def timify(self, time):
        time /= 1000
        mins, secs = divmod( int(time), 60)
        text = '{:02d}:{:02d}'.format(mins,secs)
        return text


    def run(self):
        self.protocol("WM_DELETE_WINDOW", self.on_delete)
        self.title('BTMediaControl')
        self.minsize(550,300)

        self.canvas = tk.Canvas(self, height=300, width=550)
        self.canvas.pack()

        self.frame = tk.Frame(self, bg='#80c1ff')
        self.frame.place(relx=0, rely=0, relheight=0.65, relwidth=1)

        self.title_var = tk.StringVar()
        self.album_var = tk.StringVar()
        self.artist_var = tk.StringVar()

        self.title_label = tk.Label(self.frame, textvariable=self.title_var, bg='#80c1ff', font=('Helvetica',16))
        self.title_label.place(relx=0.5, rely=0.25, anchor='n')

        self.album_label = tk.Label(self.frame, textvariable=self.album_var, bg='#80c1ff', font=20)
        self.album_label.place(relx=0.5, rely=0.45, anchor='n')

        self.artist_label = tk.Label(self.frame, textvariable=self.artist_var, bg='#80c1ff', font=20)
        self.artist_label.place(relx=0.5, rely=0.65, anchor='n')



        self.bottomframe = tk.Frame(self, bg='#4286f4')
        self.bottomframe.place(relx=0, rely=0.65, relheight=0.35, relwidth=1)


        # Progressbar region
        self.progressbar=ttk.Progressbar(self.bottomframe,orient="horizontal",mode="determinate")
        self.progressbar.place(relx=0.1, rely=0.15, relwidth=0.8) # rely 0.2

        self.position_var = tk.StringVar()
        self.duration_var = tk.StringVar()

        self.position_label = tk.Label(self.bottomframe, textvariable=self.position_var, bg='#4286f4')
        self.position_label.place(relx=0, rely=0.15, relwidth=0.1)

        self.duration_label = tk.Label(self.bottomframe, textvariable=self.duration_var, bg='#4286f4')
        self.duration_label.place(relx=0.9, rely=0.15, relwidth=0.1)


        # Buttons Region
        self.play_button_image = tk.PhotoImage(file='play_new.png')
        self.pause_button_image = tk.PhotoImage(file='pause_new.png')
        self.previous_button_image = tk.PhotoImage(file='previous_new.png')
        self.next_button_image = tk.PhotoImage(file='next_new.png')

        self.play_button = tk.Button(self.bottomframe, image=self.play_button_image, bg='#4286f4',\
                                                    relief='flat', bd=0,\
                                                    highlightthickness=0, activebackground='#4286f4',\
                                                    command=self.func_list['Play'])
        self.play_button.place(relx=0.5, rely=0.43, anchor='n')


        self.previous_button = tk.Button(self.bottomframe, image=self.previous_button_image, bg='#4286f4',\
                                                    relief='flat', bd=0,\
                                                    highlightthickness=0, activebackground='#4286f4',\
                                                    command=self.func_list['Previous'])
        self.previous_button.place(relx=0.3, rely=0.43, anchor='n')

        self.next_button = tk.Button(self.bottomframe, image=self.next_button_image, bg='#4286f4',\
                                                    relief='flat', bd=0,\
                                                    highlightthickness=0, activebackground='#4286f4',\
                                                    command=self.func_list['Next'])
        self.next_button.place(relx=0.7, rely=0.43, anchor='n')


        # Execution
        self.after(200,self.scheduled_caller)

        self.mainloop()

    def on_delete(self):
        self.func_list['Terminate']()
        self.destroy()

    def scheduled_caller(self):
        self.func_list['CheckConnection']()
        self.gui_update()
        self.after(100,self.scheduled_caller)
