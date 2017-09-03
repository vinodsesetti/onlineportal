from django.shortcuts import render
from .forms import RegisterForm,LoginForm,ChangePasswordForm,ForgetPasswordForm,CreateExamForm
from django.contrib.auth.hashers import make_password
from .models import *
from django.contrib.auth import login as auth_login
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
import uuid 
from django.core.mail import EmailMessage
from dateutil.parser import parse
from django.shortcuts import get_object_or_404

# Create your views here.
def Index(request):
    return render(request,"index.html")
def Signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            image=request.FILES.get('image')
            username=request.POST.get("username")
            email=request.POST.get("email")
            password=request.POST.get("password1")
            number=request.POST.get("number")
            branch=request.POST.get("branch")
            year=request.POST.get("year")
            profile=Profile.objects.create(username=username,image=image,email=email,number=number,branch=branch,year=year)         
            profile.password = make_password(password=password,
                                  salt=None,
                                  hasher='unsalted_md5')
            profile.save()
            return HttpResponseRedirect('/signin')
    else:
        form = RegisterForm()
    return render(request,"signup.html", {'form': form})
def Login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            #print  '*************'
            #print  user
            if user:
                auth_login(request, user)
                return HttpResponseRedirect('/Profile')
    else:
        form=LoginForm()

    return render(request,"login.html",{'form':form})
import csv  
@login_required
def CreateExam(request):
    if request.method=='POST':
        form=CreateExamForm(request.POST, request.FILES)
        # #print  (form)
        if form.is_valid():
            file=request.FILES.get('uploadFile')
            exam_name=request.POST.get('exam_name')
            date=request.POST.get('date')
            date=parse(date)
            date=date.strftime('%Y-%m-%d')
            duration=request.POST.get('duration')
            # #print  (duration)
            # #print  (type(duration))
            branch=request.POST.get('branch')
            exam=Exam.objects.create(exam_name=exam_name,duration=timedelta(minutes=int(duration)),date_published=date,branch=branch)
            exam.save()
            with open('f', 'wb+') as destination:
                for chunk in file.chunks():
                    chunk=chunk.decode("utf-8") 
                    data=chunk.split('\n')
                    for i in data[1:]:
                        info=i.split(',')
                        question=Question.objects.create(question_text=info[0],option1=info[1],option2=info[2],option3=info[3],option4=info[4],answer=info[5],exam_id=exam.id)
                        question.save()
            return HttpResponseRedirect('/')

    else:
        form=CreateExamForm()
    return render(request,"createexam.html",{'form':form})

@login_required
def Exams(request):
    return render(request,"exams.html")

@login_required
def signout(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required
def change_password(request):
    if request.method=='POST':
        form=ChangePasswordForm(request.POST)
        if form.is_valid():
            new_pass=request.POST['new_password']
            reenter_pwd=request.POST['reenter_password']
            user=Profile.objects.get(username=request.user.username)
            user.set_password(new_pass)
            user.save()
            update_session_auth_hash(request, request.user)
            return HttpResponseRedirect('/')
    else:
        form=ChangePasswordForm()
    return render(request,"change_password.html",{'form':form})


def forget_password(request):
    if request.method=='POST':
        form=ForgetPasswordForm(request.POST)
        if form.is_valid():
            email=request.POST['email']
            user=Profile.objects.get(email=email)
            if user:
                random=uuid.uuid4().hex[:7].upper()
                # #print  (random)
                user.set_password(random)
                user.save()
                username=user.username
                body="this email gives information about user details .if you want to change password ,you can change with below password. 'username:%s,password:%s'"%(username,random)
                # #print  (body)
                Subject="Your Login details"
                email_send = EmailMessage(Subject,body,to=[email])
                email_send.send()
                return HttpResponseRedirect('/signin')



    else:
        form=ForgetPasswordForm()

    return render(request,"forget_password.html",{'form':form})

def profile(request):
    # #print  (request.user.id)
    user=Profile.objects.get(id=request.user.id)
    # #print  (user)
    return render(request,"profile.html",{"user":user})

def exams_list(request):
    exam_list = Exam.objects.all().order_by('date_published')
    # #print  (exam_list)
    return render(request,"exams.html",{"exam_list":exam_list})

def exam_detail(request, exam_id):
    exam_id=exam_id
    exam=Question.objects.filter(exam=exam_id).order_by('?')
    exam_info=Exam.objects.get(pk=exam_id)
    exam_name = exam_info.exam_name
    duration = str(exam_info.duration).split(":")
    total_min=(duration[0]*60)+duration[1]
    sec = duration[2]
    # #print  (exam)    
    return render(request, 'questionpaper.html', {'exam': exam,
        'name':exam_name,'exmid':exam_id,'duration':duration,
        "total_min":total_min,"sec":sec
        })

def submits(request, exam_id):
    #print  request.user.username
    #print  request.user.branch
    #print  request.user.year

    exam = get_object_or_404(Exam, pk=exam_id)
    score = 0
    count = exam.question_set.count()
    questions=exam.question_set.all()
    questions_data=[]
    for question in questions:
        if request.POST.get(str(question.pk)):
            # #print  (request.POST.get(str(questions.pk)))
            response = request.POST.get(str(question.pk))
            if response:
                #print  (response,"questions")
                # #print  (str(questions),"answer")
                if str(question.answer) == str(response):
                    score += 1
                #print  (question.question_text)
                questions_data.append({'question':question,'choice':response})
        else:
            #print  ("no options")
            questions_data.append({'question':question,'choice':"you did not provide any option "})
            # your_choice.update({question.id:response})
    # #print  (questions_data)

    # #print  (score)
    Report.objects.create(user=request.user, exam=exam, marks=score)
    Results.objects.create(name=request.user.username,marks=score,year=request.user.year,branch=request.user.branch)
    # #print  ("LLLLLLLLLLLl")
    return render(request, 'submit.html', {'score': score, 'count': count,'questions_data':questions_data})

