# Generated by Django 3.2.9 on 2022-03-23 17:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SRS', '0007_auto_20220323_1327'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='registerer',
        ),
        migrations.AlterField(
            model_name='status',
            name='code',
            field=models.CharField(choices=[('FULL PAID', 'COMPLETE'), ('NOT PAID', 'NOT PAID'), ('PARTIAL PAID', 'PARTIAL PAID')], default='NOT PAID', max_length=30, unique=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='school',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='SRS.school'),
        ),
        migrations.AlterField(
            model_name='studentcharacter',
            name='grade',
            field=models.CharField(choices=[('B', 'B'), ('F', 'F'), ('A', 'A'), ('C', 'C'), ('D', 'D')], max_length=30),
        ),
    ]
