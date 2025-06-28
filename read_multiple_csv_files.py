import os
import csv

multiple_files = "P:/postgres_query/csvs/"

for file in os.listdir(multiple_files):
    if file.endswith(".csv"):
        file_path = os.path.join(multiple_files, file)
        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    print(row)