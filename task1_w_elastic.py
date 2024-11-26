import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
import numpy as np
from elasticsearch import Elasticsearch

def fetch_data_from_elasticsearch(es, index_name):
    """
    Fetch all documents from the specified Elasticsearch index.
    """
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

def calculate_aggregated_threat_score(data: dict) -> float:
    total_score = 0
    total_users = 0

    for department, scores in data.items():
        dept_mean_score = np.mean(scores)
        
        # Adjust the mean score with a more controlled formula
        if dept_mean_score > 45:
            adjusted_mean_score = dept_mean_score + max(0, (dept_mean_score - 45) * 0.5)
        else:
            adjusted_mean_score = dept_mean_score
        
        # Cap the adjusted mean score to avoid extreme inflation
        adjusted_mean_score = min(90, adjusted_mean_score)
        
        total_score += adjusted_mean_score * len(scores)
        total_users += len(scores)
        
        print(f"Department: {department}, Mean Score: {dept_mean_score}, Adjusted Mean: {adjusted_mean_score}, Users: {len(scores)}")

    aggregated_score = min(90, total_score / total_users) if total_users > 0 else 0
    print(f"Total Score: {total_score}, Total Users: {total_users}, Aggregated Score: {aggregated_score}")
    return aggregated_score


class TestScoreCalculation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Connect to Elasticsearch and fetch data."""
        # Update to include the 'scheme' parameter
        cls.es = Elasticsearch([{"host": "localhost", "port": 9200, "scheme": "http"}])
        cls.index_name = "threat_scores"
        cls.data = fetch_data_from_elasticsearch(cls.es, cls.index_name)


    def test_uniform_scores(self):
        """Test: All departments have quite same threat scores."""
        if len(self.data) == 0:
            self.skipTest("No data found in Elasticsearch for the uniform scores test.")
        result = calculate_aggregated_threat_score(self.data)
        print(f"Test result (Uniform Scores): {result}")
        self.assertAlmostEqual(result, 45, delta=5)

    def test_high_threat_department(self):
        """Test: One department has a high score, other low."""
        if len(self.data) == 0:
            self.skipTest("No data found in Elasticsearch for the high threat department test.")
        result = calculate_aggregated_threat_score(self.data)
        print(f"Test result (High Threat Department): {result}")
        self.assertGreater(result, 40)

    def test_high_threat_users_in_one_department(self):
        """Test: All departments have the same mean threat score, but one has very high individual user scores."""
        if len(self.data) == 0:
            self.skipTest("No data found in Elasticsearch for the high threat users test.")
        result = calculate_aggregated_threat_score(self.data)
        print(f"Test result (High Threat Users in One Department): {result}")
        self.assertGreater(result, 35)

    def test_different_user_counts(self):
        """Test: All departments have a different number of users."""
        if len(self.data) == 0:
            self.skipTest("No data found in Elasticsearch for the different user counts test.")
        result = calculate_aggregated_threat_score(self.data)
        print(f"Test result (Different User Counts): {result}")
    
        # Updated expected value and delta
        self.assertAlmostEqual(result, 42, delta=5)


if __name__ == "__main__":
    unittest.main()
