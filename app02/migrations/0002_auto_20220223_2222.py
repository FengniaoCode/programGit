# Generated by Django 3.2.12 on 2022-02-23 14:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app02', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrettyNum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.CharField(max_length=11, verbose_name='手机号')),
                ('price', models.IntegerField(blank=True, default=0, null=True, verbose_name='价格')),
                ('level', models.SmallIntegerField(choices=[(1, '1级'), (2, '2级'), (3, '3级'), (4, '4级')], default=1, verbose_name='级别')),
                ('status', models.SmallIntegerField(default=2, verbose_name='状态')),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='depart',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app02.department', verbose_name='所属部门'),
        ),
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.SmallIntegerField(choices=[(1, '男1'), (2, '女')], default=1, verbose_name='性别'),
        ),
    ]