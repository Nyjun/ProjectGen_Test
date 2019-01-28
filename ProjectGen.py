
import os

# Defining Defaults
clientNames = []
targetFolders = []
rtti = False
noExc = False
vectExt = ""
AllowedVectorExtensions = ["AVX", "AVX2", "IA32", "SSE", "SSE2", "SSE3",\
 "SSSE3", "SSE4.1", "NEON", "MXU"]

# Parsing Config File
tmp = ""
state = 0
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
				noExc = tmp == "on"
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

# Generate folder(s)
for folder in targetFolders:
	if not os.path.exists(folder):
		os.makedirs(folder)

# Call Premake5
for client in clientNames:
	if os.name == 'nt':
		pass
	else:
		pass


