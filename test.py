from operator import itemgetter

from neo4j import GraphDatabase

uri = "neo4j://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "neo4j1"))


query = """
        MATCH (m:Movie {lang: 'el'})
        RETURN m.movie_id as movie_id, m.title as movie_title;
        """

def get_friends_of(tx, query):
    res = []
    result = tx.run(query)
    result_keys = result.keys()
    for record in result:
        res.append(itemgetter(*result_keys)(record))
    return myvalues


with driver.session() as session:
    friends = session.read_transaction(get_friends_of, query)
    print(friends)
driver.close()
