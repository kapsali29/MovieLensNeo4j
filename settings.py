# DATASET DETAILS
DATA_FOLDER = 'data'
DATASETS = {
    'credits': 'credits.csv',
    'metadata': 'movies_metadata.csv',
    'keywords': 'keywords.csv'
}

# NEO4J DETAILS
NEO4J_HOST = 'localhost'
NEO4J_PORT = 7474
NEO4J_USER = 'neo4j'
NEO4J_PASS = 'neo4j1'
NEO4J_URI = "neo4j://{host_name}:{port}".format(host_name=NEO4J_HOST, port=7687)

# APP DETAILS
API_PORT = 5000