# @Author: Manuel Rodriguez <valle>
# @Date:   18-Sep-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 18-Sep-2017
# @License: Apache license vesion 2.0


from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, "website/index.html")
