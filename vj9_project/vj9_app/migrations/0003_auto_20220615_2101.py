# Generated by Django 3.1.5 on 2022-06-15 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vj9_app', '0002_auto_20220615_2035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='korisnik',
            name='role',
            field=models.CharField(choices=[('profesor', 'profesor'), ('student', 'student'), ('admin', 'admin')], max_length=100, null=True),
        ),
        migrations.DeleteModel(
            name='Uloge',
        ),
    ]