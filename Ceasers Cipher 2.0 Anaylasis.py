#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 22:11:08 2020

@author: yohankanji
"""

# open files, encrypt them, then save, the decrypt
# loop over text files in a folder and open them. encryypt file with key 2 record time taken and save temporarily
# then decrypt that file using frequency anayalsis and brute force, record time taken for both
# let the x-axis be the length of the text and saved in the list called xs_length
# Plot two different graphs both using time for the y-axis and length for the x-axis

import time ; import string
import matplotlib.pyplot as plt
import os ; import pylab

xs_length = []
ys_e_time = []
ys_d_time = []
ys_dBF_time = []

lowercase = string.ascii_lowercase
skips = ['.', ':', ';', "'", '"', '(', ')', '%', ' ', '$', '!']

def read_book(title_path):
    '''
    opens and reads a .txt using it's title path 
    and replaces all the special characters
    returns the text as a string
    '''
    with open(title_path, 'r', encoding = 'UTF-8') as current_file:
        text = current_file.read()
        text = text.replace('\n', '').replace('\r', '')
    return text

def encrypt(decrypted_message, key):
    '''
    Takes English text and a key (int) and increments that
    letter by that key eg incrementing a by 1 becomes b.
    It uses the special number that python gives each 
    character. a is 97. It returns the encrypted message
    '''
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
    '''
    This function takes the result of the decrypt function
    and checks each word to see if it is in a .txt file of 
    common english words. If so, it increments the count 
    by one. I then calculates what percetage of words are 
    common english words and returns that percentage.
    '''
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

def letter_frequency(encrypted_message):
    '''
    This function is used when decrypting a message. I takes
    the encrypted message and loops over each letter and
    records it's frequency in a dictionary. This function finds
    the key in the dictionary with the largest value.
    
    Because the most occuring letter in English is 'e', we will
    find the number of spaces that the most frequent letter 
    is from e which has an index of 4.
    '''
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
    '''
    This function takes the encrypted message as it's input. 
    It looks for lingle letter words - a and i equivelent.
    If there are single letter words in te text, they will be
    appended to a dictionary. The maximum number of objects
    in the singles dictionary is 2. The index of that 
    letter is also found.
    '''
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
    '''
    This function takes the encypted message and the key that
    was calculated. The letters and decrement them by that number
    it returns the decrypted message back to the caller.
    '''
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
    
def brute_force(encrypted_message):
    '''
    This function is called when frequency anaylasis fails.
    It increments the letters by 0, 1, then 2 etc. It then
    checks if 50% of the words are common english, if so,
    that is the decrypted message and is retured. If not, the
    messgae is decrypted using the next key.
    '''
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
        
for filename in os.listdir('/Users/dillipkanji/Desktop/2020/texts/'):
    if filename.endswith(".txt"):
        currentfile = os.path.join('/Users/dillipkanji/Desktop/2020/texts/', filename)
        print(' ') ; print(currentfile)
        decrypted_message = read_book(currentfile)
        xs_length.append(len(decrypted_message))

        start_encrypt = time.time()
        decrypted_message = decrypted_message.lower()
        encrypted_message = encrypt(decrypted_message, 3)
        end_encrypt = time.time()
        
        print(' ') ; print('Time Taken = ', end_encrypt - start_encrypt, 'seconds')

        start_decrypt = time.time()
        key = None
        
        if len(encrypted_message) > 250:
            fromE = letter_frequency(encrypted_message)
            singleW = single_letter_words(encrypted_message)
            
            if type(singleW) == tuple: 
                if singleW[0] - fromE == 0 or singleW[1] - fromE == 0: 
                    key = fromE
           
            elif type(singleW) == int:
                if singleW - fromE == 0 or singleW - fromE == 8:
                    key = fromE  
                    
            if key != None:
                found_decrypted_message = decrypt(encrypted_message, key)
             
            isEnglish = check_decryption(found_decrypted_message) 
            
            if isEnglish > 50:
                print(' ') ; print('Common English = ', isEnglish, '%')
                decrypted_message = found_decrypted_message
                end_decrypt = time.time()
                
        ys_e_time.append(end_encrypt - start_encrypt)
        ys_d_time.append(end_decrypt - start_decrypt)
    
        print(' ') ; print('Time Taken For Decryption = ', end_decrypt - start_decrypt, 'seconds')
        
    start_BF = time.time()
    decrypted_message_BF = brute_force(encrypted_message) 
    end_BF = time.time()
    ys_dBF_time.append(end_BF - start_BF)
    
s = sorted(zip(xs_length, ys_e_time, ys_d_time, ys_dBF_time))
xs_length, ys_e_time, ys_d_time, ys_dBF_time = map(list, zip(*s))
        
plt.figure()
plt.plot(xs_length, ys_e_time, label = "Encryption")
plt.plot(xs_length, ys_d_time, label = "Decryption")
plt.xlabel('Length of Text')
plt.ylabel('Time Taken - Frequency Analysis (s)')
plt.title('Encryption and Decryption Time of Texts')
plt.legend()
plt.show()

plt.figure()
plt.plot(xs_length, sorted(ys_dBF_time), label = "Brute Force")
plt.plot(xs_length, ys_d_time, label = "Frequency Analysis")
plt.xlabel('Length of Text')
plt.ylabel('Time Taken (s)')
plt.title('Frequency Analysis VS Brute Force')
plt.legend()
plt.show()

        
