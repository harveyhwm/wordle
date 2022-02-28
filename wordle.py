import pandas as pd
import numpy as np
import zipfile
import re,os

# allows us to invoke from any directory
DICT_DIR = os.path.dirname(os.path.realpath(__file__))+'/data/'
DICT_MAIN_PATH = 'dict_main.zip'

class Wordle:
    def __init__(self,data,n=5,first=True):
        if first is True:
            print('Welcome to \033[1mWORDLE!\n\033[0m')
            self.n = n
            self.data = data[data['len']==self.n].reset_index(drop=True)
        self.word = self.data['word'][np.random.randint(len(self.data))]
        self.keys = {}

    # the n+1 keys save the state of each letter in your current guess, with the final one used to store the letter state in your guess history
    def set_keys(self,save_letters=False):
        for a in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            if save_letters is False:
                self.keys[a] = list(np.zeros(self.n+1,dtype=int))
            else:
                self.keys[a] = list(np.zeros(self.n,dtype=int))+[self.keys[a][self.n]]

    def guess(self):
        t = 1
        # ansi escape codes for light grey, dark grey, orange and green
        colors = ['\033[38;5;254m','\033[38;5;239m','\033[38;5;214m','\033[38;5;36m']
        match = np.zeros(self.n,dtype=int)
        self.set_keys()
        while min(match) < 3:
            m = ''
            myguess = input('Guess '+str(t)+' : ')
            if len(myguess) != self.n:
                print('Please choose a '+str(self.n)+'-letter word!')
                continue
            else:
                guessmap = []
                for c in myguess:
                    guessmap.append(self.keys[c][0])
                    self.keys[c][0] += 1
                self.set_keys(save_letters=True)
                for i,c in enumerate(myguess):
                    if c == self.word[i]:
                        match[i] = self.keys[c][guessmap[i]-1] = 3
                    elif (c in self.word) and (c != self.word[i]):
                        match[i] = self.keys[c][guessmap[i]-1] = 2
                    else:
                        match[i] = self.keys[c][guessmap[i]-1] = 1
                    self.keys[c][self.n] = max(self.keys[c][self.n],match[i])
                    m += '\033[1m'+colors[match[i]]+c+' '+'\033[1m'
                m += '  :   '
                for s in self.keys.keys():
                    m += '\033[1m'+colors[self.keys[s][self.n]]+' '+s+'\033[1m'
                m += '\033[0m'
                print(m)
                if min(match) == 3:
                    print('you got it in '+str(t)+' tries :)\n')
                    replay = input('Do you want to play again? y/n : ')
                    if replay == 'y':
                        self.__init__(self.data,first=False)
                        self.guess()
                    else:
                        break
                else:
                    self.set_keys(save_letters=True)
                    t += 1
        return 'You got it in '+str(t)+' tries :)'

if __name__ == '__main__':
    dict_main = pd.read_csv(zipfile.ZipFile(DICT_DIR+DICT_MAIN_PATH).open(re.sub('zip$','csv',DICT_MAIN_PATH)))
    word = Wordle(dict_main)
    word.guess()

