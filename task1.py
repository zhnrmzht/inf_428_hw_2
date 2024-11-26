import unittest
import numpy as np

def generate_random_data(mean: int, variance: int, num_samples: int) -> np.ndarray:
    if variance == 0:
        data = np.full(num_samples, mean)
    else:
        data = np.random.randint(max(mean - variance, 0), min(mean + variance + 1, 90), num_samples)
    print(f"Generated data (mean: {mean}, variance: {variance}): {data}")
    return data


def calculate_aggregated_threat_score(data: list) -> float:
    total_score = 0
    total_users = 0

    for dept in data:
        dept_mean_score = np.mean(dept['scores'])
        if dept_mean_score > 45:
            adjusted_mean_score = dept_mean_score ** (1 + (dept_mean_score - 45) / 30)
        else:
            adjusted_mean_score = dept_mean_score
        total_score += adjusted_mean_score * len(dept['scores'])
        total_users += len(dept['scores'])
        print(f"Department mean score: {dept_mean_score}, Adjusted Mean: {adjusted_mean_score}, Users: {len(dept['scores'])}")

    aggregated_score = min(90, total_score / total_users) if total_users > 0 else 0
    print(f"Total Score: {total_score}, Total Users: {total_users}, Aggregated Score: {aggregated_score}")
    return aggregated_score


class TestScoreCalculation(unittest.TestCase):

    def test_uniform_scores(self):
        """Test: All departments have quite same threat scores."""
        data = [
            {'scores': generate_random_data(45, 5, 50)} for _ in range(5)
        ]
        result = calculate_aggregated_threat_score(data)
        print(f"Test result (Uniform Scores): {result}")
        self.assertAlmostEqual(result, 45, delta=5)

    def test_high_threat_department(self):
        """Test: One department has a high score, other low."""
        data = [
            {'scores': generate_random_data(85, 5, 50)},
            {'scores': generate_random_data(30, 5, 50)},
            {'scores': generate_random_data(30, 5, 50)},
            {'scores': generate_random_data(30, 5, 50)},
            {'scores': generate_random_data(30, 5, 50)},
        ]
        result = calculate_aggregated_threat_score(data)
        print(f"Test result (High Threat Department): {result}")
        self.assertGreater(result, 40)

    def test_high_threat_users_in_one_department(self):
        """Test: All departments have the same mean threat score, but one has very high individual user scores."""
        data = [
            {'scores': generate_random_data(30, 5, 50)},
            {'scores': generate_random_data(30, 5, 50)},
            {'scores': generate_random_data(90, 0, 10)},
            {'scores': generate_random_data(30, 5, 50)},
            {'scores': generate_random_data(30, 5, 50)},
        ]
        result = calculate_aggregated_threat_score(data)
        print(f"Test result (High Threat Users in One Department): {result}")
        self.assertGreater(result, 35)

    def test_different_user_counts(self):
        """Test: All departments have a different number of users."""
        data = [
            {'scores': generate_random_data(30, 5, 100)}, 
            {'scores': generate_random_data(30, 5, 50)},
            {'scores': generate_random_data(30, 5, 25)}, 
            {'scores': generate_random_data(30, 5, 10)}, 
            {'scores': generate_random_data(30, 5, 75)}, 
        ]
        result = calculate_aggregated_threat_score(data)
        print(f"Test result (Different User Counts): {result}")
        self.assertAlmostEqual(result, 30, delta=10)


if __name__ == '__main__':
    unittest.main()