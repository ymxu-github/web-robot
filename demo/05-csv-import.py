# Author: ymxu
# Created: 2026/9/30 9:14
# File: 05-csv-import.py
import csv

with open("../csv_data/02.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["Name", "Age", "Gender", "Hobbies"])
    writer.writeheader()
    writer.writerow({"Name": "Alex", "Age": 18, "Gender": "Female", "Hobbies": "Dancing,Singing"})
    writer.writerow({"Name": "Jamie", "Age": 20, "Gender": "Male", "Hobbies": "Swimming,Fitness"})
    writer.writerow({"Name": "Taylor", "Age": 22, "Gender": "Female", "Hobbies": "Java"})

with open("../csv_data/02.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row)