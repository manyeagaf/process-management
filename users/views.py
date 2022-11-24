from curses.ascii import HT
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import permission_required, login_required
from users.models import User,Privilege,UserPrivilege
from .forms import LoginForm,PrivilegeForm, UserRegistrationForm
from django.core.mail import send_mail
from django.contrib import messages

def user_login(request):
    if request.method == 'POST':
        # print('Ok')
        # print(request.POST.get('username'))
        # print(request.POST.get('password')) 
        # email = request.POST.get('email')
        # password = request.POST.get('password')
        # user = user = authenticate(request,
        #                         email=email,
        #                         password=password,
        #                         )
        # login(request,user)
        # return redirect('/')
        form = LoginForm(request.POST)
        if form.is_valid():
            
            cd = form.cleaned_data
            user = authenticate(request,
                                email=cd['email'],
                                password=cd['password']
                                )
            
            if user is not None:
                if user.is_active:
                    print('Active')
                    login(request, user)
                    return redirect('/')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse("Invalid User")   
    else:
        if request.user.is_authenticated:
            return redirect("/")
        form = LoginForm()
        return render(request, 'users/login.html', {'form': form})


@login_required
def user_logout(request):
    
    logout(request)
    return redirect('/accounts/login/')

    
@login_required
def dashboard(request):
    user = request.user
    if user.get_user_type_display() == 'admin':
        return redirect('/admin')
    elif user.get_user_type_display() == 'officer':
        return redirect('/officer')
    elif user.get_user_type_display() == 'branch':
        return redirect('/branch')
    else:
        return redirect('/access-control')
  
@login_required
def create_user(request):
    user = request.user
    form = UserRegistrationForm(request.POST)
    if form.is_valid():
        
        new_user = form.save(commit = False)
        new_user.set_password(form.cleaned_data['password1'])
        if user.get_user_type_display() == 'access control admin':
            new_user.is_active = True
        new_user.save()
        if new_user.is_active:

            messages.success(request,"Account with name {} was successfully created".format(new_user),)
        else:
            messages.success(request,"Account with name {} created successfully. Wait for admin approval".format(new_user))
        return redirect('/')
        
    else:
        messages.error(request,form.errors)
        return redirect('/')
       
        
    

@login_required
def activate_user(request,pk):
    user_to_activate = User.objects.get(id = pk)
    user_to_activate.is_active = True
    user_to_activate.is_delete_requested = False
    user_to_activate.save()
    messages.success(request,"Account with name {} was activated successfully".format(user_to_activate),)
    return redirect('/')

@login_required
def request_user_delete(request,pk):
    user_to_delete = User.objects.get(id = pk)
    print(user_to_delete)
    user_to_delete.is_delete_requested = True
    user_to_delete.is_active = False
    user_to_delete.save()
    messages.success(request,"Delete was requested for account with name {}.Wait for admin approval".format(user_to_delete))
    return redirect('/')

@login_required
def delete_user(request,pk):
    user = request.user 
    if user.get_user_type_display() == 'access control admin':
        user_to_delete = User.objects.get(id = pk)
        user_to_delete.delete()
        messages.success(request,"Account with name {} was successfully deleted".format(user_to_delete),)
        return redirect('/')
    else:
        user_to_delete = User.objects.get(id = pk)
        print(user_to_delete)
        user_to_delete.is_delete_requested = True
        user_to_delete.is_active = False
        user_to_delete.save()
        messages.success(request,"Delete was requested for account with name {}.Wait for admin approval".format(user_to_delete))
        return redirect('/')


#Get admin privileges
def get_admin_user_privilege(user):
    try:
        admin_user_privileges = Privilege.objects.get(slug = 'admin-privileges')
        admin_privilege = UserPrivilege.objects.get(user = user,privilege = admin_user_privileges,is_active = True)
    except:
        admin_privilege = None
    return admin_privilege

#Get branch user privileges
def get_officer_user_privilege(user):
    try:
        officer_user_privileges = Privilege.objects.get(slug = 'officer-privileges')
        officer_privilege = UserPrivilege.objects.get(user = user,privilege = officer_user_privileges,is_active = True)
    except:
        officer_privilege = None
    return officer_privilege

#Get officer user privileges
def get_branch_user_privilege(user):
    try:
        branch_user_privileges = Privilege.objects.get(slug = 'branch-user-privileges')
        branch_privilege = UserPrivilege.objects.get(user = user,privilege = branch_user_privileges,is_active = True)
    except:
        branch_privilege = None
    return branch_privilege

#Privilege Views
@login_required
def create_user_privilege(request):
    user = request.user
    privilege = request.POST.get('privilege')
    form = PrivilegeForm(request.POST)
    if form.is_valid():
        privilege = form.save(commit = False)
        privilege.created_by = user
        privilege.save()

    if user.get_user_type_display() == 'access control admin':
        privilege.is_active = True
        privilege.approved_by = user
        privilege.save()
    if privilege.is_active:
        messages.success(request,"Privilege {} was successfully assigned to {}".format(privilege.id,privilege.user),)
    else:
        messages.success(request,"Privilege {} was successfully created. Wait for admin to approval".format(privilege.id),)
    return redirect('/access-control/user-privileges/')

@login_required
def activate_privilege(request,pk):
    user = request.user
    privilege_to_activate = UserPrivilege.objects.get(id = pk)
    privilege_to_activate.is_active = True
    privilege_to_activate.approved_by = user
    privilege_to_activate.save()
    messages.success(request,"Privilege {} was successfully assigned to {}".format(privilege_to_activate.id,privilege_to_activate.user))
    return redirect('/access-control/user-privileges/')

@login_required
def delete_privilege(request,pk):
    user = request.user
    user_privilege = UserPrivilege.objects.get(id = pk)
    privilege_owner = user_privilege.user
    if user.get_user_type_display() == 'access control admin':
        user_privilege.delete()
        messages.success(request,"Privilege {} was successfully taken from {}".format(pk,privilege_owner))
        return redirect('/access-control/user-privileges/')

    elif user.get_user_type_display() == 'access control staff':
        user_privilege.is_delete_requested = True
        user_privilege.is_active = False
        user_privilege.save()
        messages.success(request,"Privilege {} deletion requested wait for admin to approve".format(pk),)
        return redirect('/access-control/user-privileges/')
    else:
        return HttpResponse("Hooold up! You do not have the privilege to access this page")

def update_user_privilege(request):
    pass

