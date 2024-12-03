import pandas as pd
from tabulate import tabulate
import re

# Initializes the FetchData class with an existing database connection.
class FetchData:
    def __init__(self, connection):
        self.connection = connection
        self.inflation_data = self.get_inflation_data()  # Initialize inflation data

    # Returns inflation data as a DataFrame.
    @staticmethod
    def get_inflation_data():
        return pd.DataFrame({
            'Year': [1913, 1914, 1915, 1916, 1917, 1918, 1919, 1920, 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928,
                     1929, 1930, 1931, 1932, 1933, 1934, 1935, 1936, 1937, 1938, 1939, 1940, 1941, 1942, 1943, 1944,
                     1945, 1946, 1947, 1948, 1949, 1950, 1951, 1952, 1953, 1954, 1955, 1956, 1957, 1958, 1959, 1960,
                     1961, 1962, 1963, 1964, 1965, 1966, 1967, 1968, 1969, 1970, 1971, 1972, 1973, 1974, 1975, 1976,
                     1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992,
                     1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008,
                     2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023],
            '% Change': [0, 1, 2, 12.6, 18.1, 20.4, 14.5, 2.6, -10.8, -2.3, 2.4, 0, 3.5, -1.1, -2.3, -1.2, 0.6,
                         -6.4, -9.3, -10.3, 0.8, 1.5, 3, 1.4, 2.9, -2.8, 0, 0.7, 9.9, 9, 3, 2.3, 2.2, 18.1, 8.8, 3,
                         -2.1, 5.9, 6, 0.8, 0.7, -0.7, 0.4, 3, 2.9, 1.8, 1.7, 1.4, 0.7, 1.3, 1.6, 1, 1.9, 3.5, 3,
                         4.7, 6.2, 5.6, 3.3, 3.4, 8.7, 12.3, 6.9, 4.9, 6.7, 9, 13.3, 12.5, 8.9, 3.8, 3.8, 3.9, 3.8,
                         1.1, 4.4, 4.4, 4.6, 6.1, 3.1, 2.9, 2.7, 2.7, 2.5, 3.3, 1.7, 1.6, 2.7, 3.4, 1.6, 2.4, 1.9,
                         3.3, 3.4, 2.5, 4.1, 0.1, 2.7, 1.5, 3, 1.7, 1.5, 0.8, 0.7, 2.1, 2.1, 1.9, 2.3, 1.4, 7, 6.5,
                         3.4]
        }).set_index('Year')

    # Adjusts values in accordance with inflation
    def calculate_adjusted_value(self, year, value):
        if pd.isna(value):
            return None
        try:
            year = int(year)
            self.inflation_data.index = self.inflation_data.index.astype(int)
        except ValueError:
            return value
        if year not in self.inflation_data.index:
            return value
        relevant_data = self.inflation_data.loc[year:2023, '% Change'].dropna()
        inflation_multipliers = 1 + (relevant_data / 100)
        cumulative_multiplier = inflation_multipliers.prod()
        return value * cumulative_multiplier

    # Fetches and processes movie data, calculates adjusted values and % Profit / Loss.
    def fetch_and_process_movie_data(self):
        if self.connection is None:
            print("Error: Database connection not established.")
            return None

        try:
            # Fetch raw data
            with self.connection.connect() as conn:
                movies = pd.read_sql("SELECT movieid, title, year FROM movies", conn)
                genres = pd.read_sql("SELECT movieid, genre FROM genres", conn)
                business = pd.read_sql("SELECT movieid, businesstext FROM business", conn)

            # Merge dataframes to simulate INNER JOIN on movieid
            merged = movies.merge(genres, on="movieid").merge(business, on="movieid")

            # Filter rows where businesstext contains 'GR'
            filtered = merged[merged["businesstext"].str.contains("GR", na=False)].copy()

            # Extract business information
            def extract_detailed_business_info(text):
                info = {
                    "Currency": None,
                    "Budget": None,
                    "Gross Revenue": None,
                    "Additional Data": None
                }
                budget_match = re.search(r'BT:\s*([A-Z]{3})\s*([\d,]+)', text)
                gross_revenue_match = re.search(r'GR:\s*([A-Z]{3})\s*([\d,]+)', text)
                additional_data_match = re.findall(r'AD:\s*([^\n]+)', text)

                if budget_match:
                    info['Currency'] = budget_match.group(1)
                    info['Budget'] = int(budget_match.group(2).replace(',', ''))
                if gross_revenue_match:
                    info['Gross Revenue'] = int(gross_revenue_match.group(2).replace(',', ''))
                if additional_data_match:
                    info['Additional Data'] = " | ".join(additional_data_match)

                return pd.Series(info)

            detailed_info = filtered["businesstext"].apply(extract_detailed_business_info)
            filtered = pd.concat([filtered, detailed_info], axis=1)

            # Filter rows with "USD" in Currency or Additional Data
            filtered = filtered[
                (filtered["Currency"] == "USD") |
                (filtered["Additional Data"].str.contains("USD", na=False))
                ]

            # adjust budget
            def adjust_budget(row):
                return self.calculate_adjusted_value(row['year'], row['Budget'])

            # adjust gross revenue
            def adjust_gross_revenue(row):
                return self.calculate_adjusted_value(row['year'], row['Gross Revenue'])

            # calculate % Profit / Loss
            def calculate_percentage_profit_loss(row):

                try:
                    if (
                            pd.notna(row['Adjusted_Gross_Revenue'])
                            and pd.notna(row['Adjusted_Budget'])
                            and row['Adjusted_Budget'] != 0
                    ):
                        return ((row['Adjusted_Gross_Revenue'] - row['Adjusted_Budget']) / row['Adjusted_Budget']) * 100
                    return None
                except Exception as e:
                    print(f"Error calculating % Profit / Loss for row: {e}")
                    return None

            # Apply adjustments and calculations
            filtered['Adjusted_Budget'] = filtered.apply(adjust_budget, axis=1)
            filtered['Adjusted_Gross_Revenue'] = filtered.apply(adjust_gross_revenue, axis=1)
            filtered['Percentage_Profit_Loss'] = filtered.apply(calculate_percentage_profit_loss, axis=1)

            # Concatenate genres for grouped data
            def concatenate_genres(genre_series):
                return ", ".join(genre_series)

            # Group data by movieid, title, and year
            grouped = filtered.groupby(["movieid", "title", "year"]).agg(
                genres=("genre", concatenate_genres),
                Currency=("Currency", "first"),
                Budget=("Budget", "first"),
                Adjusted_Budget=("Adjusted_Budget", "first"),
                Gross_Revenue=("Gross Revenue", "first"),
                Adjusted_Gross_Revenue=("Adjusted_Gross_Revenue", "first"),
                Percentage_Profit_Loss=("Percentage_Profit_Loss", "first"),
                Additional_Data=("Additional Data", "first")
            ).reset_index()

            # Rename 'year' to 'Year' for consistency
            grouped.rename(columns={"year": "Year"}, inplace=True)

            # Save to CSV. Try block used to prevent interference with return of dataframe if file is open
            try:
                print("Attempting to write to file.")
                output_file = "processed_movie_data.csv"
                grouped.to_csv(output_file, index=False)
            except Exception as e:
                print(f"An error occurred while saving the file: {e}")

            return grouped

        except Exception as e:
            print(f"An error occurred: {e}")
            return None


