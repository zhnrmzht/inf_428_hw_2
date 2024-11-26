import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pandas as pd
from elastic.elastic_utils import connect_to_elastic, create_index, index_data

# Connect to Elasticsearch
es = connect_to_elastic()

# Define the datasets and indices
datasets = {
    "threat_scores_uniform": "data/threat_scores_uniform.csv",
    "threat_scores_high_outlier": "data/threat_scores_high_outlier.csv",
    "threat_scores_different_counts": "data/threat_scores_different_counts.csv",
    "threat_scores_high_threat_users": "data/threat_scores_high_threat_users.csv",
}

# Define common mappings
MAPPINGS = {
    "mappings": {
        "properties": {
            "department": {"type": "keyword"},
            "score": {"type": "integer"}
        }
    }
}

for index_name, file_path in datasets.items():
    # Create index
    create_index(es, index_name, MAPPINGS)
    print(f"Created index: {index_name}")

    # Read data from CSV
    df = pd.read_csv(file_path)
    data = df.to_dict(orient="records")

    # Populate Elasticsearch
    index_data(es, index_name, data)
    print(f"Populated index: {index_name}")
