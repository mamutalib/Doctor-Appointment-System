


from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name = 'home'),
    path('contact',views.contact,name = 'contact'),
    path('about',views.about,name = 'about'),
    path('services',views.services,name = 'services'),
    path('signUp',views.signUp,name = 'signUp'),
    path('login',views.login,name = 'login'),
    path('signout',views.signout,name = 'signout'),
    path('base',views.base,name = 'base'),
    path('doctorAcc',views.doctorAcc,name = 'doctorAcc'),
    path('patientAcc',views.patientAcc,name = 'patientAcc'),
    path('NearByDoc',views.NearByDoc,name = 'NearByDoc'),
    path('emDoc',views.emDoc,name = 'emDoc'),
    path('review',views.review,name = 'review'),
    path('rateing',views.rateing,name = 'rateing'),
    path('submit_review', views.submit_review, name='submit_review'),
    path('payment',views.payment,name = 'payment'),

]





from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name = 'home'),
    path('contact',views.contact,name = 'contact'),
    path('about',views.about,name = 'about'),
    path('services',views.services,name = 'services'),
    path('signUp',views.signUp,name = 'signUp'),
    path('login',views.login,name = 'login'),
    path('signout',views.signout,name = 'signout'),
    path('base',views.base,name = 'base'),
    path('doctorAcc',views.doctorAcc,name = 'doctorAcc'),
    path('patientAcc',views.patientAcc,name = 'patientAcc'),
    path('NearByDoc',views.NearByDoc,name = 'NearByDoc'),
    path('emDoc',views.emDoc,name = 'emDoc'),
    path('review',views.review,name = 'review'),
    path('rateing',views.rateing,name = 'rateing'),
    
    # for Department wise doctor list 
    # path('docDept', views.docDept, name='Doctors Profile'), 
    path('Ophthalmologists', views.Ophthalmologists, name='Ophthalmologists Doctors Profile'),
    path('Endocrinologists', views.Endocrinologists, name='Endocrinologists Doctors Profile'),
    path('Gastroenterologists', views.Gastroenterologists, name='Gastroenterologists Doctors Profile'),
    path('Cardiologists', views.Cardiologists, name='Cardiologists Doctors Profile'),
    path('Psychiatry', views.Psychiatry, name='Psychiatry Doctors Profile'),
    path('Orthopedics', views.Orthopedics, name='Orthopedics Doctors Profile'),
    path('Pediatrics', views.Pediatrics, name='Pediatrics Doctors Profile'),
    
    
    
    
    # path('faq', views.faq, name = 'faq')
    path('faq/', views.faq_view, name='faq'),
    path('faq/submit/', views.submit_question, name='submit_question'),
    path('faq/answer/<int:pk>/', views.answer_question, name='answer_question'),
    path('faq/delete/<int:pk>/', views.delete_question, name='delete_question'),


]



