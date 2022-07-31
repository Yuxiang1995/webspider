from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re
import json
import xmltodict
import requests
from utils import strB2Q
import csv


def driver_open(key_word):
    url = "https://www.cnki.net"
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(2)

    # 输入关键词
    search = driver.find_element(webdriver.common.by.By.ID, 'txt_SearchText')
    search.send_keys(key_word)
    time.sleep(2)

    # 点击搜索按钮
    driver.find_element(webdriver.common.by.By.CLASS_NAME, 'search-btn').click()
    time.sleep(5)
    # driver.close()

    # 拿到返回结果
    content = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(content, 'html.parser')
    # print(type(soup))
    driver.close()

    return soup


def matchAuthor(string):
    author_list = []
    tmp_list = re.findall("'au','.*'", string)
    # print(tmp_list)
    for i in range(len(tmp_list)):
        tmp_list[i] = tmp_list[i].replace("'au','", "")
        tmp_list[i] = tmp_list[i].replace("'", "")
        # print(tmp_list[i])
        author_list.append(tmp_list[i].split(',')[0])
    return author_list

def matchInstitution(list):
    institution_list = []
    for item in list:
        item = str(item)
        tmp = re.findall("'in','.*'", item)
        if tmp:
            tmp[0] = tmp[0].replace("'in','", "")
            tmp[0] = tmp[0].replace("'", "")
            institution_list.append(tmp[0].split(',')[0])
    return institution_list


if __name__ == '__main__':
    with open("./label.json", encoding='utf-8') as f:
        mapping = json.load(f)

    csvFile = open("./label_0729.csv", 'w', newline='', encoding='utf-8')
    writer = csv.writer(csvFile)
    csvRow = ['md5', 'title', 'authors', 'institution', 'abstract']
    writer.writerow(csvRow)
    rows = []

    for key in mapping:
        row = []

        soup = driver_open(mapping[key])
        # tbody = soup.find_all('tbody')
        msgs = soup.find_all('tr')[7:27]
        # dic = xmltodict.parse(msgs[0])
        # print(dic)
        for msg in msgs:
            paper = str(msg)
            tmp = re.search('value=".*"/>', paper).group()
            tmp = tmp.replace('value="', '')
            tmp = tmp.replace('"/>', '')
            dbname, filename, a, b = tmp.split('!')
            detail_url = "https://kns.cnki.net/kcms/detail/detail.aspx?dbname={}&filename={}".format(dbname, filename)
            print(detail_url)
            r = requests.get(detail_url)
            # print(r.text)
            soup = BeautifulSoup(r.text, 'html.parser')

            title = soup.find_all('h1')[0].text
            if strB2Q(mapping[key]) != strB2Q(title):
                continue
            print(title)

            author = matchAuthor(str(soup.find_all('h3', {'class': 'author', 'id': 'authorpart'})[0]))
            print(author)

            institution = matchInstitution(soup.find_all('a', {'class': 'author', 'target': '_blank'}))
            print(institution)

            abstract = soup.find_all('span', {'id': 'ChDivSummary', 'class': 'abstract-text'})[0].text
            print(abstract)

            row = [key, title, author, institution, abstract]

        rows.append(row)

    writer.writerows(rows)
    csvFile.close()