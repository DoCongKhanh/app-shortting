from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import ShortenURL, UserAgent, UserAgentCondition, HistoryShorten
from .forms import ShortenURLForm,UserAgentForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# create from register
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


# def shorten_url_get(request):
#     used_form = ShortenURLForm(request.POST) 
#     if used_form.is_valid():  
#         shortened_object = used_form.save()
#         new_url = request.build_absolute_uri('/') + shortened_object.shorten_url 
#         original_url = shortened_object.original_url                        
#         context['new_url'] = new_url
#         context['original_url'] = original_url
        



def home_view(request):     
    form = ShortenURLForm()
    context = {'form': form}
    if request.method == 'GET':
        return render(request,'urlshortener/home.html', context)
    if request.method == 'POST':     
        # get  operating system, version of user
        user_agent = get_user_agent(request)
        operating_system = request.user_agent.os.family
        operating_version_string = request.user_agent.os.version_string
        # get browser of user
        ua_string = request.META['HTTP_USER_AGENT']        
        browser_user_agents = parse(ua_string) 
        browser = browser_user_agents.browser.family   
        # get id address of client
        hostname = socket.gethostname()     
        user_ip_address = socket.gethostbyname(hostname)
        # filter models UserAgent with para browser,... from request(http) assign to list_instance
        list_instance = UserAgent.objects.filter(browser=browser,
                                                    operating_system=operating_system,
                                                    operating_version_string=operating_version_string,
                                                    user_ip_address=user_ip_address)
        # from list_instance, view it exits 
        if list_instance.exists():
            # get value first. it's request(http) assign to instance_user
            instance_user = list_instance.first()
            # filter models UserAgentCondition with para is instance_user
            list_user_agent = UserAgentCondition.objects.filter(user_agent=instance_user)
            # get value of it. view, how many times used
            user_agent_first = list_user_agent.first()
            used_count = user_agent_first.time_used
            # print('used_count',used_count)
            if used_count > 5:
                # Limited used through the user
                if request.user.is_authenticated:  
                    used_form = ShortenURLForm(request.POST) 
                    if used_form.is_valid():  
                        shortened_object = used_form.save()
                        new_url = request.build_absolute_uri('/') + shortened_object.shorten_url 
                        original_url = shortened_object.original_url                        
                        context['new_url'] = new_url
                        context['original_url'] = original_url 
                    # method filter -> get list value models ShortenURL -> get first value of list -> create record models HistoryShorten(shortend_url).
                    list_shorten_instance = ShortenURL.objects.filter(shorten_url=shortened_object.shorten_url)  
                    shorten_instance = list_shorten_instance.first()           
                    # print('shorten_instance',shorten_instance)                                                        
                    HistoryShorten.objects.create(shortend_url=shorten_instance,                # taọ record (ở khóa ngoại) để tham chiếu tới bảng chứa khóa chính để lấy objects
                                                    user=request.user)                 
                    # Filter models HistoryShorten get all objects through the user login and print in templates
                    shortend_url_instance = HistoryShorten.objects.filter(user=request.user)                                                                                                                                                
                    context['shortend_url_instance'] = shortend_url_instance              
                    return render(request,'urlshortener/home.html', context)
                messages.error(request,'You have used up all 5 free spins. You must be logged in to use') 
                return redirect('login/')
            else:               
                if request.user.is_authenticated:  
                    used_form = ShortenURLForm(request.POST) 
                    if used_form.is_valid():  
                        shortened_object = used_form.save()
                        new_url = request.build_absolute_uri('/') + shortened_object.shorten_url 
                        original_url = shortened_object.original_url                        
                        context['new_url'] = new_url
                        context['original_url'] = original_url
                    # method filter -> get list value models ShortenURL -> get first value of list -> create record models HistoryShorten(shortend_url).
                    list_shorten_instance = ShortenURL.objects.filter(shorten_url=shortened_object.shorten_url)  
                    shorten_instance = list_shorten_instance.first()           
                    # print('shorten_instance',shorten_instance)                                                        
                    HistoryShorten.objects.create(shortend_url=shorten_instance,                # taọ record (ở khóa ngoại) để tham chiếu tới bảng chứa khóa chính để lấy objects
                                                    user=request.user)                 
                    # Filter models HistoryShorten get all objects through the user login and print in templates
                    shortend_url_instance = HistoryShorten.objects.filter(user=request.user)                                                                                                                                                
                    context['shortend_url_instance'] = shortend_url_instance
                    return render(request,'urlshortener/home.html',context)  
                else:
                    used_form = ShortenURLForm(request.POST)                                                    
                    if used_form.is_valid():  
                        shortened_object = used_form.save()
                        new_url = request.build_absolute_uri('/') + shortened_object.shorten_url 
                        original_url = shortened_object.original_url 
                        context['new_url'] = new_url
                        context['original_url'] = original_url                         
                        # History.objects.create(used_short_url=new_url,
                        #                        ip_address=user_ip_address)              
                        # history_user_used = History.objects.filter(ip_address=user_ip_address)
                        # context['history_user_used'] = history_user_used
                    user_agent_first.time_used += 1
                    user_agent_first.save()       
                return render(request,'urlshortener/home.html',context)  
       
        else:
            browser_instance = UserAgent.objects.create(browser=browser,
                                                        operating_system=operating_system,
                                                        operating_version_string=operating_version_string,
                                                        user_ip_address=user_ip_address)    # tạo record mới trong các cột attributes          
            
            UserAgentCondition.objects.create(user_agent=browser_instance) 
            list_user_agent = UserAgentCondition.objects.filter(user_agent=browser_instance)
            user_agent_objects = list_user_agent[0]
            # print('list_user_agent',list_user_agent)
            # print('user_agent_objects',user_agent_objects.user_agent.operating_system)
            user_agent_objects.time_used += 1
            user_agent_objects.save() 
            
            used_form = ShortenURLForm(request.POST) 
            if used_form.is_valid():  
                shortened_object = used_form.save()
                new_url = request.build_absolute_uri('/') + shortened_object.shorten_url 
                original_url = shortened_object.original_url 
                context['new_url'] = new_url
                context['original_url'] = original_url                    
                    # History.objects.create(used_short_url=new_url,
                    #                        ip_address=user_ip_address)
                    # history_user_used = History.objects.filter(ip_address=user_ip_address)
                    # context['history_user_used'] = history_user_used
            context['errors'] = used_form.errors
            return render(request, 'urlshortener/home.html', context)


def redirect_url_view(request, shortened_part):

    try:
        shortener = ShortenURL.objects.get(shorten_url=shortened_part)
        shortener.times_followed += 1        
        shortener.save()  
        return HttpResponseRedirect(shortener.original_url)     
    except:
        raise Http404('Sorry this link is broken :(')
