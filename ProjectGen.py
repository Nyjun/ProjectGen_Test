
import os
import subprocess
from subprocess import Popen, PIPE

# Defining Defaults
clientNames = []
targetFolders = []
rtti = False
noExc = ""
vectExt = ""
AllowedExceptionHanfling = ["On", "Off", "seh"]
AllowedVectorExtensions = ["avx", "avx2", "ia32", "sse", "sse2", "sse3",\
 "ssse3", "sse4.1", "neon", "mxu"]

# Parsing Config File
tmp = ""
state = 0	# ClientName(1), rtti(2), no-exception(3), vector-extensions(4)
read = False
file = open("Config.txt", "r")
for line in file:
	for c in line:
		if c == '=':		# Start recording value
			state += 1
			read = True
		elif c == ';':		# End recording + store value
			read = False
			if state == 1 and tmp != "":
				clientNames.append(tmp)
				targetFolders.append(os.path.join(".",tmp))
			if state == 2:
				rtti = tmp == "On"
			if state == 3:
				if tmp in AllowedVectorExtensions:
					vectExt = tmp
			if state == 4:
				if tmp in AllowedVectorExtensions:
					vectExt = tmp
			tmp = ""
		elif c == ',':		# Store multiple values
			read = False
			if state == 1 and tmp != "":
				clientNames.append(tmp)
				targetFolders.append(os.path.join(".",tmp))
				tmp = ""
				read = True
		else:
			if read == True:
				tmp += c
				

# Completion with defaults when necessary
if len(clientNames) == 0:
	clientNames.append("NewProject")
	targetFolders.append(os.path.join(".","NewProject"))

# Generate folders
for folder in targetFolders:
	if not os.path.exists(folder):
		os.makedirs(folder)
	winfolder = os.path.join(folder, "windows")
	linfolder = os.path.join(folder, "linux")
	if not os.path.exists(winfolder):
		os.makedirs(winfolder)
	if not os.path.exists(linfolder):
		os.makedirs(linfolder)

# Generate Option/Arg list
callList = [os.path.join("bin" , "premake5")]
if rtti:
	callList.append("--rtti=\"On\"")
if noExc != "":
	callList.append("--no-exception=" + noExc)
if vectExt != "":
	callList.append("--vector-ext=" + vectExt)

# Call Premake5
for client in clientNames:
	if os.name == 'nt':
		callList.append("vs2015")
		callList.append("--to=" + os.path.join(client, "windows"))
		subprocess.run(callList)
		callList.remove("--to=" + os.path.join(client, "windows"))
		callList.remove("vs2015")
		
		callList.append("--os=linux")
		callList.append("gmake2")
		callList.append("--to=" + os.path.join(client, "linux"))
		subprocess.run(callList)
		callList.remove("--to=" + os.path.join(client, "linux"))
		callList.remove("gmake2")
		callList.remove("--os=linux")
	else:
		callList.append("--os=windows")
		callList.append("vs2015")
		callList.append("--to=" + os.path.join(client, "windows"))
		subprocess.run(callList)
		callList.remove("--to=" + os.path.join(client, "windows"))
		callList.remove("vs2015")
		callList.remove("--os=windows")
		
		callList.append("gmake2")
		callList.append("--to=" + os.path.join(client, "linux"))
		subprocess.run(callList)
		callList.remove("--to=" + os.path.join(client, "linux"))
		callList.remove("gmake2")


