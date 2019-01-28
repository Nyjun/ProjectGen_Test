
import os

# Defining Defaults
clientNames = []
targetFolders = []
rtti = False
noExc = False
vectExt = ""

# Parsing Config File





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


