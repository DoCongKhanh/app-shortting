from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import Shortener, UserAgent, History
from .forms import ShortenerForm,UserAgentForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# tự  tạo from register
from django.contrib.auth.forms import UserCreationForm  
from django_user_agents.utils import get_user_agent
from user_agents import parse
# get ip_address
import socket

# Create your views here.

def login_user(request):  
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            my_user = User.objects.get(username=username)
        except:
            messages.error(request, 'User dose not exist')
        my_user = authenticate(request,username = username, password = password)
        if my_user is not None:  
            login(request, my_user)
            return redirect('/')
        else:
            messages.error(request, 'Username Or Password dose not exit')    
    return render(request, 'urlshortener/login_user.html')


def loguot_User(request):
    logout(request)
    return redirect('/')


def register_user(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            my_user = form.save()
            login(request, my_user)
            return redirect('/')
        else:
            messages.error(request, 'An error occurred during registration')
    context = {'form': form}
    return render(request, 'urlshortener/register_user.html', context)


def home_view(request):     
    form = ShortenerForm()
    context = {'form': form}
    if request.method == 'GET':
        return render(request,'urlshortener/home.html', context)
    if request.method == 'POST':         
        # get browser, operating system, version of user
        user_agent = get_user_agent(request)
        operating_system = request.user_agent.os.family
        operating_version_string = request.user_agent.os.version_string
        ua_string = request.META['HTTP_USER_AGENT']        
        browser_user_agent = parse(ua_string) 
        browser = browser_user_agent.browser.family   
        # get id address of client
        hostname = socket.gethostname()
        # print('hostname:',hostname)      
        user_ip_address = socket.gethostbyname(hostname)
        # print('user_ip_address:',user_ip_address)
        list_browsers = UserAgent.objects.filter(browser=browser,
                                                    operating_system=operating_system,
                                                    operating_version_string=operating_version_string,
                                                    user_ip_address=user_ip_address) # [Limited1, Limited2] 
        
        # print('list_browsers', list_browsers)          
        if list_browsers.exists():             
            browser_instance = list_browsers[0]       # == list_browsers.first()   lấy value đầu tiên
            # print('browser_instance', browser_instance)
            operating_systems = browser_instance.operating_system
            # print('operating_systems', operating_systems)
            operating_version_string = browser_instance.operating_version_string
            # print('version_strings', version_strings)
            used_count = browser_instance.count              # Limited1.count  Lấy số lần sử dụng
            # print('used_count', used_count)
            if used_count > 5:   
                if request.user.is_authenticated: # xác thực user sagin'  
                    used_form = ShortenerForm(request.POST) 
                    if used_form.is_valid():    
                        shortened_object = used_form.save()
                        new_url = request.build_absolute_uri('/') + shortened_object.short_url 
                        # print('new_url:', new_url)
                        long_url = shortened_object.long_url 
                        context['new_url'] = new_url
                        context['long_url'] = long_url  
                    #  ko tạo history_record được, nếu còn sử dụng tiếp thì tạo biến.
                    History.objects.create(used_user=request.user,
                                            used_short_url=new_url)
                    history_user_used = History.objects.filter(used_user=request.user)    
                    context['history_user_used'] = history_user_used
                    return render(request,'urlshortener/home.html', context)
                messages.error(request, 'You must be logged in to use') 
                return redirect('login/')     
            else:
                browser_instance.count += 1
                browser_instance.save()
            return render(request,'urlshortener/home.html',context)
        else:
            browser_instance = UserAgent.objects.create(browser=browser,
                                                          operating_system=operating_system,
                                                          operating_version_string=operating_version_string,
                                                          user_ip_address=user_ip_address)    # tạo record mới trong cột browser   
            
            used_form = ShortenerForm(request.POST) 
            if used_form.is_valid():    
                shortened_object = used_form.save()
                new_url = request.build_absolute_uri('/') + shortened_object.short_url 
                long_url = shortened_object.long_url 
                context['new_url'] = new_url
                context['long_url'] = long_url  
        context['errors'] = used_form.errors
        return render(request, 'urlshortener/home.html', context)


def redirect_url_view(request, shortened_part):
    try:
        shortener = Shortener.objects.get(short_url=shortened_part)
        shortener.times_followed += 1        
        shortener.save()
        return HttpResponseRedirect(shortener.long_url)
    except:
        raise Http404('Sorry this link is broken')