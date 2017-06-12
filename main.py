import sds011
import machine
import esp
import utime as time

if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    print('Woke from a deep sleep')

READ_SECONDS = 20
SLEEP_SECONDS = 60
DUTYCYCLE_REST_MINS = 0

# sds011.set_dutycycle(DUTYCYCLE_REST_MINS)
sds011.wake()
sds011.read(READ_SECONDS)
sds011.sleep()
esp.deepsleep(SLEEP_SECONDS * 1000000)
