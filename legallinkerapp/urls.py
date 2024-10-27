from django.urls import path
from  .views import * 
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path


urlpatterns = [
    path('register/advocate/', register, name='register_advocate'),
    path('register/user', register, name='register_user'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', adminDashboard, name='dashboard'),
    path('advocate/<int:advocate_id>/approve/', approve_advocate, name='approve_advocate'),
    path('', home, name='home'),
    path('services/', services, name='services'),
    path('about/', about, name='about'),
    path('view_all_cases/', view_all_cases, name='view_all_cases'),
    path('case_studies/', case_studies, name='case_studies'),
    path('cases/add/', add_case, name='add_case'),
    path('cases/', view_cases, name='view_cases'),
    path('cases/edit/<int:case_id>/', edit_case, name='edit_case'),
    path('cases/delete/<int:case_id>/', delete_case, name='delete_case'),
    path('contact/', contact_view, name='contact'),
    path('user_registration/', user_registration, name='user_registration'),
    path('userDashboard/', userDashboard, name='userDashboard'),
    path('advocateDashboard/', advocateDashboard, name='advocateDashboard'),
    path('approve_user/<int:user_id>/', approve_user, name='approve_user'),
    path('send_message/<int:recipient_id>/', send_message, name='send_message'),
    path('sent_messages/', view_sent_messages, name='view_sent_messages'),
    path('received_messages/', view_received_messages, name='view_received_messages'),
    path('view_advocates/', view_advocates, name='view_advocates'),
    path('view_all_users/', view_all_users, name='view_all_users'),
    path('view_all_advocates/', view_all_advocates, name='view_all_advocates'),
    path("update-user/<int:user_id>/", update_user, name="update_user"),
    path("delete-user/<int:user_id>/",delete_user, name="delete_user"),
    path('advocate/update/<int:advocate_id>/', update_advocate, name='update_advocate'),
    path('advocate/delete/<int:advocate_id>/', delete_advocate, name='delete_advocate'),
    
     path('user/profile/', view_user_profile, name='view_user_profile'),
    path('user/profile/update/', update_user_profile, name='update_user_profile'),
    path('user/password/change/', change_user_password, name='change_user_password'),
    
    path('advocate/profile/', view_advocate_profile, name='view_advocate_profile'),
    path('advocate/profile/update/', update_advocate_profile, name='update_advocate_profile'),
    path('advocate/password/change/', change_advocate_password, name='change_advocate_password'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])