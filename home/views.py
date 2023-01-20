
from django.shortcuts import render, HttpResponse, redirect
from datetime import datetime
from home.models import patient,NearBy_Doctor, Appointment_List, departments,rating,reviewers,health,ReviewRating
from django.contrib import messages
from .forms import FAQForm
from .models import PatientList
from .models import patient


# for user authticcation 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as authlogin,logout
# email
# from MrDoc import settings
# from django.core.mail import send_mail
from email.message import EmailMessage
import ssl
import smtplib
from django.template.response import TemplateResponse
from .forms import ReviewForm
from .models import patient



# Create your views here.
def home(request):
    # this form is accessing for taking appointment list from home page
    if request.method == "POST":
        depName = request.POST.get("sedep")
        Pname = request.POST.get("name")
        Pmail = request.POST.get("mail")
        docName = request.POST.get("sedoc")
        Pphone = request.POST.get("phone")
        AppointDate = request.POST.get("date")

        appointment_list = Appointment_List(se_dept = depName, se_doc = docName, patient_name = Pname, patient_phone = Pphone, patient_email = Pmail, calendar = AppointDate)
        appointment_list.save()

        # SEND EMAIL
        email_sender = 'sa3518548@gmail.com'
        email_password = 'pziggqxkwggxtopt'

        email_receiver = Pmail
        subject = "hello "+Pname+"! check your appointment status."
        body = "Hi "+ Pname+ " your appointment is booked.\nthanking you team malloc to visit our doctor appointment system.\nDoctor name: "+docName +"\nDepartment: "+depName+"\nappointment date: "+AppointDate

        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['subject'] = subject
        em.set_content(body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465,context=context) as smtp:
            smtp.login(email_sender,email_password)
            smtp.sendmail(email_sender,email_receiver,em.as_string())

        messages.success(request,"Your Appointment is booked, we send a mail on your mail address. Please check it out and Thank you!")


    return render(request,'index.html',{'doc':NearBy_Doctor.objects.all(), 'dep':departments.objects.all()})
    # return HttpResponse('this is home page')



def payment(request):
    if request.method == "POST":
        depName = request.POST.get("sedep")
        Pname = request.POST.get("name")
        Pmail = request.POST.get("mail")
        docName = request.POST.get("sedoc")
        Pphone = request.POST.get("phone")
        AppointDate = request.POST.get("date")

        appointment_list = Appointment_List(se_dept = depName, se_doc = docName, patient_name = Pname, patient_phone = Pphone, patient_email = Pmail, calendar = AppointDate)
        appointment_list.save()


    return render(request, 'payment.html',{'app':Appointment_List.objects.all()})


def about(request):
    fn = User.first_name
    return render(request,'about.html',{'fname':fn})

def services(request):
    return render(request,'services.html')
    # return HttpResponse('this is services page')

def signUp(request):
    if request.method == "POST":
        uname = request.POST.get("username")
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        fpass = request.POST.get("pass1")
        cpass = request.POST.get("pass2")
        

        # validation for user
        if User.objects.filter(username=uname):
            messages.error(request,"Username already exist!")
            return redirect('signUp')

        if User.objects.filter(email=email):
            messages.error(request,"email already registerd")
            return redirect('signUp')

        if len(uname) >10:
            messages.error(request,"the username must be under 10 character!")
            return redirect('signUp')

        if fpass != cpass:
            messages.error(request,"Passwords didn't match.Try agian!")
            return redirect('signUp')

        if not uname.isalnum():
            messages.error(request,"Username must be alpha-numeric!")
            return redirect('signUp')


        
        


        my_user = User.objects.create_user(uname,email,fpass)
        my_user.first_name = fname
        my_user.last_name = lname

        my_user.save()

        messages.success(request, 'Thank you! your account has been successfully created.')

        return redirect('login')

        

        # regusers = RegUsers(UserName=uname, Fname=fname, Lname=lname, Email=email, Password=fpass, CPassword=cpass, Date=datetime.today())
        # regusers.save()
        # confirmation message

        # return redirect('login')
    
    return render(request,'signUp.html')

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("pass1")
        doc_pat = request.POST.get("doc_pat")

        user = authenticate(request, username = username, password = password)
        if user is not None:
            authlogin(request, user)
            fname = user.first_name
            messages.success(request,'Thank You! Your are successfully logged in. Now you can create your desired account.')
            doc='Doctor'
            pat='Patient'

            if doc == doc_pat:
                return render(request, 'doctorAcc.html', {'fname':fname})
            else:
                return render(request, 'patientAcc.html', {'fname':fname})
            
        
        else:
            messages.error(request, 'Bad request! Username or Password did not match. Try aging.')
            return redirect('login')


    return render(request,'login.html')

