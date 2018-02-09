"""
Paul Davis
Steganography Project

How to run this program:
	1. Be working on an Macintosh OS
		- It should work on any OS, but I will only be outlining exactly 
		how I have it set up on my machine

	2. Open a terminal and install Homebrew Package Manager for Mac OS
		- This command should install it:
		/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

	3. Run the command "brew install python"
	
	4. If PIL (Python Image Library) is installed, UNINSTALL IT BEFORE CONTINUING

	5. Now you should be able to run the command "pip2 install pillow"

	6. Download Steg.py, Pad.py, and Run_Steg.py and save them to a folder

	7. Open a terminal, navigate to the folder

	8. Type the command "python2.7 Run_Steg.py"
		- You MUST use Python 2.7 or the program may not work

	9. Follow the on screen prompts for the program
"""

import Pad
import Steg

if __name__ == "__main__":
	mode = Pad.getMode()
	while(mode != "quit"):
		if(mode == "hide"):
			message = Pad.getMessage()
			keyMes = Pad.encryptMessage(message)
			Pad.writeKeyList(keyMes[0])
			encMessage = keyMes[1]
			coverPath = Steg.getCoverPath()
			savePath = Steg.getSavePath()
			Steg.hideMessage(encMessage, coverPath, savePath)

		if(mode == "reveal"):
			imagePath = Steg.getEncImagePath()
			keyList = Pad.getKeyList()
			encMessage = Steg.revealMessage(imagePath, len(keyList))
			decMessage = Pad.decryptMessage(encMessage, keyList)
			print("\nThe hidden message is: " + decMessage)

		mode = Pad.getMode()
