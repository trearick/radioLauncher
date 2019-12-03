from dronekit import connect, VehicleMode
import logging
import time
import mission_one


def run_once(vehicle):
	logging.debug("Called run_once")
	mission_one.mission_one(vehicle)


def run_loop():
	logging.debug("Called run_loop")


#connection_string = "/dev/serial0"
connection_string = None			# Note: this does not work on rPi without additional work

if not connection_string:
	import dronekit_sitl
	sitl = dronekit_sitl.start_default()
	connection_string = sitl.connection_string()

baud_rate = 921600
logging.basicConfig(filename="radioLaunch.log", level=logging.DEBUG)
logging.info("Connecting to hex on: %s" % (connection_string,))
vehicle = connect(connection_string, wait_ready=False, baud=baud_rate)
vehicle.wait_ready(True, timeout=300)
state = 0


while(True):
	t = time.clock()
	if vehicle.channels['6'] > 1500: # if true, run program
		if state == 0:
			run_once(vehicle)
		state = 1
		run_loop()
		break
	else:
		if state == 1:
			break

vehicle.close()
print("Program terminated")
