""""
sonicwall.py - Copyright (c) 2013 Will Smith

	Backup Sonicwall Configs to an FTP Server. 

Licensing: MIT style -- Free, open source, and all that good stuff.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER 
DEALINGS IN THE SOFTWARE.

*** Requirements ***

	* An accessible FTP Server
	* pexcept by Noah (http://www.noah.org/wiki/pexpect)
		
""""

#!/usr/bin/python
import pexpect, time

FTP_SERVER = '10.xxx.xxx.xxx'							#FTP Server Address
FTP_USERNAME = 'myftpusername'							#FTP Username
FTP_PASSWORD = 'mystrongpassword'						#FTP Password


#('192.168.168.168','username', 'password', 'host-description', 'System Name')

#Sonicwalls to Backup
SONICWALLS = (
	('192.168.168.168','admin', 'password', 'TEST-FW', 'NSA 2400'),
	('192.168.168.168','admin', 'password', 'TEST-FW-2', 'NSA 2400'),
)

def connection(host, username, password, desc, sysname):

	 sshc = pexpect.spawn('ssh ' + host)
	 sshc.expect('User:')
	 sshc.sendline(username)
	 sshc.expect('Password:')
	 sshc.sendline(password)
	 sshc.expect(sysname + '>')
	 print 'Logged in...'
	 dts = time.strftime('%Y%m%d%H%M%S')	
	 sshc.sendline('export preferences ftp ' + FTP_SERVER + ' ' + FTP_USERNAME + ' ' + FTP_PASSWORD + ' prefs_'+ desc +'_'+ dts +'.exp')
	 print 'config dumped & copied...'
	 sshc.expect(sysname + '>')
	 sshc.sendline('exit')
	 print 'Exiting...'
	 sshc.close()
	 print 'Connection closed...'
	 time.sleep(2)

#For every Sonicwall in the tuple at the top of the script, run the backup method.
for i in range(0,len(SONICWALLS)):
	print 'backing up ' + SONICWALLS[i][3]
	connection(SONICWALLS[i][0], SONICWALLS[i][1],SONICWALLS[i][2],SONICWALLS[i][3],SONICWALLS[i][4])
	print 'done backing up ' + SONICWALLS[i][3]