# Generated by Django 3.1.4 on 2021-01-02 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ParklePlayer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('player_key', models.CharField(max_length=32, unique=True)),
                ('secret_key', models.CharField(max_length=32, unique=True)),
            ],
        ),
    ]
