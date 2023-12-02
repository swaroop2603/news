# Generated by Django 4.2.4 on 2023-12-02 07:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('newsapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='News_paper',
            fields=[
                ('paper_id', models.AutoField(primary_key=True, serialize=False)),
                ('categary', models.CharField(max_length=255)),
                ('source', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('news_description', models.TextField()),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newsapp.user')),
            ],
        ),
        migrations.DeleteModel(
            name='Offer',
        ),
    ]