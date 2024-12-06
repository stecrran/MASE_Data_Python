import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

class VisualiseData:
    def __init__(self, connection):
        self.columns = None
        self.connection = connection


    """
    Preprocess data to ensure 'Year' is an integer, remove invalid or missing values,
    and filter up to year 2000
    """
    def preprocessData(self, data):
        required_columns = {'Year', 'Percentage_Profit_Loss'}
        if not required_columns.issubset(data.columns):
            raise ValueError(f"Error: The required columns {required_columns} are not in the DataFrame.")

        # Ensure 'Year' is numeric
        data['Year'] = pd.to_numeric(data['Year'], errors='coerce')

        # Drop rows with missing or invalid Year and Percentage_Profit_Loss
        filtered_data = data.dropna(subset=['Year', 'Percentage_Profit_Loss'])

        # Convert 'Year' to integer
        filtered_data['Year'] = filtered_data['Year'].astype(int)

        # Filter by year range 1921 to 2000
        return filtered_data[(filtered_data['Year'] >= 1921) & (filtered_data['Year'] <= 2000)]


    # Visualise gender distribution for all actors. *Not used*
    def visualiseGenderDistribution(self):
        # Validate connection before visualizing client data
        if self.mydb is None:
            print("Error: Database connection not established.")
            return
        try:
            frame = pd.read_sql("SELECT * FROM actors", self.mydb)
            pd.set_option('display.expand_frame_repr', False)
            gender_counts = frame['sex'].value_counts(dropna=False)
            plt.pie(gender_counts, labels=gender_counts.index, autopct='%.1f%%')
            plt.legend(gender_counts.index)
            plt.title("Actors - Gender Distribution")
            plt.show()
        except Exception as error:
            print(f"Error while visualizing client data: {error}")


    # Plot % Profit / Loss by year
    def plotPercentProfitOrLossByYear(self, data):
        try:
            # Preprocess the data
            filtered_data = self.preprocessData(data)

            # Use a scatter-plot to represent data
            plt.figure(figsize=(10, 6))
            plt.scatter(
                filtered_data['Year'],
                filtered_data['Percentage_Profit_Loss'],
                alpha=0.7,
                c='blue',
                edgecolor='black',
                label='% Profit / Loss'
            )
            plt.xlabel('Year')
            plt.ylabel('% Profit / Loss')
            plt.title('% Profit / Loss: Years 1921 - 2000')
            plt.grid(True, linestyle='--', linewidth=0.5)
            plt.legend()
            plt.show()

        except Exception as e:
            print(f"An error occurred while plotting: {e}")


    # Plot % Profit / Loss by year. Zoom in to show values a bit more clearly
    def plotPercentProfitOrLossByYearZoom(self, data):
        try:
            filtered_data = self.preprocessData(data)

            # Filter data to include only rows with Percentage_Profit_Loss <= 5000
            zoomed_data = filtered_data[filtered_data['Percentage_Profit_Loss'] <= 5000]

            plt.figure(figsize=(10, 6))
            plt.scatter(
                zoomed_data['Year'],
                zoomed_data['Percentage_Profit_Loss'],
                alpha=0.7,
                c='blue',
                edgecolor='black',
                label='% Profit / Loss (Zoomed)'
            )
            plt.xlabel('Year')
            plt.ylabel('% Profit / Loss')
            plt.title('% Profit / Loss: Years 1921 - 2000 (Zoomed to ≤ 5000%)')
            plt.grid(True, linestyle='--', linewidth=0.5)
            plt.legend()
            plt.show()

        except Exception as e:
            print(f"An error occurred while plotting: {e}")


    # Plot % Profit / Loss by year. Zoom in to show loss values +/- 100%
    def plotPercentProfitOrLossByYearPlusMinus100pct(self, data):
        try:
            filtered_data = self.preprocessData(data)

            # Filter data to include only rows with Percentage_Profit_Loss <= 100
            zoomed_data = filtered_data[filtered_data['Percentage_Profit_Loss'] <= 100]

            plt.figure(figsize=(10, 6))
            plt.scatter(
                zoomed_data['Year'],
                zoomed_data['Percentage_Profit_Loss'],
                alpha=0.7,
                c='blue',
                edgecolor='black',
                label='% Profit / Loss (Zoomed)'
            )
            plt.xlabel('Year')
            plt.ylabel('% Loss / Profit')
            plt.title('% Profit / Loss: Years 1921 - 2000 (100% Profit or Loss)')
            plt.grid(True, linestyle='--', linewidth=0.5)
            plt.legend()
            plt.show()

        except Exception as e:
            print(f"An error occurred while plotting: {e}")


    # Generate a plot for each genre, showing x = Year and y = Adjusted_Gross_Revenue.
    def plotGenreRevenueByYear(grouped_data):
        try:
            # Check if the required columns exist
            required_columns = {'Year', 'Adjusted_Gross_Revenue', 'genres'}
            if not required_columns.issubset(grouped_data.columns):
                raise ValueError(f"Error: The required columns {required_columns} are not in the DataFrame.")

            # Drop rows with missing or invalid values
            filtered_data = grouped_data.dropna(subset=['Year', 'Adjusted_Gross_Revenue', 'genres'])

            # Convert 'Year' to integer
            filtered_data['Year'] = filtered_data['Year'].astype(int)

            # Filter by the year cutoff
            filtered_data = filtered_data[filtered_data['Year'] <= 2000]

            # Split genres into individual entries
            filtered_data['genres_split'] = filtered_data['genres'].str.split(',')
            exploded_data = filtered_data.explode('genres_split')

            # Strip whitespace from genre names
            exploded_data['genres_split'] = exploded_data['genres_split'].str.strip()

            # Get unique genres
            unique_genres = exploded_data['genres_split'].dropna().unique()

            # Generate a plot for each genre
            for genre in unique_genres:
                genre_data = exploded_data[exploded_data['genres_split'] == genre]

                # Group by Year and sum Adjusted_Gross_Revenue for each year
                genre_revenue = genre_data.groupby('Year')['Adjusted_Gross_Revenue'].sum()

                # Plot the data
                plt.figure(figsize=(10, 6))
                plt.plot(genre_revenue.index, genre_revenue.values, marker='o', label=f'{genre} Revenue')
                plt.xlabel('Year')
                plt.ylabel('Adjusted Gross Revenue')
                plt.title(f'Adjusted Gross Revenue by Year for {genre}')

                years = sorted(filtered_data['Year'].unique())
                ticks = np.arange(min(years), max(years) + 1, 3) # 3 year increment

                # Remove exponential formatting from y-axis
                ax = plt.gca()
                ax.yaxis.set_major_formatter(ScalarFormatter(useOffset=False))
                plt.ticklabel_format(style='plain', axis='y')  # Force plain formatting

                plt.xticks(ticks=ticks, rotation=45)
                plt.grid(True, linestyle='--', linewidth=0.5)
                plt.legend()
                plt.tight_layout()  # Adjust layout to avoid clipping
                plt.show()

        except Exception as e:
            print(f"An error occurred while plotting genres: {e}")




