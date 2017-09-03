from django import forms
from django.contrib.auth.models import User
from .models import Profile
from io import TextIOWrapper
import csv
from django.conf import settings

class RegisterForm(forms.Form):
    username=forms.CharField(max_length=100,error_messages={'required': 'This field required!'})
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    email=forms.EmailField(max_length=100,error_messages={'required': 'This field required!'})

    number = forms.RegexField(regex=r'^\+?1?\d{10}$', 
                                error_message = ("Please enter valid mobile number."))
    branch_choices= [
    ('ece', 'ECE'),
    ('cse', 'CSE'),
    ('eee', 'EEE'),
    ('mech', 'MECH'),
    ('civil', 'CIVIL')
    ]
    branch= forms.CharField(label='select your branch?',widget=forms.Select(choices=branch_choices))

    year_choices= [
    ('first', 'First'),
    ('second', 'Second'),
    ('third', 'Third'),
    ('final', 'Final')
    ]

    year= forms.CharField(label='select your year?',widget=forms.Select(choices=year_choices))
    #   . bimage       = forms.ImageField()
    image = forms.ImageField()
    def clean_username(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        if username and Profile.objects.filter(username=username).exclude(email=email).count():
            raise forms.ValidationError("user already registerd")
            return username
    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and Profile.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError(u'Email addresses must be unique.')
            return email

    def clean(self):
        password1 =self.cleaned_data.get('password1')
        password2 =self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            self._errors['password2'] = self.error_class(['passwords did not match.'])
            del self.cleaned_data['password2']
        return password1

class LoginForm(forms.Form):
    password =forms.CharField(widget=forms.PasswordInput)
    username = forms.CharField(required=True)
    def clean(self):
        username=self.cleaned_data.get('username')
        password=self.cleaned_data.get('password')
        if not Profile.objects.filter(username=username):
            raise forms.ValidationError(u'Please enter correct user details.')
            return username


class ChangePasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput)
    reenter_password = forms.CharField(widget=forms.PasswordInput)
    def clean(self):
        new_password =self.cleaned_data.get('new_password')
        reenter_password =self.cleaned_data.get('reenter_password')

        if new_password and reenter_password and new_password != reenter_password:
            self._errors['reenter_password'] = self.error_class(['passwords did not match.'])
            del self.cleaned_data['reenter_password']
        return new_password


class ForgetPasswordForm(forms.Form):
    email=forms.EmailField(max_length=100,error_messages={'required': 'This field required!'})
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not Profile.objects.filter(email=email):
            raise forms.ValidationError(u'Please enter correct email.')
            return email

class CreateExamForm(forms.Form):
    exam_name=forms.CharField(max_length=100,error_messages={'required': 'This field required!'})
    date = forms.DateField(label=u'date', input_formats=['%d-%m-%Y'], required=False, widget=forms.DateInput(format = '%d-%m-%Y'),error_messages={'required': 'This field required!'})
    # date=forms.DateField(input_formats=settings.DATE_INPUT_FORMATS)
    duration=forms.DurationField(error_messages={'required': 'This field required!'})
    branch_choices= [
    ('ece', 'ECE'),
    ('cse', 'CSE'),
    ('eee', 'EEE'),
    ('mech', 'MECH'),
    ('civil', 'CIVIL')
    ]


    branch= forms.CharField(label='select your branch?',widget=forms.Select(choices=branch_choices))
    # uploadFile = forms.FileField(widget=forms.FileInput(attrs={'accept': ".csv"}))

    def validate_file_extension(value):
            if not value.name.endswith('.csv'):
                raise forms.ValidationError("Only CSV file is accepted")
    uploadFile = forms.FileField(label='Select a file',validators=[validate_file_extension])

    def clean(self):
        uploadFile =self.cleaned_data.get('uploadFile')
        # print (uploadFile)
        if uploadFile:
            with open('f', 'wb+') as destination:
                for chunk in uploadFile.chunks():
                    chunk=chunk.decode("utf-8") 
                    exam_data=['answer','option_1','option_2','option_3','option_4','question']
                    # print (exam_data)
                    data=chunk.split('\n')
                   
                    header_data    = data[0].split(',')
                    # print (header_data)
                    if not set(exam_data)==set(header_data):
                        raise forms.ValidationError("enter valied fields")
                    # else:
                    #     print ('mop')
                        
                    # # print (csv_header)
                    # # for i in data:
                    # # #     print(i)
                    # # destination.write(chunk)
                    # # # print (destination)
                    # # destination.close()


class ExamFrom(forms.Form):
    question=forms.CharField()
    option_1=forms.CharField()
    option_2=forms.CharField()
    option_3=forms.CharField()
    option_4=forms.CharField()
    answer=forms.CharField()

