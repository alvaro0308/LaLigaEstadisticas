from django.http import HttpResponse
import datetime
from django.template import Template, Context
from django.template import loader
from django.shortcuts import render


def hello(request):
    name = "John"
    # externDoc = open(
    #     "/home/alvaro/github/LaLigaEstadisticas/LaLigaEstadisticasWeb/LaLigaEstadisticasWeb/templates/template.html")
    # plt = Template(externDoc.read())

    # externDoc.close()

    # externDoc = loader.get_template('template.html')

    # ctx = Context({"name": name})

    # doc = externDoc.render({"name": name})

    return render(request, "template.html", {"name": name})


def c(request):
    currentTime = datetime.datetime.now()

    return render(request, "c.html", {"time": currentTime})


def time(request):
    currentTime = datetime.datetime.now()
    text = """<html>
    <body>
    <h1>
    Date and time %s
    </h1>
    </body>
    </html>""" % currentTime

    return HttpResponse(text)
