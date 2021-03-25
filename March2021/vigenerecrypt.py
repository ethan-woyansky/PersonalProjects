#Takes a message and a key and returns cipher text, using the Vigenère method
#https://en.wikipedia.org/wiki/Vigenère_cipher

import string
import collections
import easygui as eg #For easy entry. Would like to expand to Tkinter.

alphabet = collections.deque(string.ascii_lowercase.upper()) #alphabet = ['A', 'B', ... , 'Y', 'Z']
alphaValues = dict(zip(string.ascii_lowercase.upper(), range(0,26))) #alpahbet2 = {'A': 1, 'B': 2, ... 'Y': 25, 'Z': 26}
alphaRValues = {value: key for key, value in alphaValues.items()}

def vigenereEncrypt(message, key):
    message = message.upper()
    key = key.upper()
    myCipherText = ''
    z = 0
    i = 0

    lengthDiff = len(message) - len(key) #If the key is shorter than the message, it loops through itself again until it is the length of the message.
    while i < lengthDiff:                #Example: message = 'ethanwoyansky', key = 'key'. the key now becomes 'keykeykeykeykeyk'
        key = key + key[i]               #Example 2: message = 'just google it', key = 'asdf'. the key now becomes 'asdfasdfasdf'
        i += 1

    print(key)

    #Constructing the cipher text
    for x in message:

        if x.isspace() == True: #There is no value for spaces, so I concatenate them to the cipher text and continue
            myCipherText += ' '
            continue

        elif x.isalpha() == False: #Vigenère didn't plan for numbers or special characters.
            myCipherText += x
            continue

        xAlphaVal = alphaValues[x] #
        alphabet.rotate(-xAlphaVal) #Rotate the list of letters so that the first value is equal to x
        zAlpha = key[z]                 #zAlpha gives us the corresponding letter in the key to evaluate x
        keyVal = alphaValues[zAlpha]    #keyVal is the index for which we'll look in alphabet to find our corresponding cipher letter
        cipherVal = alphabet[keyVal] 
        myCipherText += cipherVal      #Concatenate cipherVal to myCipherText and continue
        alphabet.rotate(xAlphaVal) #Rotate the list of letters back to its intial position
        z += 1
        
    return myCipherText

###Invert the encryption process
def vigenereDecrypt(message, key):
    message = message.upper()
    key = key.upper()
    myCipherText = ''
    i = 0
    z = 0

    lengthDiff = len(message) - len(key) 
    while i < lengthDiff:                
        key = key + key[i]               
        i += 1

    key = key.replace(' ', '')
    print(key)
    for x in key:

        if x.isalpha() == False:
            myCipherText += x
            z += 1
            continue

        elif message[z].isspace() == True:
            myCipherText += ' '
            z += 1
            continue

        elif message[z].isalpha() == False:
            myCipherText + message[z]
            z += 1
            continue

        xAlphaVal = alphaValues[x]
        alphabet.rotate(-xAlphaVal)
        myVal = alphabet.index(message[z])
        cipherVal = alphaRValues[myVal]
        myCipherText += cipherVal
        alphabet.rotate(xAlphaVal) 
        z += 1
    return myCipherText

while True:

    msg = 'Please choose: Encryption or Decryption?'
    title = 'Vigenère Encryption'
    choices = ['Encryption', 'Decryption']
    cryptChoice = eg.buttonbox(msg, title, choices)

    if cryptChoice == 'Encryption':
        eMsg = 'Please enter a message to be encrypted and the key to decrypt it.'
        title = 'Vigenère Encryption'
        fieldNames = ['Message:', 'Key:']
        fieldValues = []
        fieldValues = eg.multenterbox(eMsg, title, fieldNames)
        finalmsg = vigenereEncrypt(fieldValues[0], fieldValues[1])
        eg.msgbox(msg = f'Your cipher is {finalmsg}. \nYour key is {fieldValues[1].upper()}.', title='Cipher', ok_button="OK")

    elif cryptChoice == 'Decryption':
        dMsg = 'Please enter a message to be decrypted and the key that encrypted it.'
        title = 'Vigenère Decryption'
        fieldNames = ['Message:', 'Key:']
        fieldValues = []
        fieldValues = eg.multenterbox(dMsg, title, fieldNames)
        finalmsg = vigenereDecrypt(fieldValues[0], fieldValues[1])
        eg.msgbox(msg = f'Your original message is {finalmsg}.', title='Original Message Decrypted', ok_button="OK")

    msg = "Do you want to continue?"
    title = "Vigenère Encryption" 
    if eg.ccbox(msg, title):
        pass
    else:
        break
