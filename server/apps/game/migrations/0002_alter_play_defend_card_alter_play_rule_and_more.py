# Generated by Django 4.1.5 on 2023-01-19 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='play',
            name='defend_card',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='play',
            name='rule',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='play',
            name='winner',
            field=models.IntegerField(null=True),
        ),
    ]
