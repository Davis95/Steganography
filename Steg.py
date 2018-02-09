"""
NOTES:
The term "encrypted image" refers an image that has an encrypted message hidden inside of it.
The term "cover image" refers to an image without a message inside of it.
"""

from PIL import Image
import os

extractLSB = 3

# Prompt the user for the initial image path
# Returns: The path to the cover image (string)
def getCoverPath():
	print("Please provide a path to your cover image. This image MUST be a PNG image and have the .png extension.\n")
	coverPath = raw_input()
	return coverPath

# Prompt the user for a path to save the encrypted image
# Returns: The save path provided by the user (string)
def getSavePath():
	print("\nPlease provide a path to save the encrypted image. Make sure to include the .png extension (e.g. \'new_image.png\')\n")
	savePath = raw_input()
	return savePath

# Prompt the user for a path to an encrypted image
# Returns: The path to the ecnrypted image (string)
def getEncImagePath():
	print("\nPlease provide a path to an encrypted image. Make sure to inlude the .png extention (e.g. \'hidden_image.png\')\n")
	imagePath = raw_input()
	return imagePath

# Takes message and hides it within an image
# @message The message to be hidden (string)
# @coverPath The path to the cover image (string)
# @savePath The path to save the encrypted image (string)
# Returns: nothing
def hideMessage(message, coverPath, savePath):
	im = Image.open(coverPath)
	messageBits = prepMessage(message)
	imData = list(im.getdata())

	if(len(imData) < len(message)):
		print("\nThe message is too long to fit inside the given cover image. Please try again.\n")
		return -1
	
	for i, char in enumerate(messageBits):
		imData[i] = encodePixel(char, imData[i])
	
	im.putdata(imData)
	im.save(savePath)
	print("\nThe encrypted image has been saved to " + savePath)

# Takes the given image and reveals the message hidden within (if there is one)
# @imagePath The path to an encrypted image (string)
# @messageLen The length of the encrypted message (int)
# Returns: The encrypted message extracted from the image (string)
def revealMessage(imagePath, messageLen):
	im = Image.open(imagePath)
	imData = list(im.getdata())
	encMessage = ""

	for i in range(messageLen):
		encMessage += extractChar(imData[i])

	return encMessage

# Builds a character from the least significant bits of the values in pixel
# @pixel The pixel to extract a character from (tuple(int, int, int, int))
# Returns: The character extracted from pixel (char)	
def extractChar(pixel):
	global extractLSB

	charNum = 0
	for i, value in enumerate(pixel):
		leastSigBits = value & extractLSB
		charNum |= leastSigBits
		if(i != len(pixel)-1):
			charNum = (charNum << 2)

	return chr(charNum)


# Transform characters in the message to 4 sets of 2 bits each.
# @message The message to hide in the image (string)
# Returns: The message represented as stated above (list[(int,int,int,int), ...])
def prepMessage(message):
	global extractLSB

	firstBits = 0
	secondBits = 0
	thirdBits = 0
	fourthBits = 0
	messageBits = []

	for char in message:
		charNum = ord(char)
		firstBits = (charNum >> 6) & extractLSB
		secondBits = (charNum >> 4) & extractLSB
		thirdBits = (charNum >> 2) & extractLSB 
		fourthBits = charNum & extractLSB
		messageBits.append((firstBits, secondBits, thirdBits, fourthBits))
	
	return messageBits

# Encodes char into pixel
# @char The character to encode (tuple(int, int, int, int)) 
# @pixel The pixel to be changed (tuple(int, int, int, int)) 
# Returns: The new pixel with char hidden in the least significant bits (tuple(int, int, int, int)) 
def encodePixel(char, pixel):
	newPixel = []
	for i, value in enumerate(pixel):
		newPixel.append(((value >> 2) << 2) | char[i])
	return tuple(newPixel)