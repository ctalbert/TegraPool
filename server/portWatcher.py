import socket
import urlparse
import MySQLdb

import ConfigParser

config = ConfigParser.ConfigParser()
config.read("dbsettings.ini")
SQL_HOST = config.get("database", "MYSQL_SERVER")
SQL_USER = config.get("database", "MYSQL_USER")
SQL_PASSWD = config.get("database", "MYSQL_PASSWD")
SQL_DB = config.get("database", "MYSQL_DB")

#Set up the port to be listened on. 
HOST = ''
PORT = 28001
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST,PORT))

#Set up db for database connection


#Permanent loop listening to the port waiting for a ping. 
while 1:
  s.listen(1)
  conn, addr = s.accept()
  print 'Connected by', addr
  data = conn.recv(1024)
  #print("Data= " +data)
  data = data.lstrip("register ")
  info = urlparse.parse_qs(data)
  #print info
  devicename = info['NAME'][0].strip()
  deviceip = info['IPADDR'][0].strip()
  devicehw = info['HARDWARE'][0].strip()
  deviceusr = info['POOL'][0].strip()

  print "NAME = " + devicename
  print "IP = " + deviceip
  print "TYPE = " + devicehw
  print "USER = " + deviceusr
  #When a ping arrives, store the information in the devices table.
  #NOTE: Issue occurs if the PINGs arrive faster than
  #data can be written to the database.
  inputted = False
  db = False
  while not inputted:
    try:
      db = MySQLdb.connect(user=SQL_USER, passwd=SQL_PASSWD, db=SQL_DB)
      c=db.cursor();
      c.execute("LOCK TABLE devices WRITE");
      c.execute("INSERT INTO devices (deviceid,deviceIP,deviceType,state, localuser) VALUES ('"+
                 devicename +"','" + deviceip +"','"+ devicehw +
                 "','AVAILABLE','" + deviceusr + "') ON DUPLICATE KEY UPDATE state='AVAILABLE';")
      c.execute("UPDATE devices SET state='CHECKED_OUT' WHERE deviceIP ='" +
                deviceip + "' AND user IS NOT NULL;")
      c.execute("UNLOCK TABLES;")
      db.commit()
      c.close()
      db.close()
      conn.close()
      inputted = True
    except:
      if db: 
        if c:
          c.close()
        db.close()
      

