from elasticsearch import Elasticsearch

def connect_to_elastic(url="http://localhost:9200"):
    """Connect to Elasticsearch."""
    return Elasticsearch(url)

def create_index(es, index_name, mappings):
    """Create an Elasticsearch index with specified mappings."""
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name, body=mappings)
        print(f"Index '{index_name}' created.")
    else:
        print(f"Index '{index_name}' already exists.")

def index_data(es, index_name, data):
    """Index a batch of data into Elasticsearch."""
    for record in data:
        es.index(index=index_name, body=record)
    print(f"Data indexed into '{index_name}'.")

def fetch_all_data(es, index_name):
    """Fetch all documents from an Elasticsearch index."""
    from elasticsearch.helpers import scan
    query = {"query": {"match_all": {}}}
    return list(scan(client=es, index=index_name, query=query))
