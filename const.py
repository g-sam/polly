WAKE_RF_DEFAULT = 0 # RF_CAL or not after deep-sleep wake up, depends on init data byte 108.
WAKE_RF_CAL = 1     #// RF_CAL after deep-sleep wake up, there will be large current.
WAKE_RF_NO_CAL = 2  #// no RF_CAL after deep-sleep wake up, there will only be small current.
WAKE_RF_DISABLED = 4 #// disable RF after deep-sleep wake up, just like modem sleep, there will be the smallest current.
