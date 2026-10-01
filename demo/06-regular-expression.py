# Author: ymxu
# Created: 2026/10/1 14:47
# File: 06-regular-expression.py
import re

s1 = "18809090000 is my phone number. Do you remember it? My other number is 18800008888. My two QQ numbers are 155998992 and 18809091293821."
s2 = "My phone number is 18809090000. Do you remember it? My other number is 18800008888. My two QQ numbers are 155998992 and 18809091293821."

# match() matches from the start of the string. If the beginning does not match the
# regular expression, the match fails and None is returned.
result = re.match(r"1[3-9]\d{9}", s1)
print(result.group() if result else "No phone number found")  # Matched phone number
print(result.span() if result else "No phone number found")  # Start and end positions of the match
print(result.start() if result else "No phone number found")  # Start position of the match
print(result.end() if result else "No phone number found")  # End position of the match

# search() scans the entire string and returns the first successful match.
result2 = re.search(r"1[3-9]\d{9}", s2)
print(result2.group() if result2 else "No phone number found")  # Matched phone number
print(result2.span() if result2 else "No phone number found")  # Start and end positions of the match
print(result2.start() if result2 else "No phone number found")  # Start position of the match
print(result2.end() if result2 else "No phone number found")  # End position of the match

# findall() returns all matches in the string as a list.
result3 = re.findall(r"1[3-9]\d{9}", s2)
print(result3)  # All matched phone numbers