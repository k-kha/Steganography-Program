# Steganography Encryption System

The code isn't entirely organized and the variable names aren't as clear, due to time constraints.

Dependencies:
The program requires Python 3.
The program should be executed in Python 3.7.
(There are some problems with Python 3.8)
The following libraries will be needed:
numpy, cryptography
These libraries should already be installed, but install if needed:
PIL, sys, base64

Change the directory to the project root directory.

How to Run
steganography.py takes 4 command line arguments:
First arguement:
The program name.

Second argument:
   -e, 		for encoding the message into the picture
   -d, 		for decoding the message out of the picture

Third argument:
Any text file with message to hide.

Fourth argument:
For -e, any picture you wish to hide your message in.
For -d, Secret_Image.png has to be used.

Examples:
$ python steganography -e message.txt image1.png
#  then
$ python steganography -d message.txt Secret_Image.png

Outputs:
The first line is just to encrypt and then encode the message into the picture. Nothing interesting happens, but
a Secret_Image.png should pop out after running the first line.
The second line will decrypt and decode the message from the picture and print it.
