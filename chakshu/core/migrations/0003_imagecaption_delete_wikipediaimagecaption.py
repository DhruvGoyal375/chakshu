# Generated by Django 5.1.7 on 2025-03-18 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_wikipediaimagecaption_delete_wikipediacaption'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageCaption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_url', models.URLField()),
                ('image_url', models.URLField()),
                ('caption', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.DeleteModel(
            name='WikipediaImageCaption',
        ),
    ]
