# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-23 15:59
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
                ('caja_dia', models.DecimalField(decimal_places=2, default=0.0, max_digits=20, null=True)),
                ('efectivo', models.DecimalField(decimal_places=2, default=0.0, max_digits=20, null=True)),
                ('cambio', models.DecimalField(decimal_places=2, default=0.0, max_digits=20, null=True)),
                ('total_gastos', models.DecimalField(decimal_places=2, default=0.0, max_digits=20, null=True)),
                ('tarjeta', models.DecimalField(decimal_places=2, default=0.0, max_digits=20, null=True)),
                ('descuadre', models.DecimalField(decimal_places=2, default=0.0, max_digits=20, null=True)),
                ('modify', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Arqueo',
            },
        ),
        migrations.CreateModel(
            name='Clientes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('apellido', models.CharField(default='', max_length=100, null=True)),
                ('email', models.EmailField(blank=True, default='', max_length=100, null=True)),
                ('telefono', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('nota', models.TextField(blank=True, default='', null=True)),
                ('fecha_add', models.DateField(auto_now_add=True)),
                ('modify', models.DateTimeField(auto_now=True)),
                ('direccion', models.IntegerField(default=0, null=True)),
            ],
            options={
                'ordering': ['apellido', 'nombre'],
                'verbose_name': 'Cliente',
            },
        ),
        migrations.CreateModel(
            name='Conteo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('can', models.IntegerField(verbose_name='Cantidad')),
                ('tipo', models.DecimalField(decimal_places=2, default=0.0, max_digits=20, null=True, verbose_name='Tipo de moneda')),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=20, null=True)),
                ('texto_tipo', models.CharField(blank=True, default='Euros', max_length=100)),
                ('modify', models.DateTimeField(auto_now=True, verbose_name='Modificado')),
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
            options={
                'verbose_name': 'Direccion',
            },
        ),
        migrations.CreateModel(
            name='Gastos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('des', models.CharField(default='Nada', max_length=100, verbose_name='Descripcion')),
                ('gasto', models.DecimalField(decimal_places=2, default=0.0, max_digits=20, null=True)),
                ('modify', models.DateTimeField(auto_now=True, verbose_name='Modificado')),
            ],
            options={
                'verbose_name': 'Gasto',
            },
        ),
        migrations.CreateModel(
            name='LineasPedido',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=50)),
                ('des', models.TextField(null=True)),
                ('cant', models.IntegerField()),
                ('precio', models.DecimalField(decimal_places=2, default=0.0, max_digits=20, null=True)),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=20, null=True)),
                ('tipo', models.CharField(max_length=50)),
                ('modify', models.DateTimeField(auto_now=True)),
                ('servido', models.BooleanField(default=False)),
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
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=20, null=True)),
                ('estado', models.CharField(default='PG_NO', max_length=10)),
                ('entrega', models.DecimalField(decimal_places=2, default=0.0, max_digits=20, null=True)),
                ('cambio', models.DecimalField(decimal_places=2, default=0.0, max_digits=20, null=True)),
                ('modify', models.DateTimeField(auto_now=True)),
                ('servido', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-id'],
                'verbose_name': 'Pedido',
            },
        ),
        migrations.CreateModel(
            name='PedidosExtra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('importe', models.DecimalField(decimal_places=2, max_digits=20)),
                ('numero_pedido', models.IntegerField()),
                ('modo_pago', models.CharField(blank=True, default='Efectivo', max_length=50, null=True)),
                ('modify', models.DateTimeField(auto_now=True)),
                ('estado', models.CharField(blank=True, default='no_arqueado', max_length=50, null=True)),
            ],
            options={
                'verbose_name': 'Pedidos Extra',
            },
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
        migrations.AddField(
            model_name='arqueos',
            name='pedidosextra',
            field=models.ManyToManyField(to='ventas.PedidosExtra'),
        ),
    ]
