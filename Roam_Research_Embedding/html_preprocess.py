from bs4 import BeautifulSoup
import numpy as np
import re
import glob
import os
import pandas as pd

class html_preprocess():

    def __init__(self, path):
        self.path = path

    def read_content(self):
        dir = os.listdir(self.path)

        read_in = 0
        not_wrote = 0

        for html in dir:
            with open(self.path + html, 'r') as f:
                try:
                    self.html_clean = self.soup(f.read())
                    df = pd.DataFrame({'content': [self.html_clean]})
                    df.to_csv(self.path + 'html_clean/' + html[:-3] + '.csv')
                except:
                    read_in += 1

        if read_in != 0: 
            print(read_in, 'html documents not read in', '\n')
        else:
            print('Success :)')

    def soup(self, html_content):

        souped = BeautifulSoup(html_content, 'html.parser')
        data = souped.get_text().replace('\n', '. ')
        data = data.replace('__', '')
        data = data.replace('|', '')
        data = data.replace('[[]]', '')
        data = data.replace('- via', '')
        data = data.replace('Tags:', '')
        
        return data


if __name__ == '__main__':
    
    path = '/Users/wastechs/Documents/data/roam_clean/'
    html_preprocess(path).read_content()