def signout(request):
    logout(request)
    messages.success(request,'Logged out successfully!')
    return redirect('home')

def patientAcc(request):
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formOne':
            pat_image = request.POST.get("pat_image")
            if len(request.FILES) !=0:
                pat_image= request.FILES['pat_image']
            
            pat_name = request.POST.get("pat_name")
            pat_age = request.POST.get("pat_age")
            pat_location = request.POST.get("pat_location")
            pat_lag_spoken = request.POST.get("pat_lag_spoken")
            pat_occu = request.POST.get("pat_occu")
            


            # pat_name = user.first_name
            pat_obj = patient(pat_image = pat_image, pat_name = pat_name, pat_age=pat_age,pat_location = pat_location,pat_lag_spoken = pat_lag_spoken,
            pat_occu = pat_occu)
            pat_obj.save()
        
            return render (request,'patientAcc.html',{'pat_image':pat_image,'pat_name':pat_name,'pat_age':pat_age,'pat_location':pat_location,'pat_lag_spoken':pat_lag_spoken,'pat_occu':pat_occu})
        elif request.POST.get("form_type") == 'formTwo':
            blood = request.POST.get("blood")
            bllod_2 = request.POST.get("bllod_2")
            suger_lvl = request.POST.get("suger_lvl")
            dat=datetime.today()

            pat_health = health(blood=blood,bllod_2=bllod_2,suger_lvl=suger_lvl,date=dat)

            if int(blood) > 120 and int(bllod_2) > 80:
                condition='High BP!!';
            elif int(blood) < 120 and int(bllod_2) < 80:
                condition='low BP!!';
            elif int(blood) > 120 and int(bllod_2) < 80 or int(blood) < 120 and int(bllod_2) > 80:
                condition='Critical conditio';
                
            

            
            pat_health.save()
            return TemplateResponse (request,'patientAcc.html',{'blood':blood,'bllod_2':bllod_2,'suger_lvl':suger_lvl, 'condition':condition})

        
    return render (request,'patientAcc.html')
    # fname = user.first_name
    
    # print(user)
        
    

    


