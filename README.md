# Pollution monitor

Components:

- SDS011 particulate sensor
- Wemos D1 mini pro (based on ESP8266)
- Some wires

Ultra simple wiring and ultra simple programming with Micropython! The SDS011 communicates over serial with a protocol detailed here http://cl.ly/ekot: 

SDS011 -- Wemos 

  TX   --   RX    
  RX   --   TX  
  5v   --   5v  
  GND  --   GND   

Wemos has only one serial-in and Micropython has no software serial library, so the device cannot be accessed when it is connected to the sensor. Luckily, the webrepl can be used to interact with the device instead.

Ideally, the sensor would be put to sleep and woken periodically. There are some issues with this:
 - Printing anything to webrepl wakes the sensor up and it ceases to interpret sleep and wake signals properly
 - Sending the Wemos into deep sleep also wakes up the sensor! 

As a temporary workaround, I am using the dutycycle mode on the SDS011. This helps to preserve the life of the sensor and is fine for indoor use, but is not a good solution for battery operation because:
 - The sensor periodically wakes up, waits 60 secs, then issues a single reading before sleeping again. Since the documented initialization time of the sensor is 30 secs (and in my experience more like 10), that's a lot of wasted fan-time. 
 - The Wemos remains fully powered, drawing 50-200mA (although light sleep might be possible for around 1mA)

## Going outdoors

Some possible solutions for an immobile battery-operated version:
1) Use the dutycycle mode with a sleeping Wemos, but have the sensor initialization wake up the Wemos with a low pulse to RST (may not work if deep sleep interferes with the dutycycle). Requires a flip-flop circuit (https://github.com/esp8266/Arduino/issues/1488)? 
2) Use something (relay? MOSFET?) between the Wemos and the SDS011 to cut the connection before entering deep sleep. 
3) Hook the whole circuit to a MOSFET controlled by an ATiny85 or similar. This would provide better efficiency (because we would be sleeping the ATiny85 instead of the Wemos, which would be completely powered down), but is more complicated. 

Let's evaluate some options assuming a 10 minute wake interval, 30 sec working period (so 3 minutes / hour awake), and the following power factors:
 - SDS011 consumes 70mA (awake) or <4mA (asleep)
 - Wemos consumes 150mA on average when awake or 5mA in light sleep
 - Deepsleep on Wemos consumes 2/3 times more than on esp8266 because of the USB-TTL converter: probably equates to around 0.1mA in total 
 - At 1MHz the ATTiny85 consumes 2.5mA (awake) or 0.0005mA (asleep)
 - 3 AA batteries providing 7200mAh total
 - 70% efficiency 

As is: (7200 * 60 * 0.7) / (3 * (70 + 150) + 57 * (150 + 4) = 32 hours 

Without ATTiny but with relay: (7200 * 60 * 0.7) / (3 * (70 + 150) + 57 * 0.1) = 454 hours or 19 days 

With ATTiny: (7200 * 60 * 0.7) / (3 * (70 + 150 + 2.5) + 57 * 0.0005) = 453 hours 

What about using the ATTiny and turning on the Wemos only for last 7 secs of 30sec working period (say, 0.7 mins / hour @ 200mA)? (7200 * 60 * 0.7) / (3 * (70 + 2.5) + 0.7 * 200 + 57 * 0.0005) = 845 hours or 35 days.

If the Wemos can request time and pass it to ATTiny85, we can sleep 6 hours at night as well, bringing us up to around 1120 hours. 

## Portability

Another desideratum is the ability pair with a phone and transmit on the fly, or store measurements for transmission later.

Storing: by default we get 6 bytes of data every second. After 30 mins that's 11kb. The Wemos has 96 kb of data RAM so we should be fine... We could also move into the 4 mb of flash, but must be careful as it is limited to 100,000 write/erase cycles.

For gps data we need the phone. It should be possible for the phone to connect to the Wemos set up as an access point. Battery life on wifi might be expected to be 7200 * 0.7 / 200 = 25 hours. But it might make more sense to move to the ESP32 (which also has bluetooth) for this. 
