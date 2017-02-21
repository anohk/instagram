from django.conf.urls import url

from . import views

app_name = 'myuser'
urlpatterns = [
    url(r'^signup/$', views.signup_model_form_fbv, name='signup'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_fbv, name='logout'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^change_profile_img/$', views.change_profile_image, name='change_profile_img'),

]
