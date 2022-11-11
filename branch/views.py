from django.shortcuts import render,redirect

from tickets.models import Request, Comment, Attachment, RequestType, Status
from django.contrib.auth.decorators import permission_required, login_required
from users.models import User,Privilege,UserPrivilege
from datetime import datetime
from random import randrange, sample, choice
from django.utils.decorators import method_decorator
from django.http import JsonResponse,HttpResponse
from tickets.forms import AssignRequest,CreateRequest
from django.db.models import Q
from users.views import get_admin_user_privilege,  get_officer_user_privilege,get_branch_user_privilege

@login_required
def dashboard(request):
    user = request.user
    context = {}
    #Get admin user privilege status for current user
    admin_privilege = get_admin_user_privilege(user)
    context['admin_privilege'] = admin_privilege


    #Get officer user privilege status for current user
    officer_privilege = get_officer_user_privilege(user)
    context['officer_privilege'] = officer_privilege

   
    #Get branch user privilege status for current user
    branch_privilege = get_branch_user_privilege(user)
    context['branch_privilege'] = branch_privilege
    
    if branch_privilege or user.get_user_type_display() == 'branch':
        status_open = Status.objects.get(slug="open")
        status_closed = Status.objects.get(slug="closed")
        status_pending = Status.objects.get(slug="pending")
        status_requestor_replied = Status.objects.get(slug="requestor-replied")
        status_answered = Status.objects.get(slug="answered")
        current_month = datetime.now().month
        form = CreateRequest()
        context["form"] = form
        submitted_this_month = Request.objects.filter(
            initiator=user, created_at__month=current_month)
        context["submitted_this_month"] = submitted_this_month
        closed_this_month = Request.objects.filter(
            initiator=user, status = status_closed, created_at__month=current_month)
        context["closed_this_month"] = closed_this_month
        pending_this_month = Request.objects.filter(
            initiator=user, status = status_pending, created_at__month=current_month)
        context["pending_this_month"] = pending_this_month
        return render(request, 'branch/dashboard.html', context)
    else:
        return HttpResponse("Hooold up! You do not have the privilege to access this page")
        
@login_required
def active(request):
    user = request.user
    context = {}
    
    #Get admin user privilege status for current user
    admin_privilege = get_admin_user_privilege(user)
    context['admin_privilege'] = admin_privilege


    #Get officer user privilege status for current user
    officer_privilege = get_officer_user_privilege(user)
    context['officer_privilege'] = officer_privilege

    #Get branch user privilege status for current user
    branch_privilege = get_branch_user_privilege(user)
    context['branch_privileges'] = branch_privilege

    if branch_privilege or user.get_user_type_display() == 'branch':
    
        context['page'] = 'active'
        status_open = Status.objects.get(slug="open")
        status_closed = Status.objects.get(slug="closed")
        status_pending = Status.objects.get(slug="pending")
        status_requestor_replied = Status.objects.get(slug="requestor-replied")
        status_answered = Status.objects.get(slug="answered")
        active_requests = Request.objects.filter(Q(status = status_answered) | Q(status = status_requestor_replied),Q(initiator = user))
        context["active_requests"] = active_requests
        return render(request,'branch/request/active.html',context)
    else:
        return HttpResponse("Hooold up! You do not have the privilege to access this page")


@login_required
def pending(request):
    user = request.user
    context = {}
    
    #Get admin user privilege status for current user
    admin_privilege = get_admin_user_privilege(user)
    context['admin_privilege'] = admin_privilege


    #Get officer user privilege status for current user
    officer_privilege = get_officer_user_privilege(user)
    context['officer_privilege'] = officer_privilege

    #Get branch user privilege status for current user
    branch_privilege = get_branch_user_privilege(user)
    context['branch_privileges'] = branch_privilege

    if branch_privilege or user.get_user_type_display() == 'branch':
        context['page'] = 'pending'
        status_open = Status.objects.get(slug="open")
        status_closed = Status.objects.get(slug="closed")
        status_pending = Status.objects.get(slug="pending")
        status_requestor_replied = Status.objects.get(slug="requestor-replied")
        status_answered = Status.objects.get(slug="answered")
        pending_requests = Request.objects.filter(initiator=user, status = status_pending)
        context["pending_requests"] = pending_requests
        return render(request,'branch/request/pending.html',context)
    else:
        return HttpResponse("Hooold up! You do not have the privilege to access this page")

