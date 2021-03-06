# Generated by Django 4.0.dev20210810104906 on 2021-09-29 18:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'actors',
            },
        ),
        migrations.CreateModel(
            name='Director',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'directors',
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'genres',
            },
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ko_name', models.CharField(max_length=45)),
                ('en_name', models.CharField(max_length=100)),
                ('release_date', models.DateField()),
                ('close_date', models.DateField()),
                ('screening_type', models.CharField(max_length=45)),
                ('running_time', models.IntegerField()),
                ('age_grade', models.IntegerField()),
                ('rating', models.FloatField()),
                ('description', models.TextField()),
                ('total_audience', models.IntegerField()),
                ('actor', models.ManyToManyField(to='movies.Actor')),
                ('director', models.ManyToManyField(to='movies.Director')),
                ('genre', models.ManyToManyField(to='movies.Genre')),
            ],
            options={
                'db_table': 'movies',
            },
        ),
        migrations.CreateModel(
            name='Theater',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=32)),
            ],
            options={
                'db_table': 'theaters',
            },
        ),
        migrations.CreateModel(
            name='WishMovie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishmovies', to='movies.movie')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishmovies', to='users.user')),
            ],
            options={
                'db_table': 'wishmovies',
            },
        ),
        migrations.CreateModel(
            name='MovieTheater',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('start_time', models.DateTimeField()),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movie_theaters', to='movies.movie')),
                ('theater', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movie_theaters', to='movies.theater')),
            ],
            options={
                'db_table': 'movietheaters',
            },
        ),
        migrations.AddField(
            model_name='movie',
            name='theater',
            field=models.ManyToManyField(through='movies.MovieTheater', to='movies.Theater'),
        ),
        migrations.AddField(
            model_name='movie',
            name='user',
            field=models.ManyToManyField(through='movies.WishMovie', to='users.User'),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image_url', models.CharField(max_length=200)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='movies.movie')),
            ],
            options={
                'db_table': 'images',
            },
        ),
    ]
