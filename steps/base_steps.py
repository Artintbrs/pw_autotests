import os.path
import requests
import pandas as pd
import re
import pytest_check as check
from pandas import DataFrame
from playwright.sync_api import Page, expect
from bs4 import BeautifulSoup

URL: str = 'https://en.wikipedia.org/wiki/Programming_languages_used_in_most_popular_websites'

def parce_table_to_soup(page: Page):
    page.goto(URL)
    expect(page.get_by_text('Popularity')).to_be_visible()
    page_text = requests.get(URL).text
    soup = BeautifulSoup(page_text, 'lxml')
    return soup

def get_data_wiki_table(page: Page):
    if os.path.exists('result.csv'):
        wiki_data = pd.read_csv('result.csv')
    else:
        soup = parce_table_to_soup(page)
        table = soup.find('table', class_='wikitable')
        headers = []
        for i in table.find_all('th'):
            title = i.text
            headers.append(title)
        data_frame = pd.DataFrame(columns=headers)
        wiki_data = get_data_frame_table(table, data_frame)

    return wiki_data

def get_data_frame_table(table: BeautifulSoup, wiki_data: DataFrame):
    for j in table.find_all('tr')[1:]:
        row_data = j.find_all('td')
        row = [i.text for i in row_data]
        length = len(wiki_data)
        wiki_data.loc[length] = row

    if not os.path.exists('result.csv'):
        wiki_data.to_csv('result.csv', index = False)

    return wiki_data

def check_unique_visitors_for_data_table(wiki_data: DataFrame, param):
    messages: list = []
    k = 0
    while k < len(wiki_data):
        flag: bool = False
        message: str = ""
        value = wiki_data._get_value(k, 1, takeable=True).replace(',','')
        site = wiki_data._get_value(k, 0, takeable=True).replace('\n','')
        frontend = wiki_data._get_value(k, 2, takeable=True).replace('\n','')
        backend = wiki_data._get_value(k, 3, takeable=True).replace('\n','')
        number = re.findall(r'\b\d+\b', value)[0]
        k+=1
        flag = int(number) < param
        if flag:
            message = site+" (Frontend:"+frontend+"\Backend:"+backend+") has "+number+" unique visitors per month. (Expected more than "+str(param)+")"
        check.is_false(flag, message)


