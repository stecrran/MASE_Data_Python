import pandas as pd
import matplotlib.pyplot as plt


class GenreRevenueAnalysis:
    def __init__(self, genre_search_data):
        """
        Initialize the GenreRevenueAnalysis class with data from GenreSearch.
        :param genre_search_data: Preprocessed DataFrame from GenreSearch containing genres and Adjusted_Gross_Revenue.
        """
        self.data = genre_search_data.copy()

    def preprocess_data(self):
        """
        Preprocess data to ensure it's ready for analysis.
        """
        # Ensure required columns exist
        required_columns = {'genres', 'Adjusted_Gross_Revenue'}
        if not required_columns.issubset(self.data.columns):
            raise ValueError(f"Error: The required columns {required_columns} are not in the DataFrame.")

        # Ensure Adjusted_Gross_Revenue is numeric
        self.data['Adjusted_Gross_Revenue'] = pd.to_numeric(self.data['Adjusted_Gross_Revenue'], errors='coerce')

        # Drop rows with missing or invalid Adjusted_Gross_Revenue
        self.data = self.data.dropna(subset=['Adjusted_Gross_Revenue'])

        # Split genres into individual rows
        self.data['genres_split'] = self.data['genres'].str.split(',')
        self.data = self.data.explode('genres_split').reset_index(drop=True)

        # Strip whitespace from genre names
        self.data['genres_split'] = self.data['genres_split'].str.strip()

    def calculate_total_revenue_per_genre(self):
        """
        Calculate the total adjusted revenue for each genre.
        :return: DataFrame with total revenue per genre.
        """
        self.preprocess_data()

        # Group by genre and calculate the total adjusted revenue
        total_revenue = self.data.groupby('genres_split')['Adjusted_Gross_Revenue'].sum().reset_index()
        total_revenue = total_revenue.rename(columns={
            'genres_split': 'Genre',
            'Adjusted_Gross_Revenue': 'Total Adjusted Revenue'
        })

        # Sort by total revenue in descending order
        total_revenue = total_revenue.sort_values(by='Total Adjusted Revenue', ascending=False).reset_index(drop=True)
        return total_revenue

    def plot_total_revenue_per_genre(self):
        """
        Generate a bar plot for total adjusted revenue per genre.
        """
        # Calculate total revenue per genre
        total_revenue = self.calculate_total_revenue_per_genre()

        # Plot the data
        plt.figure(figsize=(12, 8))
        plt.bar(total_revenue['Genre'], total_revenue['Total Adjusted Revenue'], color='skyblue')
        plt.xlabel('Genre')
        plt.ylabel('Total Adjusted Revenue ($)')
        plt.title('Total Adjusted Revenue per Genre')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.grid(axis='y', linestyle='--', linewidth=0.5)
        plt.show()


# Example Usage with GenreSearch Data
if __name__ == "__main__":
    # Assuming `genre_search_data` is the DataFrame prepared by the GenreSearch class
    # Replace this with actual data from GenreSearch
    genre_search_data = pd.DataFrame({
        'genres': ['Action,Comedy', 'Drama', 'Action,Adventure', 'Comedy', 'Drama,Romance'],
        'Adjusted_Gross_Revenue': [500000, 1000000, 800000, 300000, 600000],
        'Year': [1995, 1996, 1997, 1998, 1999]
    })

    # Create an instance of GenreRevenueAnalysis
    analysis = GenreRevenueAnalysis(genre_search_data)

    # Calculate and display total revenue per genre
    total_revenue_df = analysis.calculate_total_revenue_per_genre()
    print(total_revenue_df)

    # Plot total revenue per genre
    analysis.plot_total_revenue_per_genre()
