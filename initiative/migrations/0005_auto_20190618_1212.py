# Generated by Django 2.2.2 on 2019-06-18 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('initiative', '0004_auto_20190617_1026'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='initiativelanguage',
            constraint=models.UniqueConstraint(fields=('initiative', 'language'), name='unique_initiative_language'),
        ),
    ]
