pi-server-closet
================

Using Raspberry Pi to control a fan to move hot air out of the server closet.

## Requirements

You need to download and install the Nest Python Module. This is found at https://github.com/smbaker/pynest

# Settings

* nest_username: Username to login to your Nest thermostat. Default "me@example.com"
* nest_password: Password used to login to your Nest thermostat. Default "SuperSecretPassword"
* timeout: Time in seconds to sleep between sensor checks. Default 5 
* gpio_pin: GPIO pin that will turn on and off the fan. Generally a PowerTail is connected to this pin. This is the physical pin number and not the pin label. Default 12
* log_level: Lets the log level. Possible values are "debug", "info", "warning", "error", "critical". Default "debug"
* max_temperature: Temperature in fahrenheit when the fan should be on no matter what else is going on: Default 100
* i2c_address: Hexidecimal address of the i2c thermometer. Default 0x48
* smbus: GPIO bus. Should be 0 if you are using version 1 of the Raspberry Pi. 1 if you are using version . Default 1

## Install

1. Download pynest from https://github.com/smbaker/pynest and install. 
2. Download pi-server-closet to a local directory
3. Copy local_settings.cfg.dist to local_settings.cfg and change settings appropriately
4. You may choose to install fancontrol.py in your modules path but to get started quickly, run `sudo python ./fan.py`. Depending on your logging level, you will porobably see output from the script informing you of what is going on.
5. You may also want to create an init script so that this `fan.py` will run on system startup.

## TODO

* Create init script for RHEL and Debian
* Send logs to syslog
* Add setup.py