# Generated by Django 5.1.7 on 2025-03-18 10:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_wikipediapage_delete_imagecaption'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageCaption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.URLField()),
                ('final_caption', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='captions', to='core.wikipediapage')),
            ],
            options={
                'unique_together': {('page', 'image_url')},
            },
        ),
    ]