# for doctor account
def doctorAcc(request):
    # doctor = NearBy_Doctor.objects.get(pk=doctor_id)
    # patient = patient.objects.get(pk=request.user.id)
    if request.method == 'POST':
        doc_image = request.POST.get("doc_image")
        if len(request.FILES) !=0:
            doc_image= request.FILES['doc_image']
        doctor_name = request.POST.get("doctor_name")
        department = request.POST.get("department")
        location = request.POST.get("location")
        working_H = request.POST.get("working_H")
        brife = request.POST.get("brife")
        clinicloc = request.POST.get("clinicloc")
        nw_pat_fee = request.POST.get("nw_pat_fee")
        ret_pat_fee = request.POST.get("ret_pat_fee")
        repo_fee = request.POST.get("repo_fee")
        lag_spoken = request.POST.get("lag_spoken")
        sunday_mor = request.POST.get("sunday_mor")
        sunday_ev = request.POST.get("sunday_ev")
        monday_mor = request.POST.get("monday_mor")
        monday_ev = request.POST.get("monday_ev")
        tuesday_mor = request.POST.get("tuesday_mor")
        tuesday_ev = request.POST.get("tuesday_ev")
        wedday_mor = request.POST.get("wedday_mor")
        wedday_ev = request.POST.get("wedday_ev")
        thursday_mor = request.POST.get("thursday_mor")
        thursday_ev = request.POST.get("thursday_ev")
        frday_mor = request.POST.get("frday_mor")
        frday_ev = request.POST.get("frday_ev")
        satday_mor = request.POST.get("satday_mor")
        satday_ev = request.POST.get("satday_ev")
        
        doc_obj = NearBy_Doctor(doc_image = doc_image,
        doctor_name = doctor_name, department=department,location = location,working_H = working_H,
            brife = brife,clinicloc = clinicloc,nw_pat_fee = nw_pat_fee,ret_pat_fee = ret_pat_fee,repo_fee = repo_fee,lag_spoken = lag_spoken,sunday_mor = sunday_mor,sunday_ev = sunday_ev,monday_mor = monday_mor,monday_ev = monday_ev,tuesday_mor = tuesday_mor,tuesday_ev = tuesday_ev,wedday_mor = wedday_mor,wedday_ev = wedday_ev,thursday_mor = thursday_mor,thursday_ev = thursday_ev,frday_mor = frday_mor,frday_ev = frday_ev,satday_mor = satday_mor,satday_ev = satday_ev)
        doc_obj.save()

        

        return TemplateResponse (request,'doctorAcc.html',{'doc_image':doc_image,'doctor_name':doctor_name,'department':department, 'location':location,'working_H':working_H,'brife':brife,'clinicloc':clinicloc,'nw_pat_fee':nw_pat_fee,'ret_pat_fee':ret_pat_fee,'repo_fee':repo_fee,'lag_spoken':lag_spoken,'sunday_mor':sunday_mor,'sunday_ev':sunday_ev,'monday_mor':monday_mor,'monday_ev':monday_ev,'tuesday_mor':tuesday_mor,'tuesday_ev':tuesday_ev,'wedday_mor':wedday_mor,'wedday_ev':wedday_ev,'thursday_mor':thursday_mor,'thursday_ev':thursday_ev,'frday_mor':frday_mor,'frday_ev':frday_ev,'satday_mor':satday_mor,'satday_ev':satday_ev})

    
    return render(request,'doctorAcc.html', {'patients': patient.objects.all()})

# for NearByDoc
def NearByDoc(request):
    nr = None
    if request.method == "POST":
        nearby = request.POST.get("NearBy")
        nr = nearby
    return render(request,'nearbyDoc.html',{'nrb':NearBy_Doctor.objects.all(),'near':nr})
    
#for Emergency Doctor
def emDoc(request):
    wkh = "Emergency doc"

    return render(request,'emDoc.html',{'em':NearBy_Doctor.objects.all(),'wkh':wkh})

def contact(request):
    
    return render(request, 'contact.html')
    # return HttpResponse('this is contact page')

def base(request):
    
    return render(request,'base.html')

def review(request):
    if request.method == "POST":
        na = request.POST.get("name")
        revi = request.POST.get("rev")
        dat=datetime.today()
        RE = reviewers(name=na,reviews=revi,time=dat)
        RE.save()
        return TemplateResponse(request, 'index.html', {"re":reviewers.objects.all()})
    return render(request,'review.html',)

def rateing(request):
    obj = rating.objects.filter(score=0).order_by("?").first()
    context={
        "obj" : obj,
    }

    return render(request,'rateing.html',context)

        

def submit_review(request):
    # from .models import patient
    url = request.META.get('HTTP_REFERER') #its collect curent url
    if request.method == 'POST':
        patient_id = request.POST['patt']
        # print(patient_id)    
        # patient = patient.objects.get(pk=patient_id)
        try:
            # Get the patient object using the 'pat' field in the request's POST data
            # patient = patient.objects.get(pk=request.POST['pat'])
            # Get the existing review object using the patient and doctor id
            reviews = ReviewRating.objects.get( doc__id=doctor_id)
            
            # Update the review object
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            # Create a new review object if it does not exist
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.doc_id = doctor_id
                # Use the patient object that we obtained earlier
                data.pat = patient_id
                doctor = NearBy_Doctor.objects.get(pk=doctor_id)
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)


# from django.shortcuts import render, HttpResponse, redirect
# from datetime import datetime
# from home.models import NearBy_Doctor, Appointment_List, departments
# from django.contrib import messages
# # from home.models import Faq
# from .forms import FAQForm
# from .forms import AnswerForm
# from django.shortcuts import get_object_or_404

