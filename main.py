import sds011
import machine
import esp
import utime as time
import logging

log = logging.getLogger('main')

SDS011_INIT_SECONDS = 23
READ_SECONDS = 7
SLEEP_SECONDS = 60

rtc = machine.RTC()

log.debug('woken with task %s', rtc.memory())

if rtc.memory() == b'init':
    sds011.wake()
    rtc.memory(b'read')
    log.debug('going to sleep, will wake to %s', rtc.memory())
    esp.deepsleep(SDS011_INIT_SECONDS * 1000000)
    time.sleep(1) # code continues to execute without this!

rtc.memory(b'init')
import sds011
sds011.read(READ_SECONDS)
sds011.sleep()
log.debug('going to sleep, will wake to %s', rtc.memory())
esp.deepsleep(SLEEP_SECONDS * 1000000)

