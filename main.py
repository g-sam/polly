import sds011
import machine
import esp
import utime as time
import logging
import const
import config

log = logging.getLogger('main')

rtc = machine.RTC()

log.debug('woken with task %s', rtc.memory())

if rtc.memory() == b'init':
    sds011.wake()
    rtc.memory(b'read')
    log.debug('going to sleep, will wake to %s', rtc.memory())
    esp.deepsleep(config.SDS011_INIT_SECONDS * 1000000, const.WAKE_RF_DEFAULT)
    time.sleep(1) # code continues to execute without this!

rtc.memory(b'init')
import net
net.connect()
import sds011
sds011.read(config.READ_SECONDS)
sds011.sleep()
log.debug('going to sleep, will wake to %s', rtc.memory())
esp.deepsleep(config.SLEEP_SECONDS * 1000000, const.WAKE_RF_DISABLED)

