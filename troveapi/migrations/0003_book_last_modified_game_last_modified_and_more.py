# Generated by Django 4.0.2 on 2022-02-12 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('troveapi', '0002_book_tags_game_platforms_game_tags_show_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='last_modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='game',
            name='last_modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='show',
            name='last_modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
