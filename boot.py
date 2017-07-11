# This file is executed on every boot (including wake-boot from deepsleep)

print('Will start in 3 secs...')
import utime as time
time.sleep(3)

import gc
import logging
import config

gc.collect()

if config.DEBUG:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)
    import esp
    esp.osdebug(None)

log = logging.getLogger('boot')
