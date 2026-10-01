# Author: ymxu
# Created: 2026/9/28 16:06
# File: 02-robot-html-parsing.py
from lxml import html

with open("../resources/xian-ni-character-guide.html", "r", encoding="utf-8") as f:
    content = f.read()

    # Parse the HTML into a document that can be queried.
    document = html.fromstring(content)

    # Extract the table headers using XPath.
    th_list = document.xpath('//table/thead/tr/th/text()')
    print(th_list)

    # Extract the table rows using XPath.
    tr_list = document.xpath('//table/tbody/tr')
    for tr in tr_list:
        td_list = tr.xpath('./td/text()')
        print(td_list)
