# Generated by Django 3.2 on 2021-04-23 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.TextField()),
                ('url', models.TextField()),
                ('title', models.TextField()),
                ('subj', models.CharField(max_length=20)),
                ('typ', models.CharField(max_length=20)),
                ('pub_time', models.DateTimeField(verbose_name='time_published')),
                ('mk_array', models.TextField()),
                ('author', models.CharField(max_length=20)),
                ('aprnc', models.CharField(max_length=1)),
                ('views', models.IntegerField(default=0)),
            ],
        ),
    ]