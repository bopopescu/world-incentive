# Generated by Django 2.2.2 on 2019-06-19 16:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('initiative', '0002_auto_20190619_0700'),
    ]

    operations = [
        migrations.AddField(
            model_name='initiativeversion',
            name='editor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
