import sds011
import machine
import time
import esp

if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    print('Woke from a deep sleep')

READ_SECONDS = 55
SLEEP_SECONDS = 5

sds011.wake()
sds011.read(READ_SECONDS * 1000);
sds011.sleep();
# esp.deepsleep(SLEEP_SECONDS * 1000000)
