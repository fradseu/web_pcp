# Generated by Django 4.0.1 on 2022-03-21 11:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Factory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Priority',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Statusos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Solicitacao',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fullname', models.CharField(max_length=30)),
                ('slug', models.SlugField(editable=False, verbose_name='Slug')),
                ('machine_code', models.CharField(max_length=50)),
                ('date_create', models.DateField(auto_now_add=True)),
                ('hour_arrive', models.TimeField(auto_now_add=True)),
                ('issue_desctiption', models.CharField(max_length=150)),
                ('factory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.factory')),
                ('priority_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.priority')),
                ('sector', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.sector')),
                ('status_os', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.statusos')),
            ],
            options={
                'ordering': ['-date_create'],
            },
        ),
        migrations.CreateModel(
            name='Ferr_report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('data_1', models.DateField()),
                ('hora_1', models.TimeField()),
                ('hora_2', models.TimeField()),
                ('body', models.TextField(max_length=255)),
                ('os_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='core.solicitacao')),
            ],
            options={
                'ordering': ['data_1'],
            },
        ),
    ]
