# @Author: Manuel Rodriguez <valle>
# @Date:   13-Sep-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 13-Sep-2017
# @License: Apache license vesion 2.0


from django.shortcuts import render
from tokenapi.http import JsonResponse

# Create your views here.

def index(request):
    return JsonResponse("Esto fundiona perfect")
