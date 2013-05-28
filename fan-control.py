import sys
import time
import logging
import smbus
import RPi.GPIO as GPIO
try:
    from config import Config
except:
    print "Unable to load the \"config\" module\n    easy_install config"
    sys.exit(-1)

try:
    from nest import Nest
except:
    print "Unable to load \"nest\" module. See README.md for URL"

cfg = Config(file('local_settings.cfg'))

numeric_level = getattr(logging, cfg.log_level.upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError('Invalid log level: %s' % loglevel)
logging.basicConfig(level=numeric_level)

logging.debug("Initializing GPIO settings.")
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(cfg.gpio_pin, GPIO.OUT)

logging.debug("Logging in to Nest thermostat")
n = Nest(cfg.username, cfg.password)
n.login()
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
        GPIO.output(cfg.gpio_pin, True)
    elif hvac_fan_on:
        logging.debug("HVAC system running. Turning on fan.")
        GPIO.output(cfg.gpio_pin, True)
    elif current_temperature > cfg.max_temperature:
        logging.debug("Current Temperature is over max threshold. Turning on fan.")
        GPIO.output(cfg.gpio_pin, True)
    else:
        logging.debug("Nothing going on. Turning off fan.")
        GPIO.output(cfg.gpio_pin, False)
    logging.debug("Sleeping for %s seconds.",cfg.timeout)

    try:
        time.sleep(cfg.timeout)
    except KeyboardInterrupt:
        logging.debug("Caught ctrl+c. Turning fan on.")
        GPIO.output(cfg.gpio_pin, True)
        sys.exit(0)
