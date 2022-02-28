import pandas as pd
import numpy as np
import zipfile
import re
from termcolor import colored

DICT_MAIN_PATH = 'data/dict_main.zip'

class Wordle:
    def __init__(self,data,n=5,first=True):
        if first is True:
            print('Welcome to \033[1mWORDLE!\n\033[0m')
            self.data = data[data['len']==n].reset_index(drop=True)
        self.word = self.data['word'][np.random.randint(len(self.data))]

    def guess(self):
        t = 1
        keys = {}
        colors = ['\033[38;5;254m','\033[38;5;239m','\033[38;5;214m','\033[38;5;36m']
        for a in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            keys[a] = 0
        match = np.zeros(len(self.word),dtype=int)
        while min(match) < 3:
            m = ''
            myguess = input('Guess '+str(t)+': ')
            if len(myguess) != len(self.word):
                print('Please choose a '+str(len(self.word))+'-letter word!')
                continue
            else:
                for c in range(len(myguess)):
                    if myguess[c] == self.word[c]:
                        match[c] = keys[myguess[c]] = 3
                    elif (myguess[c] in self.word) and (myguess[c] != self.word[c]):
                        match[c] = keys[myguess[c]] = 2
                    else:
                        match[c] = keys[myguess[c]] = 1
                if min(match) != 3:
                    t += 1
                for s in myguess:
                    m += '\033[1m'+colors[keys[s]]+' '+s
                m += '   :   '
                for s in keys.keys():
                    m += colors[keys[s]]+' '+s
                print(m)
                if min(match) == 3:
                    print('you got it in '+str(t)+' tries :)\n')
                    replay = input('Do you want to play again? y/n : ')
                    if replay == 'y':
                        self.__init__(self.data,first=False)
                        self.guess()
                    else:
                        break

if __name__ == '__main__':
    dict_main = pd.read_csv(zipfile.ZipFile(DICT_MAIN_PATH).open(re.sub('zip$','csv',DICT_MAIN_PATH)))
    word = Wordle(dict_main)
    word.guess()

