# Author: ymxu
# Created: 2026/9/30 9:11
# File: 04-csv-w-r.py

with open("../csv_data/01.csv", "w", encoding="utf-8") as f:
    f.write("Name,Age,Gender,Hobbies\n")
    f.write("Alex,18,Male,'Reading,Painting'\n")
    f.write("Jamie,20,Female,Swimming\n")
    f.write("Taylor,22,Male,Basketball\n")

with open("../csv_data/01.csv", "r", encoding="utf-8") as f:
    for row in f:
        print(row.strip())