# Generated by Django 4.0.5 on 2022-06-23 09:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_alter_movie_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='movie',
            options={'ordering': ('id',)},
        ),
    ]
