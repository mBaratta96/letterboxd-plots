import pandas as pd
import os
import requests
from lxml import html
from tmdbv3api import Movie

movie = Movie()

def get_tmdb_id(link_buttons):
    for link_button in link_buttons:
        if link_button.get('data-track-action') == 'TMDb':
            print(link_button.get('href'))
            tmbd_id = link_button.get('href').split('/')[-2]
            return tmbd_id



def movie_downloader(filename='ratings.csv'):
    """
    The movie_downloader function downloads the Letterboxd URI for each movie in the ratings.csv file and saves it to a 
    folder called movies.

    :param filename='ratings.csv': Used to specify the file that is being read.
    :return: the status code of the request.

    :doc-author: Trelent
    """
    data_path = os.path.join(os.environ.get('DATA_FOLDER'), filename)
    df = pd.read_csv(data_path)
    for link in df['Letterboxd URI']:
        r = requests.get(link)
        if r.status_code == 200:
            movie_page = html.document_fromstring(r.text)
            link_buttons = movie_page.find_class('micro-button track-event')
            tmdb_id = get_tmdb_id(link_buttons)
            m = movie.details(int(tmdb_id))
            print(m.title)
            print(m.overview)

            