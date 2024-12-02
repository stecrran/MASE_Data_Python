import pandas as pd
import matplotlib.pyplot as plt

class VisualiseData:
    def __init__(self, connection):
        self.connection = connection

    def visualiseGenderDistribution(self, connection):
        # Validate connection before visualizing client data
        if self.connection is None:
            print("Error: Database connection not established.")
            return

        try:
            frame = pd.read_sql("SELECT * FROM actors", connection)
            pd.set_option('display.expand_frame_repr', False)
            gender_counts = frame['sex'].value_counts(dropna=False)
            plt.pie(gender_counts, labels=gender_counts.index, autopct='%.1f%%')
            plt.legend(gender_counts.index)
            plt.title("Actors - Gender Distribution")
            plt.show()
        except Exception as error:
            print(f"Error while visualizing client data: {error}")