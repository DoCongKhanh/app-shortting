# Generated by Django 4.0.4 on 2022-07-11 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('urlshortener', '0002_limited'),
    ]

    operations = [
        migrations.AddField(
            model_name='limited',
            name='count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='limited',
            name='Browser',
            field=models.TextField(),
        ),
    ]
