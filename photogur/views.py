from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from photogur.models import *
from photogur.forms import LoginForm, PictureForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm

def root(request):
    return HttpResponseRedirect('/pictures')


def pictures_page(request):
    context = {'pictures': Picture.objects.all() }
    response = render(request, 'pictures.html', context)
    return HttpResponse(response)

def picture_show(request, id):
    picture = Picture.objects.get(pk=id)
    context = {'picture': picture}
    response = render(request, 'picture.html', context)
    return HttpResponse(response)

def picture_search(request):
    query = request.GET['query']
    search_results = Picture.objects.filter(artist=query)
    context = {'pictures': search_results}
    response = render(request, 'searched.html', context)
    return HttpResponse(response)

def create_comment(request):
    picture_id = request.POST['picture']
    picture = Picture.objects.filter(id=picture_id)[0]
    name = request.POST['username']
    comment = request.POST['comment']
    new_comment = Comment(name=name, message=comment, picture = picture)
    new_comment.save()
    context = {'picture': picture}
    return render(request, 'picture.html', context)

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            pw = form.cleaned_data['password']
            user = authenticate(username = username, password = pw)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/pictures')
            else:
                form.add_error('username', 'Login failed')
    else:
        form = LoginForm()

    context = {'form': form}
    http_response = render(request, 'login.html', context)
    return HttpResponse(http_response)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/pictures')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username = username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect('/pictures')
    else:
        form = UserCreationForm()
    return HttpResponse(render(request, 'signup.html', {'form': form}))

def upload_picture(request):
    if request.method == 'POST':
        form = PictureForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            artist = form.cleaned_data.get('artist')
            url = form.cleaned_data.get('url')
            username = request.user
            new_picture = Picture.objects.create(title = title, artist = artist, url = url, user = request.user)
            new_picture.save()
            return HttpResponseRedirect('/pictures')
    else:
        form = PictureForm()
    context = {'form': form}
    return HttpResponse(render(request, 'upload.html', context))