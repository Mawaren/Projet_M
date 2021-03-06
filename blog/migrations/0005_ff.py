# Generated by Django 4.0.4 on 2022-05-23 17:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0004_historiques_pdp_wallets_pdp'),
    ]

    operations = [
        migrations.CreateModel(
            name='ff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blockchains', models.TextField()),
                ('tokens', models.TextField()),
                ('USD_value', models.FloatField()),
                ('balance', models.FloatField()),
                ('prices', models.FloatField()),
                ('PdP', models.FloatField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
