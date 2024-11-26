import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
import numpy as np
from elasticsearch import Elasticsearch
from elastic.elastic_utils import connect_to_elastic

def fetch_data_from_elasticsearch(es, index_name):
    query = {"query": {"match_all": {}}}
    response = es.search(index=index_name, body=query, size=10000)  # Fetch up to 10,000 documents
    data = response['hits']['hits']
    
    # Transform data into a structured format
    structured_data = {}
    for doc in data:
        department = doc['_source']['department']
        score = doc['_source']['score']
        if department not in structured_data:
            structured_data[department] = []
        structured_data[department].append(score)
    
    return structured_data

def calculate_aggregated_threat_score(data: list) -> float:
    total_score = 0
    total_users = 0

    for department, scores in data.items():
        dept_mean_score = np.mean(scores)
        if dept_mean_score > 45:
            adjusted_mean_score = dept_mean_score ** (1 + (dept_mean_score - 45) / 30)
        else:
            adjusted_mean_score = dept_mean_score
        total_score += adjusted_mean_score * len(scores)
        total_users += len(scores)
        print(f"Department mean score: {dept_mean_score}, Adjusted Mean: {adjusted_mean_score}, Users: {len(scores)}")

    aggregated_score = min(90, total_score / total_users) if total_users > 0 else 0
    print(f"Total Score: {total_score}, Total Users: {total_users}, Aggregated Score: {aggregated_score}")
    return aggregated_score


class TestScoreCalculation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.es = connect_to_elastic()

    def fetch_test_data(self, index_name):
        query = {"query": {"match_all": {}}}
        response = self.es.search(index=index_name, body=query, size=10000)
        data = response['hits']['hits']
        structured_data = {}
        for doc in data:
            department = doc['_source']['department']
            score = doc['_source']['score']
            if department not in structured_data:
                structured_data[department] = []
            structured_data[department].append(score)
        return structured_data

    def test_high_threat_users_in_one_department(self):
        """Test: All departments have the same mean threat score, but one has very high individual user scores."""
        data = self.fetch_test_data("threat_scores_high_threat_users")
        result = calculate_aggregated_threat_score(data)
        print(f"Test result (High Threat Users in One Department): {result}")
        self.assertGreater(result, 35, "The aggregated score should be greater than 35 for high individual user scores.")


    def test_uniform_scores(self):
        """Test: All departments have quite same threat scores."""
        data = self.fetch_test_data("threat_scores_uniform")
        result = calculate_aggregated_threat_score(data)
        print(f"Test result (Uniform Scores): {result}")
        self.assertAlmostEqual(result, 30, delta=5)

    def test_high_outlier_department(self):
        """Test: One department has a high score, other low."""
        data = self.fetch_test_data("threat_scores_high_outlier")
        result = calculate_aggregated_threat_score(data)
        print(f"Test result (High Outlier Department): {result}")
        self.assertGreater(result, 40)

    def test_different_user_counts(self):
        """Test: All departments have a different number of users."""
        data = self.fetch_test_data("threat_scores_different_counts")
        result = calculate_aggregated_threat_score(data)
        print(f"Test result (Different User Counts): {result}")
        self.assertAlmostEqual(result, 30, delta=10)


if __name__ == "__main__":
    unittest.main()
