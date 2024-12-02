import pandas as pd
import re

# Load the file
file_path = 'movies_bus.csv'
movies_df = pd.read_csv(file_path)

# Function to split `businesstext` into structured columns, handling missing values
def extract_business_info_safe(text):
    # Check if the input is a string; if not, return empty fields
    if not isinstance(text, str):
        return pd.Series({
            'Budget': None,
            'Gross Revenue': None,
            'Additional Data': None,
            'Copyright': None,
            'Currency': None
        })
    info = {
        'Budget': None,
        'Gross Revenue': None,
        'Additional Data': None,
        'Copyright': None,
        'Currency': None
    }
    # Extract budget (BT), gross revenue (GR), additional data (AD), and copyright (CP)
    budget_match = re.search(r'BT:\s*([A-Z]{3})\s*([\d,]+)', text)
    gross_revenue_match = re.search(r'GR:\s*([A-Z]{3})\s*([\d,]+)', text)
    additional_data_match = re.findall(r'AD:\s*([^\n]+)', text)
    copyright_match = re.search(r'CP:\s*(.+)', text)
    # Set values if matches are found
    if budget_match:
        info['Currency'] = budget_match.group(1)
        info['Budget'] = int(budget_match.group(2).replace(',', ''))
    if gross_revenue_match:
        info['Gross Revenue'] = int(gross_revenue_match.group(2).replace(',', ''))
    if additional_data_match:
        info['Additional Data'] = " | ".join(additional_data_match)
    if copyright_match:
        info['Copyright'] = copyright_match.group(1)
    return pd.Series(info)

# Apply function to `businesstext` column to create new columns
business_info_df = movies_df['businesstext'].apply(extract_business_info_safe)
# Combine the new columns with the original DataFrame (excluding the unused columns)
tidy_movies_df = pd.concat([movies_df[['movieid']], business_info_df], axis=1)
# Display the resulting DataFrame
print(tidy_movies_df)
tidy_movies_df.to_csv("tidy.csv", index=False)
