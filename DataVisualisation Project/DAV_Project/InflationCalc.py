import pandas as pd

class InflationCalculator:
    def __init__(self, data):
        """
        Initializes the InflationCalculator with inflation data.
        :param data: A DataFrame containing 'Year' and '% Change' (Dec-Dec).
        """
        self.inflation_data = data.set_index('Year')  # Set year as index for easy lookups

    def calculate_value_in_2023(self, year, amount):
        """
        Calculates the equivalent value of the input amount in 2023 based on inflation.
        :param year: The year of the original value.
        :param amount: The original amount in USD.
        :return: The inflation-adjusted value in 2023.
        """
        if year not in self.inflation_data.index:
            print(f"No inflation data available for year {year}.")
            return None

        # Filter data from the input year to 2023
        relevant_data = self.inflation_data.loc[year:2023, '% Change']

        # Convert % Change to inflation multipliers (e.g., 3% -> 1.03)
        inflation_multipliers = 1 + (relevant_data / 100)

        # Calculate cumulative inflation multiplier
        cumulative_multiplier = inflation_multipliers.prod()

        # Adjust the value
        adjusted_value = amount * cumulative_multiplier
        return adjusted_value

    def run(self):
        """
        Runs the calculator by prompting the user for input and displaying the result.
        """
        try:
            year = int(input("Enter the base year (e.g., 2000): "))
            amount = float(input("Enter the amount in USD: "))
            adjusted_value = self.calculate_value_in_2023(year, amount)
            if adjusted_value:
                print(f"\nThe equivalent value of ${amount:,.2f} in {year} is approximately ${adjusted_value:,.2f} in 2023.")
        except ValueError:
            print("Invalid input. Please enter a valid year and amount.")

# Load the data into a DataFrame
data = pd.DataFrame({
    'Year': [1913, 1914, 1915, 1916, 1917, 1918, 1919, 1920, 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1931, 1932, 1933,
             1934, 1935, 1936, 1937, 1938, 1939, 1940, 1941, 1942, 1943, 1944, 1945, 1946, 1947, 1948, 1949, 1950, 1951, 1952, 1953, 1954,
             1955, 1956, 1957, 1958, 1959, 1960, 1961, 1962, 1963, 1964, 1965, 1966, 1967, 1968, 1969, 1970, 1971, 1972, 1973, 1974, 1975,
             1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996,
             1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017,
             2018, 2019, 2020, 2021, 2022, 2023],
    '% Change': [None, 1, 2, 12.6, 18.1, 20.4, 14.5, 2.6, -10.8, -2.3, 2.4, 0, 3.5, -1.1, -2.3, -1.2, 0.6, -6.4, -9.3, -10.3, 0.8, 1.5, 3,
                 1.4, 2.9, -2.8, 0, 0.7, 9.9, 9, 3, 2.3, 2.2, 18.1, 8.8, 3, -2.1, 5.9, 6, 0.8, 0.7, -0.7, 0.4, 3, 2.9, 1.8, 1.7, 1.4, 0.7,
                 1.3, 1.6, 1, 1.9, 3.5, 3, 4.7, 6.2, 5.6, 3.3, 3.4, 8.7, 12.3, 6.9, 4.9, 6.7, 9, 13.3, 12.5, 8.9, 3.8, 3.8, 3.9, 3.8, 1.1,
                 4.4, 4.4, 4.6, 6.1, 3.1, 2.9, 2.7, 2.7, 2.5, 3.3, 1.7, 1.6, 2.7, 3.4, 1.6, 2.4, 1.9, 3.3, 3.4, 2.5, 4.1, 0.1, 2.7, 1.5,
                 3, 1.7, 1.5, 0.8, 0.7, 2.1, 2.1, 1.9, 2.3, 1.4, 7, 6.5, 3.4]
})

# Instantiate and run the calculator
if __name__ == "__main__":
    calculator = InflationCalculator(data)
    calculator.run()
