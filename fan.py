import sys
import time
import logging
import smbus
import urllib2

from fancontrol import fan_control

try:
    from config import Config
except:
    print "Unable to load the \"config\" module\n    easy_install config"
    sys.exit(-1)

try:
    from nest import Nest
except:
    print "Unable to load \"nest\" module. See README.md for URL"

# Read configuration file
cfg = Config(file('local_settings.cfg'))

# Setup logging module
numeric_level = getattr(logging, cfg.log_level.upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError('Invalid log level: %s' % loglevel)
#logging.basicConfig(level=numeric_level, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filename='/dev/shm/fan-control.log')
logging.basicConfig(level=numeric_level, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

logging.debug("Initializing fan control")
fan = fan_control(cfg.gpio_pin)


logging.debug("Logging in to Nest thermostat")
n = Nest(cfg.nest_username, cfg.nest_password)
try:
    n.login()
except urllib2.URLError:
    logging.error("Unable to login to Nest")
    sys.exit(1)
    
#print n.status['device'][n.serial]
#print n.status['shared'][n.serial]

bus = smbus.SMBus(cfg.smbus)

while True:
    try:
        n.get_status()
    except urllib2.URLError:
        pass

    away = n.status['shared'][n.serial]['auto_away']
    hvac_fan_on = n.status['shared'][n.serial]['hvac_fan_state']
    while True:
        try:
            current_temperature = bus.read_byte(0x48) * 1.8 + 32
        except IOError:
            logging.debug("Error getting temperature. Retrying...")
        else:
            break

    logging.debug("Temperature: %s", current_temperature)
    
    if away:
        logging.debug("Auto away enabled. Turning on fan.")
        fan.turn_on()
    elif hvac_fan_on:
        logging.debug("HVAC system running. Turning on fan.")
        fan.turn_on()
    elif current_temperature > cfg.max_temperature:
        logging.debug("Current Temperature is over max threshold. Turning on fan.")
        fan.turn_on()
    else:
        logging.debug("Nothing going on. Turning off fan.")
        fan.turn_off()
    logging.debug("Sleeping for %s seconds.",cfg.timeout)

    # Capture ctrl+c and turn fan on 
    try:
        time.sleep(cfg.timeout)
    except KeyboardInterrupt:
        logging.debug("Caught ctrl+c. Turning fan on.")
        fan.turn_on()
        sys.exit(0)
