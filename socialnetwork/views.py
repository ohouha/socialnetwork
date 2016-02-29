from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.db import transaction
from django.http import HttpResponse, Http404
from mimetypes import guess_type
from django.core import serializers
from django.http import HttpResponse
import json

# Used to generate a one-time-use token to verify a user's email address
from django.contrib.auth.tokens import default_token_generator

# Used to send mail from within Django
from django.core.mail import send_mail


from socialnetwork.models import Item,profile,Person,Comments
from socialnetwork.forms import RegistrationForm, messageform,profileform

from datetime import datetime

from socialnetwork.s3 import s3_upload

# Create your views here.
@login_required
def home(request):
    # Sets up list of just the logged-in user's (request.user's) items
    pro=profile.objects.filter(user=request.user)
    items = Item.objects.filter(username=request.user).order_by("-date")

    profile_to_edit=get_object_or_404(profile,user=request.user)
    form=profileform(instance=profile_to_edit)

    if profile.objects.filter(user=request.user).exists():
        pic=profile.objects.filter(user=request.user)
        context={'items' : items,'pro':pro,'pic':pic,'form':form}
    else:
        context={'items' : items,'pro':pro,'form':form}
    return render(request, 'index.html', context)

@login_required
def add_message(request):
    errors = []
    items = Item.objects.order_by("-date")
    if request.method == 'GET':
        pro=profile.objects.filter(user=request.user)
        profile_to_edit=get_object_or_404(profile,user=request.user)
        proform=profileform(instance=profile_to_edit)
        context = { 'items' : items,'form': messageform(),'errors' : errors,'pro':pro,'proform':proform }
        return render(request, 'globalstream.html', context)

    pro=profile.objects.filter(username=request.user)[0]
    entry = Item(user=pro,date=datetime.now(),username=request.user)
    form = messageform(request.POST, instance=entry)

    if not form.is_valid():
        pro=profile.objects.filter(user=request.user)
        profile_to_edit=get_object_or_404(profile,user=request.user)
        proform=profileform(instance=profile_to_edit)
        context = { 'items' : items,'form': form,'errors' : errors,'pro':pro,'proform':proform}
        return render(request, 'globalstream.html', context)
   
    # Save the new record
    form.save()

    items = Item.objects.order_by("-date")
    username=request.user;
    pro=profile.objects.filter(user=request.user)
    profile_to_edit=get_object_or_404(profile,user=request.user)
    proform=profileform(instance=profile_to_edit)
    context = {'items' : items,'form': form,'errors' : errors,'username':username,'pro':pro,'proform':proform}
    return render(request, 'globalstream.html', context)

@login_required
def showglobal(request):
    it=Item.objects.order_by("-date")
    username=request.user;
    pro=profile.objects.filter(user=request.user)
    profile_to_edit=get_object_or_404(profile,user=request.user)
    proform=profileform(instance=profile_to_edit)
    return render(request, 'globalstream.html', {'items' : it,'form': messageform(),'username':username,'pro':pro,'proform':proform})

@login_required
def check_other(request):
    errors = []
    username=request.POST.get('user','')
    currentuser=request.POST.get('currentuser','')
    if username==currentuser:
        pro=profile.objects.filter(user=request.user)
        items = Item.objects.filter(username=request.user).order_by("-date")
        #return render(request, 'index.html', {'items' : items,'pro':pro})
        return redirect(reverse('home'))

    items = Item.objects.filter(username=username).order_by("-date")
    pro=profile.objects.filter(username=username)
    profile_to_edit=get_object_or_404(profile,user=request.user)
    proform=profileform(instance=profile_to_edit)
    name=request.user;
    context = {'items' : items, 'errors' : errors,'name':username,'profiles':pro,'proform':proform}
    return render(request, 'otherprofile.html', context)

@login_required
def create_profile(request):
    if request.method == 'GET':
        context = { 'form': profileform()}
        return render(request, 'createprofile.html', context)


    entry = profile(user=request.user,username=request.user)
    form = profileform(request.POST, request.FILES, instance=entry)

    if not form.is_valid():
        context = { 'form': form }
        return render(request, 'createprofile.html', context)
   
    # Save the new record
    form.save()
    #url
    profile_to_edit=get_object_or_404(profile,user=request.user)
    if form.cleaned_data['pic']:
        url = s3_upload(form.cleaned_data['pic'], profile_to_edit.id)
        profile_to_edit.picture = url
        profile_to_edit.save()
        #form.save()

    return redirect(reverse('home'))

@login_required
def edit_profile(request):
    profile_to_edit=get_object_or_404(profile,user=request.user)

    if request.method == 'GET':
        form=profileform(instance=profile_to_edit)
        if profile.objects.filter(user=request.user).exists():
            pic=profile.objects.filter(user=request.user)
            context={'form':form,'pic':pic}
        else:
            context={'form':form}
        return render(request,'editprofile.html',context);
   
    form=profileform(request.POST,request.FILES,instance=profile_to_edit)
    if not form.is_valid():
        pic=profile.objects.filter(user=request.user)
        if profile.objects.filter(user=request.user).exists():
            pic=profile.objects.filter(user=request.user)
            context={'form':form,'pic':pic}
        else:
            context={'form':form}
        return render(request,'editprofile.html',context);

    if form.cleaned_data['pic']:
            url = s3_upload(form.cleaned_data['pic'], profile_to_edit.id)
            profile_to_edit.picture = url
    
    form.save()
    return redirect(reverse('home'))

