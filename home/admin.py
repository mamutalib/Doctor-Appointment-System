
from django.contrib import admin
from home.models import ReviewRating,reviewers,patient,RegUsers, NearBy_Doctor, Appointment_List, departments
from home.models import FAQ

# Register your models here.
admin.site.register(RegUsers)
admin.site.register(NearBy_Doctor)
admin.site.register(Appointment_List)
admin.site.register(departments)
admin.site.register(patient)
admin.site.register(reviewers)
admin.site.register(ReviewRating)
admin.site.register(FAQ)




