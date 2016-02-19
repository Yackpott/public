from django.shortcuts import render
from django.http import HttpResponse, HttpRequest


def index(view):
    return HttpResponse("Hello, world. You're at the polls index.")


def login(view):
    return HttpResponse("Login")


def polls(view):
    return HttpResponse("Polls")
