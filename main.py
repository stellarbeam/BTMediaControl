import pydbus
from pprint import pprint

service = pydbus.SystemBus().get('org.bluez', '/')
obj_list = service.GetManagedObjects()
for key in obj_list.keys():
	if "player" in key:
		print(" Device Address: " + obj_list[key]['org.bluez.MediaPlayer1']['Device'])
		print(" Player:         " + key)

media_player = pydbus.SystemBus().get('org.bluez', '/org/bluez/hci0/dev_44_C3_46_7B_2D_C7/player0')


while True:
	print("1.Play 2.Pause 3.Next 4.Previous")
	choice = int(input("Enter choice:"))

	if choice == 1:
		media_player.Play()
	elif choice == 2:
		media_player.Pause()
	elif choice == 3:
		media_player.Next()
	elif choice == 4:
		media_player.Previous()