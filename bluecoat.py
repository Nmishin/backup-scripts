#!/usr/bin/python
""""
bluecoat.py - Copyright (c) 2013 Will Smith

	Backup Bluecoat Packetshaper Configs. 

Licensing: MIT style -- Free, open source, and all that good stuff.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER 
DEALINGS IN THE SOFTWARE.

*** Requirements ***

	* pexcept by Noah (http://www.noah.org/wiki/pexpect)

"""

import os, pexpect, time
from datetime import datetime

BACKUP_PATH = '/path/to/backup/to/'					#Path to backup the config files to
CONFIG_NAME = 'config.cmd'							#Name of the dumped config file
CONNECT_PORT = 22									#Port that SSH on the Packetteer is running on.


#Packteers to Backup
PACKETEERS = (
	('10.xxx.xxx.xxx', 'mystrongpassword', 'touch'),
	('10.xxx.xxx.xxx', 'mystrongpassword', 'touch'),

# Connect to the packeteer and dump, backup and the clear the dumped config from
# the packteer, then rename the file so we know which Packeteer it is from.
def connection(host, port, username, password):

	#Initialise a new SSH Session, and
	 sshc = pexpect.spawn('ssh ' + username + '@' + host)
	 sshc.expect('Password:')
	 sshc.sendline(password)
	 print 'connected to packetshaper...'
	 sshc.expect('PacketShaper#')
	 sshc.sendline('setup capture complete')	#Dump the config
	 sshc.sendline('yes')						#incase we dont delete the old dump
	 sshc.expect('PacketShaper#')
	 print 'config dumped...'
	 sshc.close()
	 print 'connection closed...'

	 print 'ftp connection starting...'
	 ftpc = pexpect.spawn('ftp ' + username + '@' + host)
	 ftpc.expect('Password:')
	 ftpc.sendline(password)
	 ftpc.expect('ftp>')
	 print 'ftp connected...'
	 ftpc.sendline('cd cmd')					#Change to the directory where the dumped config is
	 ftpc.expect('ftp>')		
	 ftpc.sendline('lcd ' + BACKUP_PATH)		#Local change directory to where the backups will be stored
	 ftpc.expect('ftp>')
	 ftpc.sendline('binary')					#Set Binary mode
	 ftpc.expect('ftp>')				
	 ftpc.sendline('get config.cmd')			#Get the config file
	 print 'file fetched...'

	 ftpc.expect('ftp>')
	 ftpc.sendline('rm config.cmd')				#Delete the dump from the PS, ready for it to run the next time
	 ftpc.expect('ftp>')
	 print 'dumped config deleted from packetshaper...'
	 ftpc.close()		
	 print 'ftp connection closed...'
	 dts = time.strftime('%Y%m%d%H%M%S')		#Prepare the datetime stamp	 
	 os.rename(BACKUP_PATH + CONFIG_NAME,BACKUP_PATH + host +'-' + dts +'.cmd')	#Rename the file so we know which PS it is from


#For every Packetteer in the tuple at the top of the script, run the backup method.
for i in range(0,len(PACKETEERS)):
	print 'backing up ' + PACKETEERS[i][0]
	connection(PACKETEERS[i][0], CONNECT_PORT, PACKETEERS[i][2],PACKETEERS[i][1])
	print 'done backing up ' + PACKETEERS[i][0]
