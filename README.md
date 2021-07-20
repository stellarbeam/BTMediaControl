# BTMediaControl
Control media player of smartphone connected via Bluetooth, for Ubuntu (not tested on other Linux distributions)
Also displays information like time elapsed, total time, title, artist, album of song etc.

## Requirements
1. `BlueZ` version >= 5.48 (usually pre-installed)
2. Python 2 or 3
3. `pydbus` and `tkinter` (or `Tkinter` if you are using Python 2) modules installed

## How to use?
1. Pair your smartphone to Ubuntu machine
2. Play music on phone(the a2dp source), and make sure your Ubuntu machine speakers(the a2dp sink) play the audio
3. Run the script main.py (the window will only appear when the system is receiving audio through Bluetooth).
4. Now you can do Play, Pause, Next track, Previous track from Ubuntu machine itself

## Having problems with bluetooth?
If Step 2 of '<b>How to use?</b>' is not working for you, the following might help. Check out this link
<a href=https://askubuntu.com/a/109533/849242> here. </a>
