import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Configuration
num_people = 35
num_days = 28  # Collecting data for 4 weeks
start_date = datetime(2024, 10, 1)

# Generate sample data
data = []
for person_id in range(1, num_people + 1):
    date = start_date
    # Set unique baselines for each person to add individual variability
    baseline_sleep_hours = np.random.uniform(6, 8)  # Personal baseline sleep
    baseline_eda = np.random.uniform(0.3, 0.6)  # Personal baseline EDA
    baseline_hr = np.random.randint(60, 70)  # Baseline heart rate

    for _ in range(num_days):
        # Random daily factors
        caffeine_intake = np.random.choice([0, 50, 100, 150, 200, 250])
        alcohol_intake = np.random.choice([0, 1, 2, 3])
        activity_level = np.random.randint(1, 10)
        stress_level = np.random.randint(1, 10)

        # Introduce some randomness in how each factor affects sleep hours
        sleep_hours = baseline_sleep_hours
        if np.random.rand() < 0.5:  # 50% chance caffeine affects sleep that day
            sleep_hours -= caffeine_intake / 300 + np.random.normal(0, 0.3)
        if np.random.rand() < 0.4:  # 40% chance alcohol affects sleep that day
            sleep_hours -= alcohol_intake * 0.4 + np.random.normal(0, 0.2)
        sleep_hours += (activity_level * 0.1 + np.random.normal(0, 0.3))  # Add noise
        sleep_hours = max(4.5, min(sleep_hours, 9))  # Restrict sleep hours to realistic range

        # Simulate heart rate with a base influenced by stress and activity, adding noise
        heart_rate = baseline_hr + (stress_level * 0.3) + (activity_level * 0.2) + np.random.normal(0, 1.5)

        # EDA influenced by stress level, with additional noise
        eda = baseline_eda + (stress_level * 0.05) + np.random.normal(0, 0.05)

        # Body temperature fluctuations with some random variation
        temperature = round(np.random.uniform(36.0, 37.5) + np.random.normal(0, 0.2), 1)

        # Self-reported sleep quality influenced by sleep hours and stress, with added noise
        sleep_quality_rating = max(1, min(10, 10 - abs(7 - sleep_hours) - (stress_level * 0.1) + np.random.normal(0, 0.5)))

        entry = {
            "Timestamp": date.strftime("%Y-%m-%d 23:00"),
            "User ID": person_id,
            "Heart Rate (BPM)": round(heart_rate, 1),
            "Sleep Hours": round(sleep_hours, 1),
            "Electrodermal Activity (EDA)": round(eda, 2),
            "Temperature (°C)": temperature,
            "Activity Level": activity_level,
            "Stress Level": stress_level,
            "Sleep Quality Rating": round(sleep_quality_rating),
            "Caffeine Intake (mg)": caffeine_intake,
            "Alcohol Intake (units)": alcohol_intake
        }
        data.append(entry)
        date += timedelta(days=1)

# Convert to DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv("health_data_realistic_varied.csv", index=False)
print("Data saved to health_data_realistic_varied.csv")
