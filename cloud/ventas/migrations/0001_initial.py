# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-09-13 16:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Arqueos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('caja_dia', models.DecimalField(decimal_places=2, max_digits=20)),
                ('efectivo', models.DecimalField(decimal_places=2, max_digits=20)),
                ('cambio', models.DecimalField(decimal_places=2, max_digits=20)),
                ('total_gastos', models.DecimalField(decimal_places=2, max_digits=20)),
                ('targeta', models.DecimalField(decimal_places=2, max_digits=20)),
                ('descuadre', models.DecimalField(decimal_places=2, max_digits=20)),
                ('modify', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Clientes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=100, null=True)),
                ('email', models.EmailField(blank=True, max_length=100, null=True)),
                ('telefono', models.CharField(max_length=20)),
                ('nota', models.TextField(null=True)),
                ('fecha_add', models.DateField(auto_now_add=True)),
                ('modify', models.DateTimeField(auto_now=True)),
                ('direccion', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Conteo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('can', models.IntegerField()),
                ('tipo', models.DecimalField(decimal_places=2, max_digits=20)),
                ('total', models.DecimalField(decimal_places=2, max_digits=20)),
                ('texto_tipo', models.EmailField(blank=True, max_length=100, null=True)),
                ('modify', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Direcciones',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('direccion', models.CharField(max_length=150)),
                ('localidad', models.CharField(default='Grandada', max_length=50, null=True)),
                ('codigo', models.CharField(max_length=10, null=True)),
                ('modify', models.DateTimeField(auto_now=True)),
                ('clientes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventas.Clientes')),
            ],
        ),
        migrations.CreateModel(
            name='Gastos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('des', models.CharField(max_length=100)),
                ('gasto', models.DecimalField(decimal_places=2, max_digits=20)),
                ('modify', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='LineasPedido',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=50)),
                ('des', models.TextField(null=True)),
                ('cant', models.IntegerField()),
                ('precio', models.DecimalField(decimal_places=2, max_digits=20)),
                ('total', models.DecimalField(decimal_places=2, max_digits=20)),
                ('tipo', models.CharField(max_length=50)),
                ('modify', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pedidos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('modo_pago', models.CharField(max_length=50)),
                ('para_llevar', models.CharField(max_length=50)),
                ('num_avisador', models.CharField(max_length=50)),
                ('total', models.DecimalField(decimal_places=2, max_digits=20)),
                ('estado', models.CharField(default='PG_NO', max_length=10)),
                ('entrega', models.DecimalField(decimal_places=2, max_digits=20)),
                ('cambio', models.DecimalField(decimal_places=2, max_digits=20)),
                ('modify', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='lineaspedido',
            name='pedidos',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventas.Pedidos'),
        ),
        migrations.AddField(
            model_name='clientes',
            name='pedidos',
            field=models.ManyToManyField(to='ventas.Pedidos'),
        ),
        migrations.AddField(
            model_name='arqueos',
            name='conteo',
            field=models.ManyToManyField(to='ventas.Conteo'),
        ),
        migrations.AddField(
            model_name='arqueos',
            name='gastos',
            field=models.ManyToManyField(to='ventas.Gastos'),
        ),
        migrations.AddField(
            model_name='arqueos',
            name='pedidos',
            field=models.ManyToManyField(to='ventas.Pedidos'),
        ),
    ]