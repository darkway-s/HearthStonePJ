# Generated by Django 3.2.3 on 2021-06-03 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='img',
            field=models.ImageField(default='default.jpg', null=True, upload_to='card_img'),
        ),
    ]
