import machine
import esp
import utime as time

SDS011_INIT_SECONDS = 23
READ_SECONDS = 7
SLEEP_SECONDS = 60

rtc = machine.RTC()

print('woken with task', rtc.memory())

if rtc.memory() == b'init':
    sds011.wake()
    rtc.memory(b'read')
    print('going to sleep, will wake to ', rtc.memory())
    esp.deepsleep(SDS011_INIT_SECONDS * 1000000)
    time.sleep(1)

rtc.memory(b'init')
import sds011
sds011.read(READ_SECONDS)
sds011.sleep()
print('going to sleep, will wake to ', rtc.memory())
esp.deepsleep(SLEEP_SECONDS * 1000000)

