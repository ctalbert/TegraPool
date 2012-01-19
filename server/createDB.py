import MySQLdb
import ConfigParser

config = ConfigParser.ConfigParser()
config.read("dbsettings.ini")
HOST = config.get("database", "MYSQL_SERVER")
USER = config.get("database", "MYSQL_USER")
PASSWD = config.get("database", "MYSQL_PASSWD")
DB = config.get("database", "MYSQL_DB")


devicesq = """CREATE TABLE dbname.`devices` (
  `deviceid` varchar(25) NOT NULL DEFAULT '',
  `deviceIP` varchar(25) NOT NULL,
  `deviceType` varchar(25) DEFAULT NULL,
  `state` varchar(25) DEFAULT NULL,
  `pid` int(11) DEFAULT NULL,
  `user` varchar(25) DEFAULT NULL,
  `email` varchar(45) DEFAULT NULL,
  `localuser` varchar(25) DEFAULT NULL,
  PRIMARY KEY (`deviceid`,`deviceIP`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;"""

usersq = """CREATE TABLE dbname.`users` (
  `userid` varchar(25) NOT NULL DEFAULT '',
  `directory` varchar(250) NOT NULL DEFAULT '',
  PRIMARY KEY (`userid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;"""

conn = MySQLdb.connect(host = HOST,
                       user = USER,
                       passwd = PASSWD,
                       db = DB)
c = conn.cursor()
devicesq = devicesq.replace('dbname', DB)
c.execute(devicesq)

usersq = usersq.replace('dbname', DB)
c.execute(usersq)
