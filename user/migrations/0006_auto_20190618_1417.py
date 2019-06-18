# Generated by Django 2.2.2 on 2019-06-18 14:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20190618_1212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userlanguage',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='languages', to=settings.AUTH_USER_MODEL),
        ),
    ]