from bs4 import BeautifulSoup
import numpy as np
import re
import glob
import os

class html_preprocess():

    def __init__(self, path):
        self.path = path

    def read_content(self):
        dir = os.listdir(self.path)

        read_in = 0
        not_wrote = 0

        for html in dir[:5]:
            with open(self.path + html, 'r') as f:
                try:
                    self.html_clean = self.soup(f.read())
                except:
                    read_in += 1
            
            with open(self.path + 'html_clean/'+html, 'w') as f:
                try:
                    f.write(self.html_clean)
                except:
                    not_wrote += 1
        
        if read_in != 0 or not_wrote != 0:
            print(read_in, 'html documents not read in', '\n')
            print(not_wrote, 'html documents not wrote out', '\n')
        else:
            print('Success :)')

    def soup(self, html_content):

        souped = BeautifulSoup(html_content, 'html.parser')
        data = souped.get_text().replace('\n', '. ')
        
        return data


if __name__ == '__main__':
    
    path = '/Users/wastechs/Documents/data/roam_clean/'
    html_preprocess(path).read_content()



      

    