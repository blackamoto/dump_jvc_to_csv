import os
import glob
import random
import time
import pandas as pd
from jvc import *


if not os.path.isfile('last_page_saved.txt'):
    last_page_saved_file=open('last_page_saved.txt', 'w')
    last_page_saved_file.write('1')
    last_page_saved_file.close()
    last_page_saved=1


else:
    last_page_saved_file = open("last_page_saved.txt", 'r')
    last_page_saved=int(last_page_saved_file.read())
    last_page_saved_file.close()



a=[]
start = 1 # page de départ
max=4238 # page max du topic
buff=0 # ne pas toucher 
max_buff = 20 # nombre de pages avant sauvegarde partielle en .csv 

for i in range(min(start,last_page_saved),max):

    Posts = getPosts('https://www.jeuxvideo.com/forums/42-3011927-61017614-'+str(i+1)+'-0-1-0-blabla-alerte-btc.htm')
    print(i+1,'/', max )
    buff=buff+1
    time.sleep(random.random())
    if buff==max_buff:
        buff=0
        df=pd.DataFrame(a)
        df.to_csv('alerte_btc_{}'.format(i))
        time.sleep(random.random()*10) # attendre de manière aléatoire entre 1 et 10 secondes toute les 20 pages pour ne pas éveiller les soupçons et se faire ban IP
        last_page_saved = open("last_page_saved.txt", "w")
        last_page_saved.write(str(i))

    for post in Posts:
        a.append(post)
        #print(post)
         
def rassembler_fichiers()->pd.DataFrame:
  all_files = glob.glob("./alerte_btc*")
  li=[]
  for filename in all_files:
      df = pd.read_csv(filename, index_col=None, header=0)
      li.append(df)

  frame = pd.concat(li, axis=0, ignore_index=True)
  frame = frame.drop_duplicates()
  frame.to_csv('FULL.csv')
  return frame
