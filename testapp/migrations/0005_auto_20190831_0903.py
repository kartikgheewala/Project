# Generated by Django 2.2.3 on 2019-08-31 03:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0004_auto_20190831_0902'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatting',
            name='Created_Date',
            field=models.DateTimeField(),
        ),
    ]
