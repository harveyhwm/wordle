import pandas as pd
import zipfile
import re

DICT_WIKI_PATH = 'data/dictionary_lowercase.zip'
DICT_WORD_PATH = 'data/wikipedia_en.zip'

dict_wiki = zipfile.ZipFile(DICT_WIKI_PATH)
dict_wiki = pd.read_csv(dict_wiki.open(re.sub('zip$','txt',DICT_WIKI_PATH)),header=None,names=['word'])
dict_wiki['word'] = dict_wiki['word'].apply(lambda x: str(x).upper())
dict_wiki = dict_wiki.drop_duplicates()

dict_word = zipfile.ZipFile(DICT_WORD_PATH)
dict_word = pd.read_csv(dict_word.open(re.sub('zip$','txt',DICT_WORD_PATH)),sep=' ',header=None,names=['word','len','instances','articles'])
dict_word['word'] = dict_word['word'].apply(lambda x: str(x).upper())
dict_word = dict_word.groupby(['word','len']).sum().sort_values(by='instances',ascending=False).reset_index()

dict_master = dict_word.merge(dict_wiki,how='inner',on='word',sort=False)
dict_master.to_csv('dict_master.zip',compression=dict(method='zip',archive_name='dict_master.csv'))
