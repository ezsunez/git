# Generated by Django 3.1.6 on 2021-02-15 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_article_update_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='update_date',
            field=models.DateTimeField(auto_now=True, verbose_name='date published'),
        ),
    ]