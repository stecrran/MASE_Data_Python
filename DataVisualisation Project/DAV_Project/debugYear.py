import pandas as pd


class YearVerifier:
    def __init__(self):
        """
        Initializes the YearVerifier class and retrieves the inflation data.
        """
        self.inflation_data = self.get_inflation_data()

    @staticmethod
    def get_inflation_data():
        """
        Returns the inflation data as a DataFrame.
        """
        return pd.DataFrame({
            'Year': [1913, 1914, 1915, 1916, 1917, 1918, 1919, 1920, 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928,
                     1929, 1930, 1931, 1932, 1933, 1934, 1935, 1936, 1937, 1938, 1939, 1940, 1941, 1942, 1943, 1944,
                     1945, 1946, 1947, 1948, 1949, 1950, 1951, 1952, 1953, 1954, 1955, 1956, 1957, 1958, 1959, 1960,
                     1961, 1962, 1963, 1964, 1965, 1966, 1967, 1968, 1969, 1970, 1971, 1972, 1973, 1974, 1975, 1976,
                     1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992,
                     1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008,
                     2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]
        })

    def verify_years(self, df):
        """
        Verifies if the values in the 'year' column of the provided DataFrame match the 'Year' values in the inflation data.

        :param df: DataFrame containing the 'year' column to verify.
        :return: A tuple (valid_years, invalid_years), where:
                 - valid_years is a set of years present in both the DataFrame and inflation data.
                 - invalid_years is a set of years present in the DataFrame but missing in the inflation data.
        """
        if 'year' not in df.columns:
            raise ValueError("The DataFrame does not contain a 'year' column.")

        # Extract the unique years from the DataFrame and inflation data
        df_years = set(int(year) for year in df['year'].dropna().unique())  # Convert to Python int
        inflation_years = set(int(year) for year in self.inflation_data['Year'])  # Convert to Python int

        # Find valid and invalid years
        valid_years = df_years.intersection(inflation_years)
        invalid_years = df_years.difference(inflation_years)

        return valid_years, invalid_years


# Example usage:
if __name__ == "__main__":
    # Example DataFrame with a 'year' column
    data = pd.DataFrame({
        'movieid': [1, 2, 3, 4],
        'title': ['Movie A', 'Movie B', 'Movie C', 'Movie D'],
        'year': [1920, 1945, 2025, 1990]  # Includes an invalid year (2025)
    })

    # Initialize the YearVerifier
    verifier = YearVerifier()

    # Verify years in the DataFrame
    valid_years, invalid_years = verifier.verify_years(data)

    print(f"Valid years: {valid_years}")
    print(f"Invalid years: {invalid_years}")