@login_required
def submitted(request):
    user = request.user
    context = {}
    
    #Get admin user privilege status for current user
    admin_privilege = get_admin_user_privilege(user)
    context['admin_privilege'] = admin_privilege


    #Get officer user privilege status for current user
    officer_privilege = get_officer_user_privilege(user)
    context['officer_privilege'] = officer_privilege

    #Get branch user privilege status for current user
    branch_privilege = get_branch_user_privilege(user)
    context['branch_privileges'] = branch_privilege

    
    if branch_privilege or user.get_user_type_display() == 'branch':
        context['page'] = 'submitted'
        status_open = Status.objects.get(slug="open")
        status_closed = Status.objects.get(slug="closed")
        status_pending = Status.objects.get(slug="pending")
        status_requestor_replied = Status.objects.get(slug="requestor-replied")
        status_answered = Status.objects.get(slug="answered")
        my_requests = Request.objects.filter(initiator=user)
        context["my_requests"] = my_requests
        return render(request,'branch/request/submitted.html',context)
    else:
        return HttpResponse("Hooold up! You do not have the privilege to access this page")


@login_required
def closed(request):
    user = request.user
    context = {}
    
   #Get admin user privilege status for current user
    admin_privilege = get_admin_user_privilege(user)
    context['admin_privilege'] = admin_privilege

    #Get officer user privilege status for current user
    officer_privilege = get_officer_user_privilege(user)
    context['officer_privilege'] = officer_privilege

    #Get branch user privilege status for current user
    branch_privilege = get_branch_user_privilege(user)
    context['branch_privileges'] = branch_privilege

    if branch_privilege or user.get_user_type_display() == 'branch':
        context['page'] = 'closed'
        status_open = Status.objects.get(slug="open")
        status_closed = Status.objects.get(slug="closed")
        status_pending = Status.objects.get(slug="pending")
        status_requestor_replied = Status.objects.get(slug="requestor-replied")
        status_answered = Status.objects.get(slug="answered")
        closed_requests = Request.objects.filter(initiator=user, status=status_closed,is_archieved = False)
        context["closed_requests"] = closed_requests
        return render(request,'branch/request/closed.html',context)
    else:
        return HttpResponse("Hooold up! You do not have the privilege to access this page")

@login_required
def request_detail(request,request_id):
    user = request.user
    context = {}
    
    #Get admin user privilege status for current user
    admin_privilege = get_admin_user_privilege(user)
    context['admin_privilege'] = admin_privilege


    #Get officer user privilege status for current user
    officer_privilege = get_officer_user_privilege(user)
    context['officer_privilege'] = officer_privilege

    #Get branch user privilege status for current user
    branch_privilege = get_branch_user_privilege(user)
    context['branch_privileges'] = branch_privilege

    if branch_privilege or user.get_user_type_display() == 'branch':
        rq = Request.objects.get(request_id = request_id)
        attechments = Attachment.objects.filter(request=rq)
        attachments_with_comments = Attachment.objects.exclude(
            comment__isnull=True)
        initiator = rq.initiator
        # initiator = User.objects.get(pk=initiator_pk)
        context["attachments_with_comments"] = attachments_with_comments
        context["request"] = rq
        context["attachments"] = attechments
        context["initiator"] = initiator
        recent_comments = Comment.objects.filter(
            request=rq).all()[:5]
        comments = Comment.objects.filter(request=rq).order_by("created_at")

        context["recent_comments"] = reversed(recent_comments)
        context["comments"] = comments
        return render(request, 'branch/request/request.html', context) 
    else:
        return HttpResponse("Hooold up! You do not have the privilege to access this page")

