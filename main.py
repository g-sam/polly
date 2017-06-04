import sds011
import machine
import esp

if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    print('Woke from a deep sleep')

READ_SECONDS = 55
SLEEP_SECONDS = 5

sds011.set_dutycycle(1)
sds011.read();
# esp.deepsleep(SLEEP_SECONDS * 1000000)
