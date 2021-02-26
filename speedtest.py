import os
import re
import subprocess
import time
import mysql.connector

db = mysql.connector.connect(user='scripts', password='scriptpass', host='localhost', db='speed')

response = subprocess.Popen('/usr/bin/speedtest', shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')

ping = re.search('Latency:\s+(.*?)\s', response, re.MULTILINE)
download = re.search('Download:\s+(.*?)\s', response, re.MULTILINE)
upload =  re.search('Upload:\s+(.*?)\s', response, re.MULTILINE)

ping = ping.group(1)
download = download.group(1)
upload = upload.group(1)
datetime = time.strftime('20%y-%m-%d %H:%M:%S')

try:
    f = open('/home/pi/speedtest/speedtest.csv', 'a+')
    if os.stat('/home/pi/speedtest/speedtest.csv').st_size == 0:
            f.write('DateTime,Ping (ms),Download (Mbps),Upload (Mbps)\r\n')
except:
    pass

f.write('{},{},{},{}\r\n'.format(time.strftime('20%y-%m-%d %H:%M:%S'), ping, download, upload))

cur = db.cursor()

sql = ("INSERT INTO speedlog (date, ping, download, upload) VALUES(%s, %s, %s, %s)", (datetime, ping, download, upload))

cur.execute(*sql)
db.commit()
db.close()
print(datetime, ping, download, upload)
