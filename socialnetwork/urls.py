"""webapps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url

urlpatterns = [
    url(r'^$', 'socialnetwork.views.home',name='home'),
    #url(r'^add-item', 'private_todo_list.views.add_item'),
    # Route for built-in authentication with our own custom login page
    url(r'^add-message', 'socialnetwork.views.add_message',name='add-message'),
    url(r'^showglobal', 'socialnetwork.views.showglobal',name='showglobal'),
    url(r'^check-profile', 'socialnetwork.views.check_other',name='check_other'),
    url(r'^create-profile', 'socialnetwork.views.create_profile',name='create_profile'),
    url(r'^edit-profile', 'socialnetwork.views.edit_profile',name='edit_profile'),
    url(r'^following', 'socialnetwork.views.following',name='following'),
    url(r'^checkfollowing', 'socialnetwork.views.checkfollowing',name='checkfollowing'),
    url(r'^picture', 'socialnetwork.views.picture',name='picture'),
    url(r'^getposts', 'socialnetwork.views.getposts',name='getposts'),
    url(r'^add-contents', 'socialnetwork.views.addcontents',name='add-contents'),
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name':'login.html'},name='login'),
    # Route to logout a user and send them back to the login page
    url(r'^logout$', 'django.contrib.auth.views.logout_then_login',name='logout'),
    # The following URL should match any username valid in Django and
    # any token produced by the default_token_generator
    url(r'^confirm-registration/(?P<username>[a-zA-Z0-9_@\+\-]+)/(?P<password>[a-zA-Z0-9_@\+\-]+)/(?P<token>[a-z0-9\-]+)$',
        'socialnetwork.views.confirm_registration', name='confirm'),
    url(r'^register$', 'socialnetwork.views.register',name='register'),
]

