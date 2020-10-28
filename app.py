import logging
import os
import sys

from flask import Flask, request

from Neo4jClient.MovieInsights import MovieInsights
from settings import API_PORT

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)

app = Flask(__name__)
movie_insignts = MovieInsights()
neo4j_base_client = movie_insignts.neo4j_base_client


@app.route("/query", methods=['POST'])
def query_neo4j():
    """query neo4j interface"""
    data = request.get_json()
    neo4j_query = data['query']

    results = neo4j_base_client.generic_executor(neo4j_query)
    jsonified_results = {'neo4j_results': results}
    return jsonified_results, 201


@app.route("/genre/movies", methods=['POST'])
def get_genre_data():
    """Returns the provided genre movies"""
    data = request.get_json()
    genre = data['genre']
    genre_movies = movie_insignts.number_of_movies_per_genre(genre)
    results = {'{}_movies'.format(genre): genre_movies}
    return results, 201


@app.route("/similar/movies", methods=['POST'])
def similar_movies():
    """Returns the provided genre movies"""
    data = request.get_json()
    movie_title = data['title']
    similar_movies_result = movie_insignts.similar_genre_movies(movie_title)
    results = {'{}_similar_movies'.format(movie_title): similar_movies_result}
    return results, 201


@app.route("/actor/colleagues", methods=['POST'])
def fetch_actor_colleagues():
    """Returns the provided genre movies"""
    data = request.get_json()
    actor_name = data['actor']
    actor_colleagues = movie_insignts.get_actor_colleagues(actor_name)
    results = {'{}_colleagues'.format(actor_name): actor_colleagues}
    return results, 201


@app.route("/similar/movies/by/genre", methods=['POST'])
def fetch_similar_movies_by_genre():
    """Returns similar by genre movies"""
    data = request.get_json()
    movie_title = data['title']
    similar_movies_by_genre = movie_insignts.similarity_based_on_genre(movie_title)
    print(similar_movies_by_genre[0])
    results = {'{}_similar_movies'.format(movie_title): similar_movies_by_genre}
    return results, 201


if __name__ == '__main__':
    log.info("Starting Neo4j Query Execution")
    app.secret_key = os.urandom(24)
    app.run(host='0.0.0.0', port=API_PORT, debug=True)
