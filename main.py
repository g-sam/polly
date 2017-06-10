import sds011
import machine
import esp

if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    print('Woke from a deep sleep')

READ_SECONDS = 20
SLEEP_SECONDS = 600
DUTYCYCLE_REST_MINS = 2

# sds011.set_dutycycle(DUTYCYCLE_REST_MINS)
print('Reading from sds011 for', READ_SECONDS, 'secs')
sds011.read(READ_SECONDS);
# esp.deepsleep(SLEEP_SECONDS * 1000000)
