import random

# Prompt user to either HIDE or REVEAL a message
# Returns: a string
def getMode():
	print("\nDo you want to HIDE a message or REVEAL a message? Or type \'quit\'\n")
	while(True):
		mode = raw_input().lower()
		if(mode == "hide") or (mode == "reveal") or (mode == "quit"):
			return mode
		else:
			print("ERROR: invalid input. Please type \'hide\', \'reveal\', or \'quit\'")


# For REVEAL mode only. 
# Prompt user to provide the key list as a string, then build it as a list
# Returns list of keys as ints
def getKeyList():
	print("\nPlease provide the key list that was used to generate this hidden message...")
	print("The key list must be given in the following form: [key1,key2,key3,...]")
	print("You can either type it into the command line OR specify a .txt file (e.g. \'my_list.txt\')\n")
	keyListStr = ""
	keyData = ""
	keyList = []
	while(True):
		keyListPath = raw_input()
		if (".txt" in keyListPath):
			keyFile = open(keyListPath, "r")
			keyData = keyFile.read()
			break
		elif (keyListPath[0] == "["):
			keyData = keyListPath
			break
		else:
			print("ERROR: invalid input. Please double check your input format for key list. If using a file, make sure to include the .txt extension in the path")

	keyListStr = keyData[1:len(keyData)-1].split(",")
	for key in keyListStr:
		keyList.append(int(key))
	return keyList

# For HIDE mode only.
# write keyList to a file or the console
def writeKeyList(keyList):
	print("\nKey list generated. You will need this to decrypt this message. If you want it printed to the console, type \'print\'. If you would like to save it to a .txt file, please enter one (e.g. \'my_list.txt\'').\n")
	while(True):
		response = raw_input().lower()
		if(".txt" in response):
			keyFile = open(response, "w+")
			keyFile.write("[")
			for i, key in enumerate(keyList):
				keyFile.write(str(key))
				if(i != len(keyList)-1):
					keyFile.write(",")

			keyFile.write("]")
			keyFile.close()
			print("\nThe key list has been written to " + response)
			print("MAKE SURE TO KEEP THIS KEY LIST FOR THIS PARTICULAR MESSAGE.\n")
			return 1
		elif(response == 'print'):
			print("\nKEY LIST: " + str(keyList) + "\n")
			return 1
		else:
			print("ERROR: invalid input. Please specify \'print\' or a .txt file")


# For HIDE mode only.
# Returns the message as given by the user
def getMessage():
	print("\nType out the message you would like to hide.\n")
	message = raw_input()
	return message


# For HIDE and REVEAL modes.
# Shifts char by key. Adjusts for out of bounds to keep captialization
# Returns the new char
def shiftChar(char, key):
	charNum = ord(char) + key

	if(char.isupper()):

		if(charNum > ord('Z')):
			charNum -= 26

		if(charNum < ord('A')):
			charNum += 26

	if(char.islower()):

		if(charNum > ord('z')):
			charNum -= 26

		if(charNum < ord('a')):
			charNum += 26

	return chr(charNum)

# For HIDE mode only.
# Take message and shift each alphabetical character by a random shift 0-26
# Returns a tuple containing the key list and encrypted message (keyList, encMessage)
def encryptMessage(message):
	encMessage = ""
	keyIndex = 0
	keyList = []

	for char in message:
		if(char.isalpha()):
			keyList.append(random.randint(0, 26))
			encMessage += shiftChar(char, keyList[keyIndex])
		else:
			keyList.append(0)
			encMessage += char
		keyIndex += 1

	return (keyList, encMessage)

# For REVEAL mode only.
# Takes the encrypted message and it's accompanying key list to decrypt the message
# Returns the decrypted message
def decryptMessage(message, keyList):
	decMessage = ""
	keyIndex = 0

	for char in message:
		decMessage += shiftChar(char, -keyList[keyIndex])
		keyIndex += 1

	return decMessage
