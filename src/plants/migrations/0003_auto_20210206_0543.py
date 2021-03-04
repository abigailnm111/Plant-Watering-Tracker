# Generated by Django 2.0.7 on 2021-02-06 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plants', '0002_auto_20210205_0722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plants',
            name='frequency',
            field=models.PositiveSmallIntegerField(),
        ),
        migrations.AlterField(
            model_name='plants',
            name='last_watered',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='plants',
            name='location',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='plants',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]