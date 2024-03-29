# Generated by Django 3.2.9 on 2022-03-22 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SRS', '0005_auto_20220322_1315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='status',
            name='code',
            field=models.CharField(choices=[('FULL PAID', 'COMPLETE'), ('PARTIAL PAID', 'PARTIAL PAID'), ('NOT PAID', 'NOT PAID')], default='NOT PAID', max_length=30, unique=True),
        ),
        migrations.AlterField(
            model_name='studentcharacter',
            name='grade',
            field=models.CharField(choices=[('B', 'B'), ('D', 'D'), ('C', 'C'), ('A', 'A'), ('F', 'F')], max_length=30),
        ),
        migrations.AlterField(
            model_name='type',
            name='code',
            field=models.CharField(choices=[('EC', 'Direct Cost'), ('OC', 'Development Cost')], default='EC', max_length=45),
        ),
        migrations.AlterUniqueTogether(
            name='studentcharacter',
            unique_together={('registration', 'character')},
        ),
    ]
