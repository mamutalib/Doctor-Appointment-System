
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

# Create your models here.
class RegUsers(models.Model):
    UserName = models.CharField(max_length = 122)
    Fname = models.CharField(max_length = 122)
    Lname = models.CharField(max_length = 122)
    Email = models.EmailField(max_length=254)
    Password = models.IntegerField()
    CPassword = models.IntegerField()
    Doc_pat = models.CharField(max_length = 122)
    Date = models.DateField()

    def __str__(self):
        return self.UserName


def  filepath(request, filename):
    old_filename=filename
    
    return os.path.join('upload/',filename)



class NearBy_Doctor(models.Model):
    doctor_name = models.CharField(max_length=122)
    department = models.CharField(max_length=122)
    location = models.CharField(max_length=122)
    working_H = models.CharField(max_length=122)
    brife =models.TextField()
    clinicloc = models.CharField( max_length=122)
    nw_pat_fee = models.CharField( max_length=122)
    ret_pat_fee = models.CharField( max_length=122)
    repo_fee = models.CharField( max_length=122)
    lag_spoken = models.CharField( max_length=122)
    sunday_mor = models.CharField( max_length=122)
    sunday_ev = models.CharField( max_length=122)
    monday_mor = models.CharField( max_length=122)
    monday_ev = models.CharField( max_length=122)
    tuesday_mor = models.CharField( max_length=122)
    tuesday_ev = models.CharField( max_length=122)
    wedday_mor = models.CharField( max_length=122)
    wedday_ev = models.CharField( max_length=122)
    thursday_mor = models.CharField( max_length=122)
    thursday_ev = models.CharField( max_length=122)
    frday_mor = models.CharField( max_length=122)
    frday_ev = models.CharField( max_length=122)
    satday_mor = models.CharField( max_length=122)
    satday_ev = models.CharField( max_length=122)
    doc_image=models.ImageField(upload_to="upload/", null=True,blank=True)

    def __str__(self):
        return self.doctor_name


# for patient
class patient(models.Model):
    user=models.ForeignKey(RegUsers,null=True,on_delete=models.SET_NULL)
    pat_image=models.ImageField(upload_to="upload/", null=True,blank=True)
    pat_name =models.CharField( max_length=122)
    pat_age=models.CharField( max_length=122)
    pat_location=models.CharField( max_length=122)
    pat_lag_spoken=models.CharField( max_length=122)
    pat_occu=models.CharField( max_length=122)
    

    def __str__(self):
        return self.pat_name


# for book appointment
class Appointment_List(models.Model):
    se_dept = models.CharField(max_length=122)
    se_doc = models.CharField(max_length=122)
    patient_name = models.CharField(max_length=122)
    patient_phone = models.IntegerField()
    patient_email = models.EmailField(max_length=254)
    calendar = models.DateField()

    def __str__(self):
        return self.patient_name

#For departments
class departments(models.Model):
    dep_name = models.CharField(max_length=50)
    def __str__(self):
        return self.dep_name
    


# for rating section
class rating(models.Model):
    name = models.CharField(max_length=50)
    score = models.IntegerField(default=0,
    validators=[
        MaxValueValidator(5),
        MinValueValidator(0),
    ]
    
    )

    def __str__(self):
        return self.name
    
    



class health(models.Model):
    blood= models.IntegerField()
    bllod_2=models.IntegerField()
    suger_lvl= models.IntegerField()
    date = models.DateTimeField()

    






# for review and rating by kopil
class ReviewRating(models.Model):
    # doc = models.ForeignKey(NearBy_Doctor, on_delete=models.CASCADE,lazy='deferred')
    # pat = models.ForeignKey(patient, on_delete=models.CASCADE,lazy='deferred')
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject



class payment(models.Model):
    pass










    
#for review section
class reviewers(models.Model):
    name = models.CharField(max_length=50)
    reviews = models.CharField(max_length=200)
    time = models.DateTimeField()
    def __str__(self):
        return self.name

# for rating section
class rating(models.Model):
    name = models.CharField(max_length=50)
    score = models.IntegerField(default=0,
    validators=[
        MaxValueValidator(5),
        MinValueValidator(0),
    ]
    
    )

    def __str__(self):
        return self.name
    
    



class health(models.Model):
    blood= models.IntegerField()
    bllod_2=models.IntegerField()
    suger_lvl= models.IntegerField()
    date = models.DateTimeField()

    


#----- Dynamic FAQ Section ------#
# class Faq(models.Model):
#     question = models.CharField(max_length=200)
#     answer = models.TextField()
#     category = models.CharField(max_length=50)
#     date_asked = models.DateTimeField()

class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    deleted = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)




# patient list 
# in your models.py file

class PatientList(models.Model):
    patient_profile = models.ForeignKey(patient, on_delete=models.CASCADE)
    # other fields for the PatientList model

