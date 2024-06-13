# Generated by Django 5.0.6 on 2024-06-13 09:01

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Boardgame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('price', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='Price')),
                ('description', models.TextField(verbose_name='Description')),
                ('min_players_age', models.IntegerField(validators=[django.core.validators.MinValueValidator(2)], verbose_name='Min. Players Age')),
                ('min_players', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Min. Players Number')),
                ('max_players', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Max. Players Number')),
                ('min_game_time', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Min. Game Time')),
                ('max_game_time', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Max. Game Time')),
                ('categories', models.ManyToManyField(to='shop.category', verbose_name='Categories')),
                ('publisher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.publisher', verbose_name='Publisher')),
            ],
            options={
                'ordering': ['name', 'price'],
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(choices=[(1, '1 star'), (2, '2 star'), (3, '3 star'), (4, '4 star'), (5, '5 star')], default=0)),
                ('comment', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('boardgame', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.boardgame')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
                'unique_together': {('user', 'boardgame')},
            },
        ),
    ]