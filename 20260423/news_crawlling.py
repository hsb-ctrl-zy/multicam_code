import time
from db import MyDB
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import requests

base_url = "https://finance.naver.com"
sub_url = "/item/main.naver?code="
code = ["005930"]
select_code = code[0]

res = requests.get(base_url + sub_url + select_code)

soup = bs(res.text, 'html.parser')

div_data = soup.find(
	'div',
    attrs = {
    	'class': 'news_section'
    }
)

li_list = div_data.find_all('li')

href_list = [li.a['href'] for li in li_list]

news_links = [base_url + href for href in href_list]

driver = webdriver.Chrome()

news_datas = []

for news in news_links:
    driver.get(news)
    time.sleep(2)
    soup2 = bs(driver.page_source, 'html.parser')

    news_title = soup2.find(
        'h2', attrs = {'id': 'title_area'}
    ).get_text()

    news_contents = soup2.find(
        'div', attrs = {'id': 'newsct_article'}
    ).get_text().replace('\n', '').replace('\t', '')

    news_datas.append(
        [news_title, news_contents]
    )

driver.quit()

db = MyDB()

create_query = f"""
    CREATE TABLE IF NOT EXISTS `CODE_{select_code}`
    (
        `title` varchar(64) PRIMARY KEY,
        `contents` text
    )
"""

db.sql_query(create_query)

insert_query = f"""
    INSERT INTO `CODE_{select_code}`
    VALUES (%s, %s)
"""

for news in news_datas:
    db.sql_query(insert_query, *news)

db.commit()