import chardet
import pandas as pd

df_genre = pd.read_csv('merge_genre.csv', encoding="UTF-16")
df_financials = pd.read_csv('compare_Budget_to_Gross.csv')

with open("compare_Budget_to_Gross.csv", "rb") as file:
    result = chardet.detect(file.read())
    print(result)

print("Columns in df_genre:", df_genre.columns)
print("Columns in df_financials:", df_financials.columns)

import codecs

# Specify the input file and its encoding
input_file = 'merge_genre.csv'
output_file = 'merge_genre_utf8.csv'

# Specify the original encoding (e.g., 'UTF-16')
original_encoding = 'utf-16'

# Convert to UTF-8
with codecs.open(input_file, 'r', encoding=original_encoding) as file:
    content = file.read()

# Write the content to a new file in UTF-8
with codecs.open(output_file, 'w', encoding='utf-8') as file:
    file.write(content)

print(f"File converted to UTF-8 and saved as {output_file}")