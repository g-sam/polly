# Pollution monitor

Components:

- SDS011 particulate sensor
- Wemos D1 mini pro (based on ESP8266)
- Some wires

Ultra simple wiring and ultra simple programming with Micropython! The SDS011 communicates over serial with a protocol detailed here http://cl.ly/ekot: 

SDS011 -- Wemos 

  TX   --   RX    
  RX   --   D4 (TX1)  
  5v   --   5v  
  GND  --   GND   

Also, connect Wemos RST -- Wemos D0 (used for interrupting deep sleep).

Wemos has only one serial-in and Micropython has no software serial library, so the device cannot be accessed when it is connected to the sensor. Luckily, the webrepl can be used to interact with the device instead.

The sensor RX is connected to D4 because of a problem when connected to TX on the Wemos:
 - Printing anything to webrepl wakes the sensor up and it ceases to interpret sleep and wake signals properly
 - Sending the Wemos into deep sleep also wakes up the sensor!

D4 is a separate serial-out pin which does not suffer from these problems, probably caused by interference with the webrepl.

As currently programmed, the sensor will loop between sleeping (with the Wemos in deep sleep) and reading. It is also possible to set the dutycycle mode on the SDS011 (where the sensor automatically sleeps for a specified interval), but there is not much benefit to this over sleeping (especially as in this mode it takes 60 secs to wake up before reading, whereas wake up from sleep takes 30 secs)

## Going outdoors

A downside of the current implementation is that the SDS011 draws a relatively hefty 4ma while asleep. Some possible solutions for increasing battery life:
1) Use something (relay? MOSFET?) between the Wemos and the SDS011 to cut the connection before entering deep sleep. 
2) Hook the whole circuit to a MOSFET controlled by an ATiny85 or similar. This would provide better efficiency (because we would be sleeping the ATiny85 instead of the Wemos, which would be completely powered down), but is more complicated. 

Let's evaluate these options assuming a 10 minute wake interval, 30 sec working period (so 3 minutes / hour awake), and the following power factors:
 - SDS011 consumes 70mA (awake) or <4mA (asleep)
 - Wemos consumes 150mA on average when awake or 5mA in light sleep
 - Deepsleep on Wemos consumes 2/3 times more than on esp8266 because of the USB-TTL converter: probably equates to around 0.1mA in total 
 - At 1MHz the ATTiny85 consumes 2.5mA (awake) or 0.0005mA (asleep)
 - 10000mAh usb battery pack (e.g. [this one](https://www.amazon.co.uk/Puridea-Portable-External-Blackberry-Valentines/dp/B0109PYRE0/ref=sr_1_4?s=electronics&ie=UTF8&qid=1499622375&sr=1-4&keywords=10000+mah+usb+power))
 - 70% efficiency 

As is: (10000 * 60 * 0.7) / (3 * (70 + 150) + 57 * (0.1 + 4) = 470 hours or 20 days 

Without ATTiny but with relay: (10000 * 60 * 0.7) / (3 * (70 + 150) + 57 * 0.1) = 631 hours or 26 days 

With ATTiny: (10000 * 60 * 0.7) / (3 * (70 + 150 + 2.5) + 57 * 0.0005) = 629 hours 

What about using the ATTiny and turning on the Wemos only for last 7 secs of 30sec working period (say, 0.7 mins / hour @ 200mA)? (10000 * 60 * 0.7) / (3 * (70 + 2.5) + 0.7 * 200 + 57 * 0.0005) = 1174 hours or 49 days.

If the Wemos can request time and pass it to ATTiny85, we can sleep 6 hours at night as well, bringing us up to around 60 days. 

## Portability

Another desideratum is the ability pair with a phone and transmit on the fly, or store measurements for transmission later.

Storing: by default we get 6 bytes of data every second. After 30 mins that's 11kb. The Wemos has 96 kb of data RAM so we should be fine... We could also move into the 4 mb of flash, but must be careful as it is limited to 100,000 write/erase cycles.

For gps data we need the phone. It should be possible for the phone to connect to the Wemos set up as an access point. Battery life on wifi might be expected to be 10000 * 0.7 / 200 = 35 hours. But it might make more sense to move to the ESP32 (which also has bluetooth) for this. 
