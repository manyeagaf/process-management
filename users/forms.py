from django import forms
from .models import UserPrivilege,User
from django.contrib.auth.forms import UserCreationForm

class LoginForm(forms.Form):
    email = forms.CharField(max_length=50, label="Email")
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        self.email = self.cleaned_data['email']
        if not(User.objects.filter(email=self.email).exists()):
            raise forms.ValidationError("Account with this user name does not exist")
        if not(User.objects.get(email=self.email).is_active):
            raise forms.ValidationError("Account with this user name is inactive contact us to get your account activated")
        return self.email
    def clean_password(self):
        # email = self.email
        # password = self.cleaned_data['password']
        try:
            if User.objects.filter(email=self.cleaned_data['email']).exists():
                if not(User.objects.get(email=self.cleaned_data['email']).check_password(self.cleaned_data['password'])):

                    raise forms.ValidationError(f"The password for {email} account is invalid")
        except:

            forms.ValidationError("The user does not exist")
        return self.cleaned_data['password']


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    
    class Meta:
        model = User
        fields =('staff_id','email','first_name','last_name','user_type','branch','role','password1','password2')
    
    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_active = False
        if commit:
            user.save()
        return user
    # def clean_password2(self):
    #     cd = self.cleaned_data
    #     if cd['password'] != cd['password2']:
    #         raise forms.ValidationError('Passwords don\'t match.')
    #     return cd['password2']

class PrivilegeForm(forms.ModelForm):
    
    class Meta:
        model = UserPrivilege
        fields = ('user','privilege')