# # for patient list
# from .models import PatientList
# from .models import patient
# from .models import departments
# from .models import NearBy_Doctor


# # for user authticcation 
# from django.contrib.auth.models import User
# from django.contrib.auth import authenticate,login as authlogin,logout
# # email
# # from MrDoc import settings
# # from django.core.mail import send_mail
# from email.message import EmailMessage
# import ssl
# import smtplib



# # Create your views here.
# def home(request):
#     # this form is accessing for taking appointment list from home page
#     if request.method == "POST":
#         depName = request.POST.get("sedep")
#         Pname = request.POST.get("name")
#         Pmail = request.POST.get("mail")
#         docName = request.POST.get("sedoc")
#         Pphone = request.POST.get("phone")
#         AppointDate = request.POST.get("date")

#         appointment_list = Appointment_List(se_dept = depName, se_doc = docName, patient_name = Pname, patient_phone = Pphone, patient_email = Pmail, calendar = AppointDate)
#         appointment_list.save()

#         # SEND EMAIL
#         email_sender = 'sa3518548@gmail.com'
#         email_password = 'pziggqxkwggxtopt'

#         email_receiver = Pmail
#         subject = "hello "+Pname+"! check your appointment status."
#         body = "Hi "+ Pname+ " your appointment is booked.\nthanking you team malloc to visit our doctor appointment system.\nDoctor name: "+docName +"\nDepartment: "+depName+"\nappointment date: "+AppointDate

            

            
            
        
#         em = EmailMessage()
#         em['From'] = email_sender
#         em['To'] = email_receiver
#         em['subject'] = subject
#         em.set_content(body)

#         context = ssl.create_default_context()

#         with smtplib.SMTP_SSL('smtp.gmail.com', 465,context=context) as smtp:
#             smtp.login(email_sender,email_password)
#             smtp.sendmail(email_sender,email_receiver,em.as_string())





#         messages.success(request,"Your Appointment is booked, we send a mail on your mail address. Please check it out and Thank you!")


#     return render(request,'index.html',{'doc':NearBy_Doctor.objects.all(), 'dep':departments.objects.all()})
#     # return HttpResponse('this is home page')


# def about(request):
#     fn = User.first_name
#     return render(request,'about.html',{'fname':fn})

# def services(request):
#     return render(request,'services.html')
#     # return HttpResponse('this is services page')

# def signUp(request):
#     if request.method == "POST":
#         uname = request.POST.get("username")
#         fname = request.POST.get("fname")
#         lname = request.POST.get("lname")
#         email = request.POST.get("email")
#         fpass = request.POST.get("pass1")
#         cpass = request.POST.get("pass2")
        

#         # validation for user
#         if User.objects.filter(username=uname):
#             messages.error(request,"Username already exist!")
#             return redirect('signUp')

#         if User.objects.filter(email=email):
#             messages.error(request,"email already registerd")
#             return redirect('signUp')

#         if len(uname) >10:
#             messages.error(request,"the username must be under 10 character!")
#             return redirect('signUp')

#         if fpass != cpass:
#             messages.error(request,"Passwords didn't match.Try agian!")
#             return redirect('signUp')

#         if not uname.isalnum():
#             messages.error(request,"Username must be alpha-numeric!")
#             return redirect('signUp')


        
        


#         my_user = User.objects.create_user(uname,email,fpass)
#         my_user.first_name = fname
#         my_user.last_name = lname

#         my_user.save()

#         messages.success(request, 'Thank you! your account has been successfully created.')

#         return redirect('login')

        

#         # regusers = RegUsers(UserName=uname, Fname=fname, Lname=lname, Email=email, Password=fpass, CPassword=cpass, Date=datetime.today())
#         # regusers.save()
#         # confirmation message

#         # return redirect('login')
    
#     return render(request,'signUp.html')

# def login(request):
#     if request.method == "POST":
#         username = request.POST.get("username")
#         password = request.POST.get("pass1")
#         doc_pat = request.POST.get("doc_pat")

#         user = authenticate(request, username = username, password = password)
#         if user is not None:
#             authlogin(request, user)
#             fname = user.first_name
#             messages.success(request,'Thank You! Your are successfully logged in. Now you can create your desired account.')
#             doc='Doctor'
#             pat='Patient'

