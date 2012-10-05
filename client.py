import urllib, urllib2, time, os
from sys import exit

url = "http://127.0.0.1/server.php"

print "Welcome to PublicShell v0.01"
print "1)Accept incoming connections \n2)Connect to a Remote PC"
choice = input("Choice : ")

if( choice == 1 ):
	identifier = raw_input("Please enter an identifier for your PC : ")
	#Enter identifier into database
	requestType = 'insertReceiver'
	reply=""
	values = {"requestType": requestType, "id" : identifier}
	try:	
		data = urllib.urlencode(values)          
		req = urllib2.Request(url, data)
		response = urllib2.urlopen(req)
		reply = response.read();  	
	except Exception, detail:
		print "Error : ", detail
	
	if(reply == 'true'):	
		print 'Your PC is now waiting for incoming commands...'
		#Loop, executing and displaying all commands received
		while(1):
			requestType = 'getCmd'
			values = {"requestType": requestType, "id" : identifier}
			reply='false'
			while(reply == 'false'):
				try:	
					data = urllib.urlencode(values)          
					req = urllib2.Request(url, data)
					response = urllib2.urlopen(req)
					reply = response.read()
				except Exception, detail:
					print "Error : ", detail
					
			command = reply
			if(command == '@exit'):
				#cleanup - delete user from id
				requestType = 'delUser'
				values = {"requestType": requestType, "id" : identifier}
				try:	
					data = urllib.urlencode(values)          
					req = urllib2.Request(url, data)
					response = urllib2.urlopen(req)
					reply = response.read()  	
					print reply
				except Exception, detail:
					print "Error : ", detail
				print 'Connection terminated by host'
				exit()
			command += ' > .__PublicShell__output.log 2> .__PublicShell__error.log'
			os.system (command) #This actually executes the command on the client PC
			print "Command Executed : ", reply; #To notify client
			
			#The output is saved in output.log
			output = ""
			for line in file(".__PublicShell__output.log"):
				output += line
			for line in file(".__PublicShell__error.log"):
				output += line	
			os.system ('rm .__PublicShell__output.log .__PublicShell__error.log')
			#Output is now in variable output
			#End of execution
			
			#Now, we need to send back the output to the server
			requestType = 'output'
			values = {"requestType": requestType, "id" : identifier, "output" : output}
			try:	
				data = urllib.urlencode(values)          
				req = urllib2.Request(url, data)
				response = urllib2.urlopen(req)
				reply = response.read()  	
			except Exception, detail:
				print "Error : ", detail
			#Output sent.
			
	else:
		print 'Sorry, unsuccessful'
			
	
elif( choice == 2 ):
	identifier = raw_input("Please enter the identifier of the  PC you are trying to connect to : ")
	requestType = 'connect'
	values = {"requestType" : requestType, "id" : identifier}
	try:
		data = urllib.urlencode(values)          
		req = urllib2.Request(url, data)
		response = urllib2.urlopen(req)
		reply = response.read()  	
	except Exception, detail: 
		print "Error : ", detail 
	
	#If identifier found in database
	if(reply == "true"):
		print "Connected. \nYou may now execute commands on the remote PC.\n"
		print "Use '@exit' to quit."
		command = ""
		while(command != "@exit"):
			command = raw_input("$ : ")
			requestType='pushCmd'
			values = {"requestType": requestType, "id" : identifier, "cmd" : command}
			try:
				data = urllib.urlencode(values)          
				req = urllib2.Request(url, data)
				response = urllib2.urlopen(req)
				reply = response.read()
			except Exception, detail: 
				print "Error : ", detail
			
			if(command != '@exit'):
				#command now in db. Get output.
				requestType='getOutput'
				values = {"requestType" : requestType, "id" : identifier}				
				reply2='false'; 
				while(reply2 == 'false'):
					try:	
						data = urllib.urlencode(values)          
						req = urllib2.Request(url, data)
						response = urllib2.urlopen(req)
						reply2 = response.read()
					except Exception, detail:
						print "Error : ", detail
				print reply2	
				
	else:
		print "Sorry, Invalid Identifier"
