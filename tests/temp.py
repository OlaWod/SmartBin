'''
import pygame
pygame.mixer.init()
pygame.mixer.music.load('aisay.mp3')
pygame.mixer.music.play()
'''

'''
import os
os.system('mpg123 '+'aisay.mp3')
'''

'''
from playsound import playsound
playsound('aisay.mp3')
'''

import pandas as pd
rubbish = pd.read_csv('./assets/rubbish.csv', encoding='gbk')
trash_harm = list(rubbish["有害垃圾"])
print(trash_harm)
