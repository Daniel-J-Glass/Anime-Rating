import re
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
import webbrowser
import urllib
import time

def get_data(anime):
    query = urllib.parse.quote_plus(anime)

    google_url = "https://www.google.com/search?q=site:myanimelist.net+" + query +"&num=" + str(5)

    #print(response.content)
    #with open('output.html', 'wb') as f:
    #    f.write(response.content)
    #webbrowser.open('output.html')

    response = requests.get(google_url)
    soup = BeautifulSoup(response.content,features="lxml")

    links = []
    for link in soup.find_all("a",href=re.compile("(?<=/url\?q=)(htt.*://.*)")):
        links.append(re.split(":(?=http)",link["href"].replace("/url?q=","")))

    anime_url = links[0][0].strip()
    response = requests.get(anime_url)
    soup = BeautifulSoup(response.content,features="lxml")
    title = soup.findAll('span',{'itemprop':'name'})[0]
    title = re.findall('>.+?<', str(title))[0][1:-1]
    score = soup.findAll('div',{'data-title':'score'})
    score = str(re.findall(r"\d\.\d\d", strB(score))[0])
    return title,score,anime_url

def parse_raw(raw_string):
    list = raw_string.split(',')
    for i,anime in enumerate(list):
        list[i] = re.sub('\(.+?\)', '', anime.strip())
    return list

def same_list(list1,list2):
    for i in list1:
        if list2[0] == i[0]:
            return True
    return False

if __name__ == "__main__":
    raw = open('AnimesRaw.txt','r')
    raw_anime_list = raw.read()
    raw.close()

    #wiping raw file
    open('AnimesRaw.txt','w').close()
    new_list = []
    if raw_anime_list.strip() is not None:
        new_list = [get_data(i) for i in parse_raw(raw_anime_list) if i]
    clean_anime = open('Animes.txt','r')
    old_list = [i.strip().split("\t") for i in clean_anime.readlines() if i is not '\n']
    clean_anime.close()

    for i in new_list:
        time.sleep(1)
        old_list.append(i)

    save_list = []
    for i in old_list:
        if not same_list(save_list,i):
            save_list.append(i)

    save_list.sort(key=lambda tup: tup[1], reverse=True)
    open('Animes.txt','w').close()
    clean_anime = open('Animes.txt','w')
    for anime in save_list:
        clean_anime.write("\t".join(anime)+"\n")
