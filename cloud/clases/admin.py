# @Author: Manuel Rodriguez <valle>
# @Date:   04-Sep-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 13-Sep-2017
# @License: Apache license vesion 2.0

# Register your models here.
from django.contrib import admin
from django.apps import apps

app = apps.get_app_config('clases')

for model_name, model in app.models.items():
    if not "_" in model_name:
        admin.site.register(model)
