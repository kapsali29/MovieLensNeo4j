import ast
import json
import logging
import sys

import pandas as pd

from utils import check_if_data, create_output_folder

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)


class DataPreprocessor(object):
    """This Python object is used to preprocess MovieLens Dataset"""

    def __init__(self):
        self.movie_metadata = pd.read_csv('data/movies_metadata.csv').rename(columns={'id': 'movie_id'})
        self.credits = pd.read_csv('data/credits.csv').rename(columns={'id': 'movie_id'})
        self.keywords = pd.read_csv('data/keywords.csv', na_values='[]').rename(columns={'id': 'movie_id'}).dropna()

    @staticmethod
    def metadata_nested_transformer(df, main_column, secondary_column):
        """This function is used to transform nested relations"""
        transformed_df = pd.concat(
            [pd.concat([
                pd.DataFrame(df.loc[idx][main_column]),
                pd.DataFrame({secondary_column: [df.loc[idx][secondary_column]] * len(df.loc[idx][main_column])})],
                axis=1)
                for idx in df.index])
        return transformed_df

    @staticmethod
    def store_df(df, path):
        df.to_csv(path, index=False)

    def transform_genres(self):
        """This function is used to transform movie genres"""
        movies_subset = self.movie_metadata[self.movie_metadata['title'].notna()]
        genres_subset = movies_subset[['genres', 'movie_id']]
        genres_subset['genres'] = genres_subset['genres'].apply(lambda row: json.loads(row.replace("\'", "\"")))

        transformed_genres = self.metadata_nested_transformer(
            df=genres_subset,
            main_column="genres",
            secondary_column="movie_id"
        ).reset_index(drop=True)
        transformed_genres['id'] = transformed_genres['id'].map(lambda row: int(row))
        transformed_genres = transformed_genres.rename(columns={'id': 'genre_id'})
        return transformed_genres

    def handle_movies_df(self):
        """This function is used to handle movies info"""
        movies_subset = self.movie_metadata[
            ['adult', 'budget', 'movie_id', 'original_language', 'title']
        ]
        not_null_subset = movies_subset[movies_subset['title'].notna()]
        not_null_subset['original_language'] = not_null_subset['original_language'].fillna('undefined')
        return not_null_subset

    def handle_actors_df(self):
        """This function is used to handle actors DF"""
        credits_cp = self.credits.copy()
        credits_cp['cast'] = credits_cp['cast'].apply(lambda row: ast.literal_eval(row))

        actors_df = self.metadata_nested_transformer(
            df=credits_cp,
            main_column='cast',
            secondary_column='movie_id'
        )[['id', 'name', 'character', 'order', 'movie_id']]

        actors_df.loc[actors_df['character'] == '', 'character'] = 'undefined'
        transformed_actors_df = actors_df.astype({'id': int, 'order': int, 'movie_id': int})
        return transformed_actors_df

    def handle_crew_df(self):
        """This function is used to process crew movie info"""
        crew_cp = self.credits.copy()
        crew_cp['crew'] = crew_cp['crew'].apply(lambda row: ast.literal_eval(row))

        crew_df = self.metadata_nested_transformer(
            df=crew_cp,
            main_column='crew',
            secondary_column='movie_id'
        )[['id', 'job', 'name', 'movie_id']]

        crew_df['job'] = crew_df['job'].fillna('undefined')
        transformed_crew_df = crew_df.astype({'id': int, 'movie_id': int})
        return transformed_crew_df

    def handle_keywords(self):
        """This function is used to handle movies keywords"""
        self.keywords['keywords'] = self.keywords['keywords'].apply(lambda row: ast.literal_eval(row))

        kws_df = self.metadata_nested_transformer(
            df=self.keywords,
            main_column='keywords',
            secondary_column='movie_id'
        )
        return kws_df

    def process(self):
        """This function is used to save processed files"""

        data_existence = check_if_data()
        if data_existence:
            log.info("Create output folder if not exists")
            create_output_folder()

            log.info("Process Movies")
            movies = self.handle_movies_df()
            self.store_df(movies, 'output/movies.csv')
            log.info("Processed Movies stored")

            log.info("Process Movie Genres")
            transformed_genres = self.transform_genres()
            self.store_df(transformed_genres, 'output/genres.csv')

            log.info("Process Movies Cast")
            transformed_cast = self.handle_actors_df()
            self.store_df(transformed_cast, 'output/cast.csv')
            log.info('Processed cast stored')

            log.info('Process Movie Crew')
            transformed_crew = self.handle_crew_df()
            self.store_df(transformed_crew, 'output/crew.csv')
            log.info('Processed Crew stored')

            log.info('Process Movie keywords')
            transformed_kws = self.handle_keywords()
            self.store_df(transformed_kws, 'output/keywords.csv')
            log.info("Processed Movie keywords stored")
        else:
            log.error("Place your dataset inside data folder")


dp = DataPreprocessor()
dp.process()
