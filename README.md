# Pollution monitor

Components:

- SDS011 particulate sensor
- Wemos D1 mini pro (ESP8266)
- Some wires

Ultra simple wiring and ultra simple programming with Micropython! The SDS011 communicates over serial with a protocol detailed here http://cl.ly/ekot: 

SDS011      Wemos 

  TX   -->   RX    
  RX   <--   TX  
  5v   <--   5v  
  GND  -->   GND   

Wemos has only one serial-in and Micropython has no software serial library, so the device cannot be accessed when it is connected to the sensor. Luckily, the webrepl can be used to interact with the device instead.

Ideally, the sensor would be put to sleep and woken periodically. While the sleep command works, I CANNOT GET THE SENSOR TO WAKE UP!

Entering deep sleep on the Wemos does not help as the SDS011 continues to draw power.

As a temporary workaround, I am using the dutycycle mode: the Wemos remains on and the sensor kicks in every minute or so.

TODO: investigate having the sensor wake up the Wemos from deep sleep when the dutycycle kicks in. 

