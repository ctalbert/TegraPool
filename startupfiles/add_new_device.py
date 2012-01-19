from devicemanagerSUT import DeviceManagerSUT
from optparse import OptionParser
import MySQLdb
import ConfigParser
import sys
import os
import subprocess

c = ConfigParser.ConfigParser()
c.read("TegraPool/server/dbsettings.ini")
HOST = c.get("database", "MYSQL_SERVER")
USER = c.get("database", "MYSQL_USER")
PASSWD = c.get("database", "MYSQL_PASSWD")
DB = c.get("database", "MYSQL_DB")

def push(ip, port, filename):
    dm = DeviceManagerSUT(ip, port)
    dm.pushFile(filename, '/data/data/com.mozilla.SUTAgentAndroid/files/SUTAgent.ini')

def makeFile(regsvrIP, regsvrPort, hardware, user):
    sutagent = os.path.join(os.getcwd(), "SUTAgent.ini")
    if os.path.exists(sutagent):
        os.remove(sutagent)

    cfg = ConfigParser.RawConfigParser()
    cfg.read("SUTAgent_base.ini")
    if not cfg.has_section("Registration Server"):
        cfg.add_section("Registration Server")

    cfg.set("Registration Server", "IPAddr", regsvrIP)
    cfg.set("Registration Server", "PORT", regsvrPort)
    cfg.set("Registration Server", "HARDWARE", hardware)
    cfg.set("Registration Server", "POOL", user)

    cfg.write(open(sutagent, 'w'))
    return sutagent
    

def addToDb(user):
    add_userq = """INSERT INTO dbname.users VALUES(%s, %s)"""
    conn = MySQLdb.connect(host=HOST, user=USER, passwd=PASSWD, db=DB)
    cursr = conn.cursor()
    add_userq = add_userq.replace("dbname", DB)
    cursr.execute(add_userq, (user, '/home/'+user))
    if not cursr.rowcount:
        print "Error creating new user for tegra, are you sure the new user %s is unique" % user
        sys.exit(1)
    conn.commit()
    cursr.close()
    conn.close()

def main(options):
    print "Adding user %s to database" % options.user
    addToDb(options.user)
    
    print "Making sutagent.ini file"
    sutagent = makeFile(options.regsvrIP, options.regsvrPort, options.hardware, options.user)
 
    print "Pushing sutagent.ini file to device"
    push(options.ip, options.port, sutagent)

    print "Setting full permissions on user's directory: home/" + options.user
    subprocess.call(["sudo", "chmod", "-R", "777", "/home/" + options.user])

    print "Done! When the device reboots next, it will register with the tegra pool."


parser = OptionParser()
defaults = {}
parser.add_option("-i", "--ip", dest="ip", help="IP address of device")
defaults["ip"] = None
parser.add_option("-p", "--port", dest="port", help="CmdPort of Agent on device, defaults to 20701")
defaults["port"] = "20701"
parser.add_option("--regIP", dest="regsvrIP", help="Registration server IP, defaults to 10.250.7.80 (this machine)")
defaults["regsvrIP"] = "10.250.7.80"
parser.add_option("--regPort", dest="regsvrPort", help="Registration server Port, defaults to 28001")
defaults["regsvrPort"] = 28001
parser.add_option("--hardware", dest="hardware", help="Type of device you are adding to system, defaults to Tegra")
defaults["hardware"] = "Tegra"
parser.add_option("--user", dest="user", help="Username for device's user.  MUST ALREADY BE CONFIGURED ON SYSTEM, see README")
defaults["user"] = None

parser.set_defaults(**defaults)

(options, args) = parser.parse_args()

# Verify options
if not options.ip:
    print "You must specify an IP address of the device you are adding.  It must also ALREADY be running the SUTAgent.  See README"
    sys.exit(1)

if not options.user:
    print "You must specify the device's user and the account must already be created, see README"
    sys.exit(1)

if __name__ == "__main__":
    main(options)

