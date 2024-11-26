import pandas as pd
import numpy as np

def generate_random_data(mean, variance, num_samples):
    return np.random.randint(max(mean - variance, 0), min(mean + variance + 1, 90), num_samples)

if __name__ == "__main__":
    # Generate random data
    departments = [
        {'department': 'HR', 'scores': generate_random_data(30, 5, 50)},
        {'department': 'Finance', 'scores': generate_random_data(85, 5, 50)},
        {'department': 'IT', 'scores': generate_random_data(30, 5, 50)},
        {'department': 'Marketing', 'scores': generate_random_data(30, 5, 50)},
        {'department': 'Sales', 'scores': generate_random_data(30, 5, 50)},
    ]

    # Save to CSV
    rows = []
    for dept in departments:
        for score in dept['scores']:
            rows.append({'department': dept['department'], 'score': score})

    df = pd.DataFrame(rows)
    df.to_csv("C:\\Users\\ZHanar\\Data Ethics\\inf_428_hw_2\\data\\threat_scores.csv", index=False)
    print("Random data saved to '../data/threat_scores.csv'.")
