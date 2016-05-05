#!/usr/bin/python3
#this line makes the program runnable standalone i.e. can run the program by just typing:
#
# ./add_users file.txt student
#
#(rather than having to prepend the command with python3)

#Original author : Ian Johnson
#Written : April 2016

#to run command line programs
from os import system

#the name of the file to read in
userListFileName = "users.txt"

group = "student"

if group == "student":
	semester = "spring16"
else:
	semester = ""


#open up the file
userListFile = open(userListFileName,'r')

#put all the lines in as users
userNames = []
for line in userListFile:
	trimmedLine = line.strip()
	#ignore commented out lines
	if len(trimmedLine)!=0 and trimmedLine[0] != '#':
		#if we're adding student's we want to prepend s to the tech ID numbers
		if group == "student":
			userNames.append("s"+trimmedLine)
		else:
			userNames.append(trimmedLine)

#now that we have the list of users, make all their home directories
print("creating semester directory")
system("mkdir /export/home/"+group+"/"+semester)
system("chgrp student /export/home/"+group+"/"+semester)

#now create the user
print("creating users")
for user in userNames:
	system("sudo useradd -d /export/home/"+group+"/"+semester+"/"+user+" -m "+user)
	
#finally set their passwords
print("setting passwords")
for user in userNames:
	system("sudo passwd "+user)
