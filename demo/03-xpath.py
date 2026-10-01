# Author: ymxu
# Created: 2026/9/29 16:56
# File: 03-xpath.py
from lxml import html

with open("../resources/xian-ni-character-guide.html", "r", encoding="utf-8") as f:
    content = f.read()

    # Parse the HTML into a document that can be queried.
    document = html.fromstring(content)

    # Parse headers using XPath.
    # /table/thead/tr/th/text(): Match from the root element.
    # //table/thead/tr/th/text(): Match from any location.
    # th_list = document.xpath("/html/body/div/div/table/thead/tr/th/text()")
    # th_list = document.xpath("//table/thead/tr/th/text()")
    th_list = document.xpath("//thead/tr/th/text()")
    print(th_list)

    # tr[2]: Match the second tr element.
    td_list = document.xpath("//tbody/tr[2]/td/text()")
    print(td_list)

    # last(): Match the last element.
    td_list = document.xpath("//tbody/tr[last()-1]/td/text()")
    print(td_list)

    # p[@class]: Match p elements with a class attribute.
    p_list = document.xpath("//p[@class]/text()")
    print(p_list)

    # p[@class='xn']: Match p elements whose class is "xn".
    p_list = document.xpath("//p[@class='xn']/text()")
    print(p_list)

    # *: Match any element.
    th_list = document.xpath("//thead/tr/*/text()")
    print(th_list)

    # @src: Match the src attribute.
    # @*: Match any attribute.
    # a_list = document.xpath("//td/img/@src")
    a_list = document.xpath("//td/img/@*")
    print(a_list)