# Generated by Django 4.0.5 on 2022-06-27 13:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_profile_watchlist_profile_watchlist'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Review',
        ),
    ]
