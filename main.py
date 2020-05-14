import os
import sys
import keys
from yandex import Translater
from time import sleep
from tqdm import tqdm
import colorama
import keyboard

colorama.init(autoreset=True)

tr = Translater.Translater()
tr.set_key(keys.KEY)
tr.set_from_lang('en')
tr.set_to_lang('ru')

firstWords = []
translatedWords = []
readyWords = []

class File(object):
    def __init__(self, filename):
        self.filename = filename
        if os.path.exists(filename) == False:
            file = open(filename, 'w')
            file.close()
            print(colorama.Fore.GREEN + 'File created ' + colorama.Fore.BLUE + str(self.filename)[:-4].upper() + colorama.Fore.GREEN + ' succesfully. Press ENTER to continue.')
            keyboard.wait('Enter')

    def writeToFile(self, list): 
        with open(self.filename, 'w') as f:
            for line in list:
                f.write(line + '\n')
    
    def readFromFile(self, listTO):
        for i in range(0, len(listTO)):
            listTO.pop(i)

        with open(self.filename, 'r') as f:
            for line in f:
                listTO.append(line)

class Array(object):
    @staticmethod
    def deleteGaps(array):
        for i in range(0, len(array)):
            array[i] = array[i].strip()
        
f = File('translated.txt')
ready = File('output.txt')
f.readFromFile(firstWords)
if len(firstWords) == 0:
    print(colorama.Fore.RED + 'No words given!')
    sleep(3)
    sys.exit(0)
    
Array.deleteGaps(firstWords)

print(colorama.Fore.MAGENTA + 'Starting...' + colorama.Fore.RESET)

errorsCount = 0

for i in tqdm(range(0, len(firstWords)), desc='Translating words: ', unit=' words'):
    tr.set_text(firstWords[i])
    translatedWords.append(tr.translate())

for i in tqdm(range(0, len(translatedWords)), desc='Checking words: ', unit=' words'):
    word = translatedWords[i]
    tr.set_text(translatedWords[i])
    if tr.detect_lang() == 'en':
        translatedWords[i] = '---!' + word.upper() + '!---'
        errorsCount += 1

Array.deleteGaps(translatedWords)

for i in range(0, len(firstWords)):
    readyWords.append(firstWords[i].lower() + ' = ' + translatedWords[i].lower())

similarWords = []

for i in tqdm(range(0, len(readyWords)), desc='Collecting similar words: '):
    if readyWords.count(readyWords[i]) > 1:
        similarWords.append(readyWords[i])

similarWordsCount = len(set(similarWords))

if similarWordsCount > 0:
    print(colorama.Fore.GREEN + 'Similar words: ' + colorama.Fore.RED + str(similarWordsCount))
    print(colorama.Fore.LIGHTCYAN_EX + 'Deleting similar words...')
else:
    print(colorama.Fore.GREEN + 'Similar words: ' + colorama.Fore.YELLOW + str(similarWordsCount))

finalWords = sorted(set(readyWords))

if errorsCount > 0:
    print((colorama.Fore.GREEN + 'Words untranslated: ') + (colorama.Fore.RED + str(errorsCount)))
else:
    print((colorama.Fore.GREEN + 'Words untranslated: ') + (colorama.Fore.YELLOW + str(errorsCount)))

ready.writeToFile(finalWords)

print(colorama.Fore.MAGENTA + 'Done.')
print('Press ' + colorama.Fore.CYAN + 'ENTER' + colorama.Fore.RESET + ' to exit...')
keyboard.wait('Enter')