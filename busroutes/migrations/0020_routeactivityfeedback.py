# Generated by Django 2.2.7 on 2020-04-05 20:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('busroutes', '0019_stage_metro_stations'),
    ]

    operations = [
        migrations.CreateModel(
            name='RouteActivityFeedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response_type', models.IntegerField(choices=[(0, 'YES'), (1, 'NO'), (2, "DON'T KNOW")], default=2)),
                ('count', models.IntegerField()),
                ('route', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='busroutes.Route')),
            ],
            options={
                'unique_together': {('route', 'response_type')},
            },
        ),
    ]
