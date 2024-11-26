import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pandas as pd
from elastic.elastic_utils import connect_to_elastic, create_index, index_data

# Elasticsearch index name and mappings
INDEX_NAME = "threat_scores"
MAPPINGS = {
    "mappings": {
        "properties": {
            "department": {"type": "keyword"},
            "score": {"type": "integer"}
        }
    }
}

if __name__ == "__main__":
    # Connect to Elasticsearch
    es = connect_to_elastic()

    # Create index
    create_index(es, INDEX_NAME, MAPPINGS)

    # Read data from CSV
    df = pd.read_csv("C:\\Users\\ZHanar\\Data Ethics\\inf_428_hw_2\\data\\threat_scores.csv")
    data = df.to_dict(orient="records")

    # Populate Elasticsearch
    index_data(es, INDEX_NAME, data)
