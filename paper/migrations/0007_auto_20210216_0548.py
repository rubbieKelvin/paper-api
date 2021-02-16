# Generated by Django 3.1.6 on 2021-02-16 05:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('paper', '0006_auto_20210216_0409'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=10)),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TagMembership',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('checkbook', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='paper.checkbook')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='paper.tag')),
            ],
        ),
        migrations.AddField(
            model_name='checkbook',
            name='tags',
            field=models.ManyToManyField(through='paper.TagMembership', to='paper.Tag'),
        ),
    ]
