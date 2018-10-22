# Generated by Django 2.1.2 on 2018-10-22 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20181020_0827'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='action',
            options={'ordering': ('-created',), 'verbose_name': 'action', 'verbose_name_plural': 'actions'},
        ),
        migrations.AlterField(
            model_name='action',
            name='color',
            field=models.IntegerField(choices=[(1, 'orange'), (2, 'red-orange'), (3, 'radical-red'), (4, 'gray'), (5, 'green'), (6, 'blue'), (7, 'purple')], default=1, help_text='Choose a color of progress bar', verbose_name='Color'),
        ),
        migrations.AlterField(
            model_name='action',
            name='text',
            field=models.CharField(help_text='Enter an action title (e.g. Book Reading)', max_length=140, verbose_name='Text'),
        ),
        migrations.AlterField(
            model_name='action',
            name='unit',
            field=models.CharField(help_text='Enter a unit (e.g. pages)', max_length=50, verbose_name='Unit'),
        ),
    ]
