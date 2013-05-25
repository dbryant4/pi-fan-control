import sys
try:
    from config import Config
except:
    print "Unable to load the \"config\" module\n    easy_install config"
    sys.exit(-1)

from nest import Nest

cfg = Config(file('local_settings.cfg'))

n = Nest(cfg.username, cfg.password)
n.login()
n.get_status()
#print n.status['device'][n.serial]
away = n.status['shared'][n.serial]['auto_away']

if away:
    print "Auto away engaged"
else:
    print "Auto away not engaged"
