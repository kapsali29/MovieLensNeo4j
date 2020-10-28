# Movie Lens Dataset and Neo4j
+ `config/`: contains docker compose script
+ `cypher/`: contains cypher code
+ `data/`: contains movie lens dataset
+ `data_preprocessing.py`: data preprocessing python script
+ `requirements.txt`: Python libraries used
+ `utils.py`: contains utilities used in this project

### Data Setup

1. Create `data/` folder
2. Place the csv files downloaded from this link https://www.kaggle.com/rounakbanik/the-movies-dataset to **data folder**


### Data preprocessing

To execute preprocessing over movie lens dataset execute the following command:

```bash
python data_preprocessing.py
```

### API to receive results from Neo4j Queries
Run the API using this command: `python -m flask run --reload`

```http request
POST /query HTTP/1.1
Host: localhost:5000
Content-Type: application/json

{
    "query": "MATCH (m:Movie)-[:HAS_GENRE]->(g:Genre {name: 'Mystery'}) WHERE m.budget > 60000000 RETURN m"
}
```

**Get similar movies**

```http request
POST /jaccard/similarity HTTP/1.1
Host: localhost:5000
Content-Type: application/json

{
    "title": "Cloud Atlas"
}
```