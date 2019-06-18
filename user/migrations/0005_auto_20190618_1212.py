# Generated by Django 2.2.2 on 2019-06-18 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_userlanguage'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='userlanguage',
            constraint=models.UniqueConstraint(fields=('user', 'language'), name='unique_user_language'),
        ),
    ]