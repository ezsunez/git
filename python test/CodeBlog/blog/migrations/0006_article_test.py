# Generated by Django 3.1.6 on 2021-02-16 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_remove_article_update_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='test',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]