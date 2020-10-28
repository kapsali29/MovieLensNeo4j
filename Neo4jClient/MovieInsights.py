from Neo4jClient.client import Neo4jApp


class MovieInsights(object):
    """This class is used to retrieve Movie Insights"""

    def __init__(self):
        self.neo4j_base_client = Neo4jApp()

    def number_of_movies_per_genre(self, genre):
        """This function return the number of movies per genre"""
        num_genre_query = (
            """
            MATCH (m:Movie)-[:HAS_GENRE]->(g:Genre {{name: '{genre}'}}) RETURN m"""
        ).format(genre=genre)
        genre_data = self.neo4j_base_client.generic_executor(num_genre_query)
        return genre_data

    def similar_genre_movies(self, movie_title):
        """This function is used to fetch similar movies using same gender movies"""
        similar_genre_movies = (
            """
            MATCH (m:Movie {{title: '{movie_title}'}})-[:HAS_GENRE]->(g:Genre)<-[:HAS_GENRE]-(other_movies:Movie)
            RETURN other_movies, collect(g.name)
            """
        ).format(movie_title=movie_title)
        similar_movies_data = self.neo4j_base_client.generic_executor(similar_genre_movies)
        return similar_movies_data

    def get_actor_movies(self, actor_name):
        """This function returns actor movies"""
        actor_movies_query = (
            f"""
            MATCH (m:Movie)<-[:ACTED_IN]-(a:Actor {{name: '{actor_name}'}})
            RETURN m.title, a.character
            """
        ).format(actor_name=actor_name)
        actor_movies_data = self.neo4j_base_client.generic_executor(actor_movies_query)
        return actor_movies_data

    def get_actor_colleagues(self, actor_name):
        """This function is used to fetch actor colleagues in movies"""
        actor_colleagues_query = (
            """
            MATCH (a:Actor {{name: '{actor_name}'}})-[:ACTED_IN]->(m:Movie)<-[:ACTED_IN]-(colleagues:Actor)
            RETURN m.title as movie_title, a.character as actor_role, collect(colleagues.name) as colleagues
            """
        ).format(actor_name=actor_name)
        actor_colleagues = self.neo4j_base_client.generic_executor(actor_colleagues_query)
        return actor_colleagues

    def similarity_based_on_genre(self, movie_title):
        """This function returns movies similar to movies provided by common genres"""
        if not type(movie_title) == list:
            similar_movies_query = (
                """
                MATCH (m:Movie {{title: "{movie_title}"}})-[:HAS_GENRE]->(g:Genre)<-[:HAS_GENRE]-(m2:Movie)
                RETURN m2.title as title, count(*) as common_genre_count
                ORDER BY common_genre_count DESC LIMIT 15
                """
            ).format(movie_title=movie_title)
        else:
            similar_movies_query = (
                """
                UNWIND {movie_title} AS movie_title
                MATCH (m:Movie {{title: movie_title}})-[:HAS_GENRE]->(g:Genre)<-[:HAS_GENRE]-(m2:Movie)
                RETURN m2.title as title, count(*) as common_genre_count
                ORDER BY common_genre_count DESC LIMIT 15
                """
            ).format(movie_title=movie_title)
        similar_movies_by_genre = self.neo4j_base_client.generic_executor(similar_movies_query)
        return similar_movies_by_genre

    def jaccard_similarity(self, movie_title):
        """This function implements Jaccard Similarity"""
        jaccard_query = (
            """
            MATCH (m:Movie {{title: "{movie_title}"}})-[:HAS_GENRE]->(g:Genre)<-[:HAS_GENRE]-(other:Movie)
            WITH m, other, COUNT(g) AS intersection
            MATCH (m)-[:HAS_GENRE]->(mg:Genre)
            WITH m, other, intersection, collect(mg.name) AS sm
            MATCH (other)-[:HAS_GENRE]->(og:Genre)
            WITH m, other, intersection, sm, collect(og.name) AS so
            WITH sm+so as soyme, intersection, other, m
            WITH DISTINCT soyme, other, m, intersection
            RETURN other.title, 1.0*intersection/SIZE(soyme) as jaccard_index
            ORDER BY jaccard_index DESC LIMIT 20
            """
        ).format(movie_title=movie_title)
        jaccard_similarity = self.neo4j_base_client.generic_executor(jaccard_query)
        return jaccard_similarity
