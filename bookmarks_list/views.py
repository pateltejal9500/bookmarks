
from django.template import RequestContext, loader
from bookmarks_list.models import List, Link, ListForm, LinkForm, UserProfile, LoginForm, RegisterForm
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.core.context_processors import csrf
from django.http import Http404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from django.db.models.signals import post_save


def index(request):
    lists = List.objects.all()
    template = loader.get_template('bookmarks_list/index.html')
    context = {'lists': lists}
    return render(request, 'bookmarks_list/index.html', context)

def detail(request, list_id):
  try:
    p = List.objects.get(pk=list_id)
  except List.DoesNotExist:
    raise Http404
  links = Link.objects.filter(list=list_id)
  list_info = List.objects.get(pk=list_id)
  template = loader.get_template('bookmarks_list/detail.html')
  context = {'links': links, 'list':list_info}
  return render(request, 'bookmarks_list/detail.html', context)

@login_required()
def add(request):
  if request.method == 'POST':
    form = ListForm(request.POST)
    if form.is_valid():
      name = form.cleaned_data['name']
      l = List(name=name, date_created=timezone.now(), date_modified=timezone.now())
      l.save()
      return HttpResponseRedirect("/bookmarks_list/")
    else:
      messages.error(request, "Error")
      return render(request, 'bookmarks_list/add.html', {'form':form})
  else:
      form = ListForm()
      return render(request, 'bookmarks_list/add.html', {'form': form})

@login_required()
def add_link(request, list_id):
  if request.method == 'POST':
    form = LinkForm(request.POST)
    if form.is_valid():
      list_of_link =  List.objects.get(pk=list_id)
      url = form.cleaned_data['url']
      tag = form.cleaned_data['tag']
      name = form.cleaned_data['name']
      l = Link(name=name, link_url=url, date_created=timezone.now(), date_modified=timezone.now(), tag=tag)
      l.save()
      list_of_link.link.add(l)
      return HttpResponseRedirect("/bookmarks_list/"+list_id)
    else:
      messages.error(request, "Error")
      return render(request, 'bookmarks_list/add_link.html', {'form':form, 'list_id': list_id})
  else:
      form = LinkForm()
      context = {'list_id': list_id, 'form':form}
      return render(request, 'bookmarks_list/add_link.html', context)

def delete(request, link_id):
  if request.method == 'POST':
    link = Link.objects.get(pk=link_id)
    link.delete()
    list_id = request.POST["list_id"]
    return HttpResponseRedirect ("/bookmarks_list/"+list_id)

def loginPerson(request):
  if request.method == 'POST':
    form = LoginForm(request.POST)
    if form.is_valid():
      username = request.POST['username']
      password = request.POST['password']
      user = authenticate(username = username, password = password)
      if user is not None:
       if user.is_active:
         login(request, user)
         return HttpResponseRedirect ("/bookmarks_list/")
       else:
        return render(request, 'bookmarks_list/login.html', {'form':form})
      else:
       return render(request, 'bookmarks_list/login.html', {'form':form})
    else:
      messages.error(request, "ERROR")
      return render(request, 'bookmarks_list/login.html', {'form':form})
  else:
      form = LoginForm()
      context = {'form':form}
      return render(request, 'bookmarks_list/login.html', context)
      
def register(request):
  if request.method == 'POST':
    form = RegisterForm(request.POST)
    if form.is_valid():
      username = form.cleaned_data['username']
      password = form.cleaned_data['password']
      user = User.objects.create_user(username = username, password = password) 
      profile = UserProfile()
      profile.user = user
      profile.save()
      return HttpResponseRedirect("/bookmarks_list/") 
  else:
      form = RegisterForm()
      context = {'form':form}
      return render(request, 'bookmarks_list/register.html', context)
      
def logoutPerson(request):
  logout(request)
  return HttpResponseRedirect("/bookmarks_list/")


  


