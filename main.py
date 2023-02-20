import pandas as pd
import numpy as np
import urllib.request 
from bs4 import BeautifulSoup
import bs4
import requests
import re
from fake_useragent import UserAgent


def remove_numbers(list):
    # Remove digits from strings in the given list
    pattern = '[0-9]'
    return [re.sub(pattern, '', i) for i in list] 


def get_clean_links(links):
    # Extract clean links from the Google search results
    clean_links = []
    for l in links:
        clean = re.search('\/url\?q\=(.*)\&sa',l)
        if clean is not None and not clean.group(1).endswith('pdf'):
            clean_links.append(clean.group(1))
    return clean_links


def get_news_content(link):
    # Extract news content from a given link
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser', from_encoding="iso-8859-1")
    content = [p.get_text().split(".") for p in soup.find_all('p')]
    return [sentence for sublist in content for sentence in sublist]


def clean_text(text):
    # Remove special characters and empty strings from a given string
    spec_chars = ["!",'"',"#","%","&","'","(",")",
                  "*","+",".","/",":",";","<",
                  "=",">","?","@","[","\\","]","^","_",
                  "`","{","|","}","~"]
    text = re.sub(r'\s+', ' ', text)
    for char in spec_chars:
        text = text.replace(char, ' ')
    return text.strip()


def main():
    number_result = 100
    ua = UserAgent()
    google_url = "https://www.google.com/search?source=hp&ei=Ro4FX7fGBLWKmge_z6foAQ&q=slum%2C+mexico%2C+2018&oq=slum%2C+mexico%2C+2018&gs_lcp=CgZwc3ktYWIQAzoICAAQsQMQgwE6AggAOgUIABCxAzoGCAAQFhAeOgUIIRCgAToECCEQFVCLLliqYmCZZ2gBcAB4AIABowGIAawTkgEEMC4xOZgBAKABAaoBB2d3cy13aXo&sclient=psy-ab&ved=0ahUKEwi3gbOxqL3qAhU1heYKHb_nCR0Q4dUDCAc&uact=5"
    params = {'num': 100, 'start': 1}
    response = requests.get(google_url, params=params)
    soup = BeautifulSoup(response.text, "html.parser")
    result_div = soup.find_all('div', attrs={'class': 'ZINbbc'})

    links = []
    for r in result_div:
        try:
            link = r.find('a', href=True)['href']
            if link.startswith('/url?q='):
                links.append(link)
        except:
            continue

    clean_links = get_clean_links(links)
    news_content = []
    for link in clean_links:
        news_content.extend(get_news_content(link))

    # Data cleaning
    cleaned_text = [clean_text(text) for text in news_content]
    cleaned_text = [text for text in cleaned_text if text]
    cleaned_text = remove_numbers(cleaned_text)

    df = pd.DataFrame(cleaned_text, columns=['news content'])
    
    df.to_excel('Mexico.xlsx')
    
if __name__ == "__main__":
    main()
