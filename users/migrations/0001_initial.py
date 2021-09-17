# Generated by Django 3.2.4 on 2021-09-16 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('password', models.CharField(max_length=256)),
                ('email', models.CharField(max_length=64, unique=True)),
                ('birth_day', models.DateField()),
                ('name', models.CharField(max_length=32)),
                ('phone_number', models.CharField(max_length=16)),
                ('kakao_id', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'users',
            },
        ),
    ]