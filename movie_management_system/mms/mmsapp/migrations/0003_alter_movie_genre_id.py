# Generated by Django 4.2 on 2023-04-30 12:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mmsapp', '0002_movie_genre_id_alter_movie_cast_actor_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='genre_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='mmsapp.genre'),
        ),
    ]
