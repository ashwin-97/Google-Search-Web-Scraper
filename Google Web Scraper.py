import pandas as pd
import numpy as np
import urllib.request 
from bs4 import BeautifulSoup
import bs4
import requests
from fake_useragent import UserAgent
import re


def remove(list):          #Function later used to remove regexes
    pattern = '[0-9]'
    list = [re.sub(pattern, '', i) for i in list] 
    return list


int main()
    number_result = 100
    ua = UserAgent()
    google_url = "https://www.google.com/search?source=hp&ei=Ro4FX7fGBLWKmge_z6foAQ&q=slum%2C+mexico%2C+2018&oq=slum%2C+mexico%2C+2018&gs_lcp=CgZwc3ktYWIQAzoICAAQsQMQgwE6AggAOgUIABCxAzoGCAAQFhAeOgUIIRCgAToECCEQFVCLLliqYmCZZ2gBcAB4AIABowGIAawTkgEEMC4xOZgBAKABAaoBB2d3cy13aXo&sclient=psy-ab&ved=0ahUKEwi3gbOxqL3qAhU1heYKHb_nCR0Q4dUDCAc&uact=5"
    params = {
        'num': 100,
        'start': 1
    }
    response = requests.get(google_url, params=params)
    soup = BeautifulSoup(response.text, "html.parser")

    result_div = soup.find_all('div', attrs = {'class': 'ZINbbc'})

    links = []
    links1= []
    links2= []
    links3= []
    titles = []
    descriptions = []
    news_contents=[]
    news_contents1=[]





    for r in result_div:
        # Checks if each element is present, else, raise exception
        try:

            link = r.find('a', href = True) 
            title = r.find('div', attrs={'class':'vvjwJb'}).get_text()
            description = r.find('div', attrs={'class':'s3v9rd'}).get_text()

            # Check to make sure everything is present before appending
            if link != '' and title != '' and description != '': 
                links.append(link['href'])
                titles.append(title)
                descriptions.append(description)
        # Next loop if one element is not present
        except:
            continue
    for i in range (0, len(links)):
     if (links[i].endswith('pdf')==False):
        links1.append(links[i])

    to_remove = []
    clean_links = []
    clean_links1 = []
    for i, l in enumerate(links):
        clean = re.search('\/url\?q\=(.*)\&sa',l)

        # Anything that doesn't fit the above pattern will be removed
        if clean is None:
            to_remove.append(i)
            continue
        clean_links.append(clean.group(1))
        for i in range(0, len(clean_links)):
         if(clean_links[i].endswith('pdf')==False):
            clean_links1.append(clean_links[i])

    # Remove the corresponding titles & descriptions
    for x in to_remove:
        del titles[x]
        del descriptions[x]
    n=len(links1)

    for i in range(0, len(clean_links)):
        page = requests.get(clean_links1[i])
        soup = BeautifulSoup(page.content, 'html.parser', from_encoding="iso-8859-1")
        soup.find_all('p')
        for g in range(0, len(soup.find_all('p'))):
          soup.find_all('p')[g].get_text().split(".")
          news_contents.append(soup.find_all('p')[g].get_text().split("."))

    for i in range(0, len(news_contents)):
     for j in range(0, len(news_contents[i])):
        news_contents1.append(news_contents[i][j])

    #Data Cleaning
    finarr=titles+news_contents1    #merge titles and content
    finarr1=remove(finarr)        
    spec_chars = ["!",'"',"#","%","&","'","(",")",
                  "*","+",".","/",":",";","<",
                  "=",">","?","@","[","\\","]","^","_",
                  "`","{","|","}","~"]    #characters to remove

    df=pd.DataFrame(finarr1, columns = ['news_content'])
    for char in spec_chars:
        df['news_content']= df['news_content'].str.replace(char, ' ')


    # Data cleaning part 2
    df.replace('', np.nan, inplace=True)
    df.replace(' ', np.nan, inplace=True)
    df.replace('  ', np.nan, inplace=True)
    df.drop_duplicates()
    df.dropna(inplace=True)

    df.to_excel("Mexico.xlsx")