#             if doc == doc_pat:
#                 return render(request, 'doctorAcc.html', {'fname':fname})
#             else:
#                 return render(request, 'patientAcc.html', {'fname':fname})
            
        
#         else:
#             messages.error(request, 'Bad request! Username or Password did not match. Try aging.')
#             return redirect('login')


#     return render(request,'login.html')

# def signout(request):
#     logout(request)
#     messages.success(request,'Logged out successfully!')
#     return redirect('home')

# def patientAcc(request):
#     if request.method == 'POST':
#         if request.POST.get("form_type") == 'formOne':
#             pat_image = request.POST.get("pat_image")
#             if len(request.FILES) !=0:
#                 pat_image= request.FILES['pat_image']
            
#             pat_name = request.POST.get("pat_name")
#             pat_age = request.POST.get("pat_age")
#             pat_location = request.POST.get("pat_location")
#             pat_lag_spoken = request.POST.get("pat_lag_spoken")
#             pat_occu = request.POST.get("pat_occu")
            


#             # pat_name = user.first_name
#             pat_obj = patient(pat_image = pat_image, pat_name = pat_name, pat_age=pat_age,pat_location = pat_location,pat_lag_spoken = pat_lag_spoken,
#             pat_occu = pat_occu)
#             pat_obj.save()
        
#             return render (request,'patientAcc.html',{'pat_image':pat_image,'pat_name':pat_name,'pat_age':pat_age,'pat_location':pat_location,'pat_lag_spoken':pat_lag_spoken,'pat_occu':pat_occu})
#         elif request.POST.get("form_type") == 'formTwo':
#             blood = request.POST.get("blood")
#             bllod_2 = request.POST.get("bllod_2")
#             suger_lvl = request.POST.get("suger_lvl")
#             dat=datetime.today()

#             pat_health = health(blood=blood,bllod_2=bllod_2,suger_lvl=suger_lvl,date=dat)

#             if int(blood) > 120 and int(bllod_2) > 80:
#                 condition='High BP!!';
#             elif int(blood) < 120 and int(bllod_2) < 80:
#                 condition='low BP!!';
#             elif int(blood) > 120 and int(bllod_2) < 80 or int(blood) < 120 and int(bllod_2) > 80:
#                 condition='Critical conditio';
                
            

            
#             pat_health.save()
#             return TemplateResponse (request,'patientAcc.html',{'blood':blood,'bllod_2':bllod_2,'suger_lvl':suger_lvl, 'condition':condition})

        
#     return render (request,'patientAcc.html')
#     # fname = user.first_name
    
#     # print(user)
        
    

    


# # for doctor account
# def doctorAcc(request):
#     return render(request,'doctorAcc.html', {'patients': patient.objects.all()})

# # for NearByDoc
# def NearByDoc(request):
#     nr = None
#     if request.method == "POST":
#         nearby = request.POST.get("NearBy")
#         nr = nearby
#     return render(request,'nearbyDoc.html',{'nrb':NearBy_Doctor.objects.all(),'near':nr})
    
# #for Emergency Doctor
# def emDoc(request):
#     wkh = "Emergency doc"

#     return render(request,'emDoc.html',{'em':NearBy_Doctor.objects.all(),'wkh':wkh})

# def contact(request):
    
#     return render(request, 'contact.html')
#     # return HttpResponse('this is contact page')

# def base(request):
    
#     return render(request,'base.html')

# def review(request):
#     if request.method == "POST":
#         na = request.POST.get("name")
#         revi = request.POST.get("rev")
#         dat=datetime.today()
#         RE = reviewers(name=na,reviews=revi,time=dat)
#         RE.save()
#         return TemplateResponse(request, 'index.html', {"re":reviewers.objects.all()})
#     return render(request,'review.html',)

# def rateing(request):
#     obj = rating.objects.filter(score=0).order_by("?").first()
#     context={
#         "obj" : obj,
#     }

#     return render(request,'rateing.html',context)

        

#--- FAQ Section for user ----#
def faq(request):
    # # faqs = Faq.objects.get(id=1)
    # context = {'faqs': faqs}
    
    # # print(Faq.question)
    # # print(Faq.answer)
    # return render(request, 'faq.html', context)
    fn = User.first_name
    return render(request,'faq.html',{'fname':fn})
    
    
