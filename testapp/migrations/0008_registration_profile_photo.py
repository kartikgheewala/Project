# Generated by Django 2.2.3 on 2019-09-02 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0007_auto_20190831_1057'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='Profile_Photo',
            field=models.ImageField(default=2, upload_to='Profile_Photos/'),
            preserve_default=False,
        ),
    ]
