# Generated by Django 2.2.3 on 2019-09-03 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0009_auto_20190902_1724'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='Profile_Photo',
            field=models.ImageField(upload_to=''),
        ),
    ]