from django.shortcuts import render
from .models import FAQ

def faq_view(request):
    faqs = FAQ.objects.all()
    return render(request, 'faq.html', {'faqs': faqs})

def submit_question(request):
    if request.method == 'POST':
        form = FAQForm(request.POST)
        if form.is_valid():
            question = form.cleaned_data['question']
            faq = FAQ(question=question)
            faq.save()
            return redirect('faq')
    else:
        form = FAQForm()
    return render(request, 'faq.html', {'form': form})

# FAQ for admin response
def admin_view(request):
    faqs = FAQ.objects.all()
    return render(request, 'admin.html', {'faqs': faqs})

def answer_question(request, pk):
    # faq = get_object_or_404(FAQ, pk=pk)
    # if request.method == 'POST':
    #     form = AnswerForm(request.POST)
    #     if form.is_valid():
    #         answer  = form.cleaned_data['answer']
    #         faq.answer = answer
    #         faq.save()
    #         return redirect('admin')
    # else:
    #     form = AnswerForm()
    faq = get_object_or_404(FAQ, pk=pk)
    if request.user.is_superuser or request.user == faq.user:
        if request.method == 'POST':
            form = AnswerForm(request.POST)
            if form.is_valid():
                answer = form.cleaned_
    return render(request, 'admin.html', {'form': form})



def delete_question(request, pk):
    faq = get_object_or_404(FAQ, pk=pk)
    faq.deleted = True
    faq.save()
    return redirect('admin')

def delete_question(request, pk):
    faq = get_object_or_404(FAQ, pk=pk)
    faq.deleted = True
    faq.save()
    return redirect('admin')

# Department Doctors List
def docDept(request):
    department_name = 'Ophthalmologists'
    doctors = NearBy_Doctor.objects.filter(department=department_name)
    
   # Psychiatry = 'Psychiatry'
   # Psychiatry_doctors = NearBy_Doctor.objects.filter(department=Psychiatry)
    
    context = {
        'doctors': doctors
    }
    # context2 = {
    #     'doctors': Psychiatry_doctors
    # }
    
    return render(request, 'doctorDepartments.html', context)
   # return render(request,'doctorDepartments.html')

def Ophthalmologists(request):
    department_name = 'Ophthalmologists'
    doctors = NearBy_Doctor.objects.filter(department=department_name)
    
    context = {
        'doctors': doctors
    }
    return render(request, 'DoctorProfile/Ophthalmologists.html', context)


def Endocrinologists(request):
    department_name = 'Endocrinologists'
    doctors = NearBy_Doctor.objects.filter(department=department_name)
    
    context = {
        'doctors': doctors
    }
    return render(request, 'DoctorProfile/Endocrinologist.html', context)

def Gastroenterologists(request):
    department_name = 'Gastroenterologists'
    doctors = NearBy_Doctor.objects.filter(department=department_name)
    
    context = {
        'doctors': doctors
    }
    return render(request, 'DoctorProfile/Gastroenterologists.html', context)

def Cardiologists(request):
    department_name = 'Cardiologists'
    doctors = NearBy_Doctor.objects.filter(department=department_name)
    
    context = {
        'doctors': doctors
    }
    return render(request, 'DoctorProfile/Cardiologists.html', context)

def Psychiatry(request):
    department_name = 'Psychiatry'
    doctors = NearBy_Doctor.objects.filter(department=department_name)
    
    context = {
        'doctors': doctors
    }
    return render(request, 'DoctorProfile/Psychiatry.html', context)

def Orthopedics(request):
    department_name = 'Orthopedics'
    doctors = NearBy_Doctor.objects.filter(department=department_name)
    
    context = {
        'doctors': doctors
    }
    return render(request, 'DoctorProfile/Orthopedics.html', context)


def Pediatrics(request):
    department_name = 'Pediatrics'
    doctors = NearBy_Doctor.objects.filter(department=department_name)
    
    context = {
        'doctors': doctors
    }

    return render(request, 'DoctorProfile/Pediatrics.html', context)


    return render(request, 'DoctorProfile/Pediatrics.html', context)

