#!/usr/bin/python
''' Get processlist from mysql -  2014-01-29 - Cody '''
import sys, redis, time, logging, MySQLdb, MySQLdb.cursors, Queue, threading
from logstash_formatter import LogstashFormatterV1

class RedisHandler(logging.Handler):
  def __init__(self, host='localhost'):
    logging.Handler.__init__(self)
    
    self.r_server = redis.Redis(host)
    self.formatter = LogstashFormatterV1()
    
  def emit(self, record):
    self.r_server.rpush(record.name, self.format(record))

def check_mysql(cursor, hostname):
    try:
        cursor.execute("SHOW PROCESSLIST")
        plist = cursor.fetchall()
        for process in (process for process in plist if process['Info'] != 'SHOW PROCESSLIST'):
                process['Server'] = hostname
                #print process
                logger.info(process)
    except Exception as e:
        logger.info({'Error' : e})

def worker(host):
    try:
        db = MySQLdb.connect(host=host, user=db_user, passwd=db_pass, cursorclass=MySQLdb.cursors.DictCursor)
        with db:
            cursor = db.cursor()
            while True:
                check_mysql(cursor, host)
                time.sleep(5)
    except Exception as e:
        logger.info({'Error' : e})
        

db_hosts = ['host']
db_user = 'user'
db_pass ='pass'
redis_key = 'mysql'

logger = logging.getLogger(redis_key)
logger.setLevel(logging.DEBUG)
logger.addHandler(RedisHandler())


for host in db_hosts:
    t = threading.Thread(target=worker, args=(host, ))
    t.daemon = True
    t.start()

while True:
    pass

