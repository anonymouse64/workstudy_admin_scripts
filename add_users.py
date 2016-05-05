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
#to get the command line arguments
from sys import argv
#for exiting the program gracefully
from sys import exit
#for parsing out the command line arguments
from argparse import ArgumentParser

#main function that parses argv and attempts to add the users
#takes as input all the arguments passed in from the command line
def main(argumentVector):
	#first parse out all the options specified from argv using the argparse module
	parser = ArgumentParser(description='Add users to the system')
	parser.add_argument('user', help='user to add, or if -b is specified filename of batch users')
	parser.add_argument('group', help='group to add all users in')
	parser.add_argument('-f','--folder', help='folder to add all users into')
	parser.add_argument('-b','--batch', default=False, action='store_const', const=True, help='use the first argument as a file to read in for list of user names')
	parser.add_argument('-p','--prefix', help='prefix to add to all user names')

	#now try to parse the arguments - ignore the first one, that's just the name of the script
	args = parser.parse_args(argumentVector[1:])

	#if we get to this point, the parsing worked, and so we can access the various options here
	user = args.user
	folder = args.folder
	group = args.group
	prefix = args.prefix
	batchMode = args.batch

	#check if we're in batch mode
	if batchMode:
		#it is an input file, read all the users into a list
		#open up the file - TODO: handle I/O excpetion when file doesn't exist properly
		userListFile = open(user,'r')
		#put all the lines in as users
		userNames = []
		for line in userListFile:
			trimmedLine = line.strip()
			#ignore commented out and empty lines
			if len(trimmedLine)!=0 and trimmedLine[0] != '#':
				#if a prefix was specified, then prepend that to the line
				if prefix != None:
					userNames.append(prefix+trimmedLine)
				else:
					userNames.append(trimmedLine)
		#now call the main add user routine
		#check if folder is None
		if folder != None:
			add_user_list(userNames,group,folder)
		else:
			add_user_list(userNames,group)
	else:
		#check if the prefix option was specified
		if prefix != None:
			if folder != None:
				add_user_list([prefix+user],group,folder)
			else:
				add_user_list([prefix+user],group)
		else:
			if folder != None:
				add_user_list([user],group,folder)
			else:
				add_user_list([user],group)

def add_user_list(userNames, group, folder=""):
	print("users to add are:")
	print(userNames)

	#now that we have the list of users, make all their home directories
	print("creating semester directory")
	system("mkdir /export/home/"+group+"/"+folder)
	system("chgrp student /export/home/"+group+"/"+folder)

	#now create the user
	print("creating users")
	for user in userNames:
		system("sudo useradd -d /export/home/"+group+"/"+folder+"/"+user+" -m "+user)
		
	#finally set their passwords
	print("setting passwords")
	for user in userNames:
		system("sudo passwd "+user)


#if this file is being run as a script, then python will define __name__ to be __main__
#so run our main function here
#note that doing this is also faster to run when we are using CPython or PyPy, but of course that doesn't
#really matter much for this script, as the main points here that will be blocking are the 
#system(XXX) calls
if __name__ == '__main__':
	main(argv)