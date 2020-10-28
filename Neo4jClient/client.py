from neo4j import GraphDatabase

from settings import NEO4J_URI, NEO4J_USER, NEO4J_PASS


class Neo4jApp(object):
    """This Python object is client to Neo4j"""

    def __init__(self):
        self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))

    def close(self):
        """Close Neo4j Session"""
        self.driver.close()

    @staticmethod
    def execute_query(tx, query):
        """This function is used to execute a Cypher query"""
        result_data = []
        query_result = tx.run(query)
        for record in query_result:
            if len(record.keys()) > 1:
                result_data.append(dict(record))
            else:
                result_data.append(dict(record[0]))
        return result_data

    def generic_executor(self, query):
        with self.driver.session() as session:
            data = session.read_transaction(self.execute_query, query)
        self.driver.close()
        return data
