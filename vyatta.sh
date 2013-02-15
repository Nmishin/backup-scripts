#!/bin/bash

#	vyatta.sh - Copyright (c) 2013 Will Smith

#	Backup Sonicwall Configs to an FTP Server. 

#	Licensing: MIT style -- Free, open source, and all that good stuff.

#	Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), 
#	to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, 
#	and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

#	The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

#	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
#	FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
#	LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER 
#	DEALINGS IN THE SOFTWARE.

#	*** Requirements ***

#	* SSH Keys setup on routers & routers in the trusted hosts.


echo It is the `eval date +%d/%m/%Y` @ `eval date +%H:%M:%S`

#Backup Core Routers
echo backing up Vyatta Routers...

#Vyatta Config Location
$CONFIG_DIR="/opt/vyatta/etc/config/config.boot"

vyattaRouters=("myrouter.mydomain.net" "myrouter2.mydomain.net")

for host in "${vyattaRouters[@]}"
	do
			echo backing up $host @ `eval date +%H:%M:%S`
			rsync -avz -e "ssh" vyatta@$host:$CONFIG_DIR /backups/vyatta/$host/
			echo finished backing up $host @ `eval date +%H:%M:%S`
	done
echo "done backing Up Vyatta Routers..."


echo finshed backing up at `eval date +%H:%M:%S`,...sending status email