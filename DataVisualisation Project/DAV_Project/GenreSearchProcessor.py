# Import necessary modules
import pandas as pd
import matplotlib.pyplot as plt


class GenreSearchProcessor:
    def __init__(self, data):
        self.data = data.copy()

    def generate_genre_revenue_dataframe(self):
        """
        Generate a DataFrame with total Adjusted_Gross_Revenue for each genre per year.
        """
        exploded_data = self.data.copy()
        exploded_data['genres_split'] = exploded_data['genres'].str.split(',')

        # Explode genres
        exploded_data = exploded_data.explode('genres_split')
        exploded_data['genres_split'] = exploded_data['genres_split'].str.strip()

        # Ensure numeric year
        exploded_data['Year'] = pd.to_numeric(exploded_data['Year'], errors='coerce')
        exploded_data = exploded_data.dropna(subset=['Year', 'Adjusted_Gross_Revenue'])
        exploded_data['Year'] = exploded_data['Year'].astype(int)

        # Group by year and genre
        grouped_data = (
            exploded_data.groupby(['Year', 'genres_split'])['Adjusted_Gross_Revenue']
            .sum()
            .reset_index()
            .rename(columns={'genres_split': 'Genre', 'Adjusted_Gross_Revenue': 'Total_Adjusted_Gross_Revenue'})
        )
        return grouped_data


class GenreRevenueAnalysis:
    def __init__(self, data):
        """
        Initialize the GenreRevenueAnalysis class with grouped data.
        :param data: DataFrame with columns 'Year', 'Genre', 'Total_Adjusted_Gross_Revenue'.
        """
        self.data = data

    def plot_total_revenue_by_genre(self):
        """
        Plot total adjusted gross revenue for each genre.
        """
        grouped_by_genre = self.data.groupby('Genre')['Total_Adjusted_Gross_Revenue'].sum().reset_index()

        # Sort genres by total revenue
        grouped_by_genre = grouped_by_genre.sort_values(by='Total_Adjusted_Gross_Revenue', ascending=False)

        # Plot the data
        plt.figure(figsize=(12, 6))
        plt.barh(
            grouped_by_genre['Genre'],
            grouped_by_genre['Total_Adjusted_Gross_Revenue'],
            color='skyblue'
        )
        plt.xlabel('Total Adjusted Gross Revenue ($)')
        plt.ylabel('Genre')
        plt.title('Total Adjusted Gross Revenue by Genre')
        plt.grid(axis='x', linestyle='--', linewidth=0.5)
        plt.tight_layout()
        plt.show()


# Main Method
def main():
    # Example GenreSearch data
    genre_search_data = pd.DataFrame({
        'genres': ['Action,Comedy', 'Drama', 'Action,Adventure', 'Comedy', 'Drama,Romance'],
        'Adjusted_Gross_Revenue': [500000, 1000000, 800000, 300000, 600000],
        'Year': [1995, 1996, 1997, 1998, 1999]
    })

    # Step 1: Generate grouped data from GenreSearchProcessor
    processor = GenreSearchProcessor(genre_search_data)
    grouped_data = processor.generate_genre_revenue_dataframe()

    # Step 2: Pass grouped_data into GenreRevenueAnalysis
    revenue_analysis = GenreRevenueAnalysis(grouped_data)
    revenue_analysis.plot_total_revenue_by_genre()


# Run the main method
if __name__ == "__main__":
    main()
