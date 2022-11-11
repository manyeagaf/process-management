from django.shortcuts import render
from users.models import User, UserPrivilege
from users.forms import UserRegistrationForm,PrivilegeForm
from django.contrib.auth.decorators import permission_required, login_required
from django.db.models import Q
# Create your views here.

@login_required
def dashboard(request):
    context = {}
    users = User.objects.all()
    context['users'] = users

    context['form'] = UserRegistrationForm
    return render(request,'access_control/dashboard.html',context)


@login_required
def privileges(request):
    context = {}
    context['form'] = PrivilegeForm
    privileges = UserPrivilege.objects.all()
    context['privileges'] = privileges
    
    context['page'] = 'privileges'
    return render(request,'access_control/user-privileges/privileges.html',context)

@login_required
def privilege_action(request,pk):
    context = {}
    privilege = UserPrivilege.objects.get(id = pk)
    context['privilege'] = privilege
    return render(request,'access_control/user-privileges/privilege_action.html',context)



@login_required
def pending_user_creations(request):
    context = {}
    pending_users = User.objects.filter(Q(is_active = False)|Q(is_delete_requested = True))
    context['pending_users'] = pending_users
    context['page'] = "pendingUsers"
    return render(request,'access_control/approvals/pending_users.html',context)

@login_required
def pending_user_approve(request,pk):
    context = {}
    pending_user = User.objects.get(id = pk)
    context['pending_user'] = pending_user
    return render(request,'access_control/user-pages/pending_user_approve.html',context)

@login_required
def pending_user_deletions(request):
    context ={}
    pending_user_deletions = User.objects.filter(is_delete_requested = True)
    context['pending_user_deletions'] = pending_user_deletions
    context['page'] = 'pendingUserDeletion'
    return render(request,'access_control/approvals/pending_user_deletions.html',context)

@login_required
def pending_user_delete(request,pk):
    context = {}
    pending_user = User.objects.get(id = pk)
    context['pending_user'] = pending_user
    return render(request,'access_control/user-pages/pending_user_delete.html',context)
@login_required
def user_action(request,pk):
    context = {}
    pending_user = User.objects.get(id = pk)
    context['pending_user'] = pending_user
    return render(request,'access_control/user-pages/user_action.html',context)

@login_required
def pending_privileges(request):
    context = {}
    pending_privileges = UserPrivilege.objects.filter(is_active = False)
    context['pending_privileges'] = pending_privileges
    context['page'] = 'pendingPrivilegeCreations'
    return render(request,'access_control/user-privileges/pending_privileges.html',context)

@login_required
def pending_privilege_approve(request,pk):
    context = {}
    pending_privilege = UserPrivilege.objects.get(id = pk)
    context['pending_privilege'] = pending_privilege
    return render(request,'access_control/user-privileges/pending_privilege_approve.html',context)





