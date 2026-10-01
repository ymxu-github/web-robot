# Author: ymxu
# Created: 2026/9/28 15:30
# File: 01-robot-introduction.py

import requests
from lxml import html

# Send a GET request and retrieve the response.
target_url = "https://www.tiobe.com/tiobe-index/"
response = requests.get(target_url)
document = html.fromstring(response.text)

# Extract the table headers using XPath.
th_list = document.xpath('//*[@id="top20"]/thead/tr/th/text()')
print(th_list)

# Extract the table rows using XPath.
tr_list = document.xpath('//*[@id="top20"]/tbody/tr')
for tr in tr_list:
    td_list = tr.xpath('./td/text()')
    print(td_list)