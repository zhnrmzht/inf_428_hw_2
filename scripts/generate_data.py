import pandas as pd
import numpy as np

def generate_random_data(mean, variance, num_samples):
    if variance == 0:
        # If variance is zero, generate an array filled with the mean value
        return np.full(num_samples, mean)
    else:
        return np.random.randint(max(mean - variance, 0), min(mean + variance + 1, 90), num_samples)

def save_to_csv(data, filename):
    rows = []
    for dept in data:
        for score in dept['scores']:
            rows.append({'department': dept['department'], 'score': score})
    df = pd.DataFrame(rows)
    df.to_csv(filename, index=False)
    print(f"Random data saved to {filename}.")

if __name__ == "__main__":
    # Uniform data
    uniform_data = [
        {'department': 'HR', 'scores': generate_random_data(30, 5, 50)},
        {'department': 'Finance', 'scores': generate_random_data(30, 5, 50)},
        {'department': 'IT', 'scores': generate_random_data(30, 5, 50)},
        {'department': 'Marketing', 'scores': generate_random_data(30, 5, 50)},
        {'department': 'Sales', 'scores': generate_random_data(30, 5, 50)},
    ]
    save_to_csv(uniform_data, "data/threat_scores_uniform.csv")

    # High outlier data
    high_outlier_data = [
        {'department': 'HR', 'scores': generate_random_data(30, 5, 50)},
        {'department': 'Finance', 'scores': generate_random_data(85, 5, 50)},  # Outlier
        {'department': 'IT', 'scores': generate_random_data(30, 5, 50)},
        {'department': 'Marketing', 'scores': generate_random_data(30, 5, 50)},
        {'department': 'Sales', 'scores': generate_random_data(30, 5, 50)},
    ]
    save_to_csv(high_outlier_data, "data/threat_scores_high_outlier.csv")

    # Different user counts
    different_counts_data = [
        {'department': 'HR', 'scores': generate_random_data(30, 5, 100)},
        {'department': 'Finance', 'scores': generate_random_data(30, 5, 50)},
        {'department': 'IT', 'scores': generate_random_data(30, 5, 25)},
        {'department': 'Marketing', 'scores': generate_random_data(30, 5, 10)},
        {'department': 'Sales', 'scores': generate_random_data(30, 5, 75)},
    ]
    save_to_csv(different_counts_data, "data/threat_scores_different_counts.csv")

    # High individual user scores for one department
    high_threat_users_data = [
    {'department': 'HR', 'scores': generate_random_data(30, 5, 50)},
    {'department': 'Finance', 'scores': generate_random_data(30, 5, 50)},
    {'department': 'IT', 'scores': generate_random_data(90, 0, 10)},  # High threat users
    {'department': 'Marketing', 'scores': generate_random_data(30, 5, 50)},
    {'department': 'Sales', 'scores': generate_random_data(30, 5, 50)},
    ]
    save_to_csv(high_threat_users_data, "data/threat_scores_high_threat_users.csv")
