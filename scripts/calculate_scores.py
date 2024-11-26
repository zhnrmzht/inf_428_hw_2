import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from elastic.elastic_utils import connect_to_elastic, fetch_all_data

def calculate_mean_scores(data):
    """Calculate mean threat scores grouped by department."""
    scores_by_department = {}
    for record in data:
        dept = record["_source"]["department"]
        score = record["_source"]["score"]
        if dept not in scores_by_department:
            scores_by_department[dept] = []
        scores_by_department[dept].append(score)

    for dept, scores in scores_by_department.items():
        mean_score = sum(scores) / len(scores)
        print(f"Department: {dept}, Mean Threat Score: {mean_score:.2f}")

if __name__ == "__main__":
    # Connect to Elasticsearch
    es = connect_to_elastic()

    # Fetch data
    INDEX_NAME = "threat_scores"
    data = fetch_all_data(es, INDEX_NAME)

    # Calculate scores
    calculate_mean_scores(data)
