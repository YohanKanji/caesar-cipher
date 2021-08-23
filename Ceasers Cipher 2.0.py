#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 22:11:08 2020

@author: yohankanji
"""

import time
import string

lowercase = string.ascii_lowercase
skips = ['.', ':', ';', "'", '"', '(', ')', '%', ' ']

def encrypt(decrypted_message, key):
    encrypted_message = ''
    for i in range(len(decrypted_message)):
        character = decrypted_message[i]
        if character != ' ' and character != '.' and character != ',' and character != ':':
            index = ord(character) - 97
            new_index = index + key
            while new_index > 25:
                new_index = new_index - 26
            newCharacter = lowercase[new_index]
            encrypted_message += newCharacter
        else:
            encrypted_message += character
    return encrypted_message

def check_decryption(found_decrypted_message):
    with open('/Users/dillipkanji/Desktop/2020/corncob_lowercase.txt', 'r', encoding = 'UTF-8') as current_file:
        text = current_file.read()
        text = text.replace('\n', '').replace('\r', '')           
    englishWordCount = 0
    totalWords = 0
    for word in found_decrypted_message.split(" "):
        totalWords += 1
        if word in text:
           englishWordCount +=1        
    englishWordPercentage = (englishWordCount/totalWords) * 100
    return englishWordPercentage

def letter_frequency(encrypted_messagee):
    print(' ') ; print('Conducting Frequency Anaylasis ...')
    word_counts = {}
    for letter in encrypted_message:
        if letter not in skips:
            if letter in word_counts:
                word_counts[letter] +=1 
            else:
                word_counts[letter] = 1
    max_key = max(word_counts, key = word_counts.get) # most occuring letter
    print(' ') ; print('The most occuring letter is: ', max_key)
    indexNumber = lowercase.index(max_key)
    fromE = indexNumber - 4
    return fromE

def single_letter_words(encrypted_message):
    singles = []
    for singleLetter in encrypted_message.split(" "):
        if len(singleLetter) == 1:
            if singleLetter not in singles:
                singles.append(singleLetter)
    
    if len(singles) == 2:
        position0 = lowercase.index(singles[0])
        position1 = lowercase.index(singles[1])
        return position0, position1
    elif len(singles) == 1:
        position0 = lowercase.index(singles[0])
        return position0
    else:
        return None
    
def decrypt(encrypted_message, key):
    decrypted_message = ''  
    for i in range(len(encrypted_message)):
            character = encrypted_message[i]
            if character not in skips:
                index = ord(character) - 97
                new_index = index - key
                newCharacter = lowercase[new_index]
                decrypted_message += newCharacter
            else:
                decrypted_message += character
    return decrypted_message
    
def bute_force(encrypted_message):
    print(' ') ; print('Using Brute Force ...')
    test_decrypted_message = ''
    print(' ')
    for key in range(26):
        print('Attempt = ', key)
        test_decrypted_message = ''
        for i in range(len(encrypted_message)):
            character = encrypted_message[i]
            if character not in skips:
                index = ord(character) - 97
                new_index = index - key
                newCharacter = lowercase[new_index]
                test_decrypted_message += newCharacter
            else:
                test_decrypted_message += character
        
        isEnglish = check_decryption(test_decrypted_message)
        if isEnglish > 50:
            return test_decrypted_message
    
userInput = input("Enter 'E' to Encrypt or 'D' to Decrypt: ")
userInput = userInput.lower()

if userInput == 'e':
    
    decrypted_message = input("Enter Text To Encrypt: ")
    start = time.time()
    decrypted_message = decrypted_message.lower()
    key = input("Enter Encryption Key: ")
    key = int(key)
    message = encrypt(decrypted_message, key)
    end = time.time()
    print(' ') ; print(message)
    print(' ') ; print('Time Taken = ', end - start, 'seconds')
    
elif userInput == 'd':

    encrypted_message = input("Enter Text To Decrypt: ")
    start = time.time()
    encrypted_message = encrypted_message.lower()
    key = None
    
    if len(encrypted_message) > 250: # conduct frequency anaylasis
        fromE = letter_frequency(encrypted_message)
        singleW = single_letter_words(encrypted_message)
        
        if type(singleW) == tuple: # there are two positions for letters a & i
            if singleW[0] - fromE == 0 or singleW[1] - fromE == 0: 
                key = fromE # if one letter's index - space from e is 0 (a), then the key is the number the most frequent letter is from e
       
        elif type(singleW) == int:
            if singleW - fromE == 0 or singleW - fromE == 8:
                key = fromE  
        
        elif type(singleW) == None:
            decrypted_message = bute_force(encrypted_message) 
                
        if key != None:
            found_decrypted_message = decrypt(encrypted_message, key)
            isEnglish = check_decryption(found_decrypted_message) 
        
            if isEnglish > 50:
                print('Common English = ', isEnglish, '%')
                decrypted_message = found_decrypted_message
                end = time.time()
                
        elif key == None:
            decrypted_message = bute_force(encrypted_message) 
            end = time.time()
    
    else:
        decrypted_message = bute_force(encrypted_message) 
        end = time.time()

    
    print(' ') ; print('Decrypted Message ...')
    print(' ') ; print(decrypted_message) 
    print(' ') ; print('Time Taken = ', end - start, 'seconds')

else:
    print(' ') ; print("To use this program, please restart the console and enter either 'E' or 'D'")
        

    
    
        

