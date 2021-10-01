import os
import django
import csv

from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from movies.models import *

CSV_PATH_PRODUCTS = './backdata.csv'

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:

        movie = Movie.objects.create(
            ko_name        = row[3],
            en_name        = row[4],
            release_date   = row[5].replace('.', '-'),
            close_date     = row[6].replace('.', '-'),
            screening_type = row[7],
            running_time   = row[8],
            rating         = row[9],
            age_grade      = row[10],
            description    = row[11],
            total_audience = row[12],
        )

        genre_list = row[0].split(',')
        for genre in genre_list:
            gr = Genre.objects.get_or_create(name = genre)
            movie.genre.add(gr[0])
        
        director_list = row[1].split(',')
        for director in director_list:
            dr = Director.objects.get_or_create(name = director)
            movie.director.add(dr[0])
        
        actor_list = row[2].split(',')
        for actor in actor_list:
            at = Actor.objects.get_or_create(name = actor)
            movie.actor.add(at[0])

        url_list = row[13:17]
        for url in url_list:
            Image.objects.create(movie_id = movie.id, image_url = url)
        
    start_time_list = [0,9,12,18]
    theater_list    = ['강남','강남대로(씨티)','강동','군자','홍대','신촌','선릉','역삼']
    for theater in theater_list:
        Theater.objects.create(location = theater)

    movie_query_set   = Movie.objects.all()
    theater_query_set = Theater.objects.all()

    MovieTheater.objects.bulk_create(
        [
            MovieTheater(
                movie_id   = m_id.id,
                theater_id = t_id.id,
                start_time = datetime(2021,10,1,hour,0)
            )
        for m_id in movie_query_set for t_id in theater_query_set for hour in start_time_list]
    )