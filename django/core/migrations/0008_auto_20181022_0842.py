# Generated by Django 2.1.2 on 2018-10-22 08:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20181022_0825'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='record',
            options={'ordering': ('-created',), 'verbose_name': 'record', 'verbose_name_plural': 'records'},
        ),
        migrations.AlterField(
            model_name='record',
            name='action',
            field=models.ForeignKey(help_text='Choose your action', on_delete=django.db.models.deletion.CASCADE, related_name='records', to='core.Action', verbose_name='Action'),
        ),
        migrations.AlterField(
            model_name='record',
            name='value',
            field=models.PositiveIntegerField(help_text='Enter a value of record', verbose_name='Value'),
        ),
    ]
