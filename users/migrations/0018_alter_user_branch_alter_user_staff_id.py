# Generated by Django 4.1.2 on 2022-10-10 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_userprivilege_is_delete_requested'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='branch',
            field=models.PositiveBigIntegerField(blank=True, choices=[(2, 'Ebankese Branch'), (3, 'Accra Central Branch'), (4, 'Republic Court Branch'), (5, 'Kumasi Branch'), (6, 'Tema Branch'), (7, 'Legon Branch'), (8, 'Abossey Okai Branch'), (9, 'Tudu Branch'), (10, 'Techiman Branch'), (11, 'KNUST Brach'), (12, 'Tamale Branch'), (13, 'Koforidua Branch'), (14, 'Baatsona Branch'), (15, 'Private Panking'), (16, 'Ashaiman Branch'), (17, 'Takoradi Branch'), (18, 'Kasoa Branch'), (19, 'Post Office Square Branch'), (20, 'Adabraka Branch'), (21, 'Agona Swedru Branch'), (22, 'Cape Coast Branch'), (23, 'Winneba Branch'), (24, 'Asamankese Branch'), (25, 'Dansoman Branch'), (26, 'Accra Newtown Branch'), (27, 'Sefwi Wiawso'), (28, 'Essam Branch'), (29, 'Asankragua Branch'), (30, 'Sefwi Bekwai Branch '), (31, 'Akontombra Branch'), (32, 'Juaboso'), (33, 'Asempaneye Branch'), (34, 'Madina Branch'), (35, 'Goaso Branch'), (36, 'Achimota Branch'), (37, 'Asokwa Branch'), (38, 'Tema Community 25 Branch'), (39, 'Bolgatanga Branch'), (40, 'Adjiringanor Branch')], null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='staff_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