@login_required
def checkfollowing(request):
    followposts=Person.objects.filter(user=request.user).values_list('otherpeople', flat=True)
    messages=Item.objects.filter(username__in=followposts).order_by('-date')
    pro=profile.objects.filter(username=request.user)
    profile_to_edit=get_object_or_404(profile,user=request.user)
    proform=profileform(instance=profile_to_edit)
    context = {'followposts' : followposts,'messages':messages,'pro':pro,'proform':proform}
    return render(request, 'followingstream.html', context)

@login_required
def following(request):

    username=request.POST.get('user','')
    number=request.POST.get('number','')

    if not Person.objects.filter(username=request.user, otherpeople=username).exists():
    #add
        new_item = Person(user=request.user,username=request.user, otherpeople=username)
        new_item.save()
        number='Unfollow'
    #delete
    else:
        item=Person.objects.filter(username=request.user, otherpeople=username)
        item.delete()
        number='Follow'

    items = Item.objects.filter(username=username).order_by("-date")
    pro=profile.objects.filter(username=username)
    name=request.user;
    context = {'items' : items, 'number' : number,'name':username,'profiles':pro}
    return render(request, 'otherprofile.html', context)

@login_required
def picture(request):
    entry=get_object_or_404(profile,user=request.user)
    if not entry.picture:
        raise HTTP404

    content_type=guess_type(entry.picture.name)
    return HttpResponse(entry.picutre, mimetype=content_type)

@login_required

def getposts(request):
    queryset = Item.objects.order_by("-date")
    list=[]
    for row in queryset:
        date= row.date.isoformat()
        if(row.user.picture!=""):   
            url=row.user.picture
        else:
            url=""
        list.append({'pk':row.pk, 'username': row.username, 'date': date,'message':row.message,'url':url})
        
    
    #response_text = serializers.serialize('json',  Item.objects.order_by("-date"))
    #return HttpResponse(response_text, content_type='application/json')
    recipe_list_json = json.dumps(list) #dump list as JSON                           
    return HttpResponse(recipe_list_json, 'application/javascript')

@login_required
def addcontents(request):
    if request.method == 'POST':
        list=[]
        comment=request.POST.get('content')
        itemid=request.POST.get('userid')
        #add things to content
        otheritem=Item.objects.filter(id=itemid)[0]
        myprofile=profile.objects.filter(user=request.user)[0]
        commentdate=datetime.now()
        new_item = Comments(date=commentdate,content=comment,username=request.user, post=otheritem,mypro=myprofile) 
        new_item.save()
        commenttime=new_item.date.isoformat()
        if(new_item.mypro.picture!=""):   
            url=new_item.mypro.picture
        else:
            url=""
        list.append({'comment':comment,'commenttime':commenttime,'url':url})
        comment_json = json.dumps(list) #dump list as JSON  
                                
        return HttpResponse(comment_json, 'application/json')
   

@transaction.atomic
def register(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['registerform'] = RegistrationForm()
        return render(request, 'register.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    registerform = RegistrationForm(request.POST)
    context['registerform'] = registerform

    # Validates the form.
    if not registerform.is_valid():
        return render(request, 'register.html', context)

    # At this point, the form data is valid.  Register and login the user.
    new_user = User.objects.create_user(username=registerform.cleaned_data['username'], 
                                        password=registerform.cleaned_data['password1'],
                                        email=registerform.cleaned_data['email'])
    # Mark the user as inactive to prevent login before email confirmation.
    new_user.is_active = False
    new_user.save()

    # Generate a one-time use token and an email message body
    token = default_token_generator.make_token(new_user)

    email_body = """
Welcome to the Simple Address Book.  Please click the link below to
verify your email address and complete the registration of your account:

  http://%s%s
""" % (request.get_host(), 
       reverse('confirm', args=(new_user.username,registerform.cleaned_data['password1'],token)))

    send_mail(subject="Verify your email address",
              message= email_body,
              from_email="wanyanz@cmu.edu",
              recipient_list=[new_user.email])

    context['email'] = registerform.cleaned_data['email']
    return render(request, 'needs-confirmation.html', context)
    
@transaction.atomic
def confirm_registration(request, username, password,token):
    user = get_object_or_404(User, username=username)

    # Send 404 error if token is invalid
    if not default_token_generator.check_token(user, token):
        raise Http404

    # Otherwise token was valid, activate the user.
    user.is_active = True
    user.save()

    new_user = authenticate(username=username,
                            password=password)
    login(request, new_user)

    return redirect(reverse('create_profile'))   
    
    
    
    
    #new_user.save()
    # Logs in the new user and redirects to his/her todo list
    #new_user = authenticate(username=registerform.cleaned_data['username'],
                            #password=registerform.cleaned_data['password1'])
    #login(request, new_user)
    #context={}
    #return redirect(reverse('create_profile'))
