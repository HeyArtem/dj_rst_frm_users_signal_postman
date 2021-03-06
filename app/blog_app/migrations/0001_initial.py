# Generated by Django 4.0.4 on 2022-05-26 11:19

import blog_app.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, verbose_name='Blog Post Category')),
            ],
            options={
                'verbose_name': 'Blog Post Category',
                'verbose_name_plural': 'Blog Post Categories',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Tag')),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
            },
        ),
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, verbose_name='Title')),
                ('img', models.ImageField(upload_to=blog_app.models.blog_img_directory_img_path)),
                ('content', models.TextField(verbose_name='Post content')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date of create')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Date of Updated')),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], default='draft', max_length=50)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posts_by_category', to='blog_app.category', verbose_name='Category')),
                ('tag', models.ManyToManyField(blank=True, to='blog_app.tag', verbose_name='Tag')),
            ],
            options={
                'verbose_name': 'Blog Post',
                'verbose_name_plural': 'Blog Post`s',
            },
        ),
    ]
