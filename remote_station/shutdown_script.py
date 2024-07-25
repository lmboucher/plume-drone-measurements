from gpiozero import Button
from subprocess import check_call
from signal import pause

def shutdown() :
	check_call(['sudo', 'poweroff'])

btn = Button(26, hold_time=2)
btn.when_held = shutdown

pause()
