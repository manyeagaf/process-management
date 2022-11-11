from ast import Add
import json
from unicodedata import category
from django.shortcuts import redirect, render, get_object_or_404
from tickets.models import Request, Comment, Attachment, RequestType, Status
from django.contrib.auth.decorators import permission_required, login_required
from django.db.models import Q

from users.models import User,UserPrivilege,Privilege
from datetime import datetime
from random import randrange, sample, choice
from datetime import timedelta
from django.utils.decorators import method_decorator
from django.core import serializers
from django.http import JsonResponse,HttpResponse
from tickets.forms import AssignRequest
from users.views import get_branch_user_privilege,get_admin_user_privilege,get_officer_user_privilege
# Create your views here.
from tickets.tasks import test,archieving_task


@login_required
def dashboard(request):
    test()
    archieving_task()
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

    if admin_privilege or user.get_user_type_display() == 'admin':
        current_month = datetime.now().month
        current_year = datetime.now().year
        #Status types for queries
        status_open = Status.objects.get(slug="open")
        status_closed = Status.objects.get(slug="closed")
        status_pending = Status.objects.get(slug="pending")
        status_requestor_replied = Status.objects.get(slug="requestor-replied")
        status_answered = Status.objects.get(slug="answered")
            
        #All requests
        all_requests = Request.objects.all()
        context['all_requests'] = all_requests
        #All request categories
        open_requests = Request.objects.filter(status = status_open)
        context["open_requests"] = open_requests

        closed_requests = Request.objects.filter(status = status_closed)
        context["closed_requests"] = closed_requests


        pending_requests = Request.objects.filter(
            status = status_pending)
        context["pending_requests"] = pending_requests

        active_requests = Request.objects.filter(Q(status = status_answered) | Q(status = status_requestor_replied))
        context["active_requests"] = active_requests
        #Bar graph
        request_types = RequestType.objects.all()
        rts = [i.request_type for i in request_types]
        context["rts"] = rts
        rts_count = []
        for rt in request_types:
            rts_count.append(len(Request.objects.filter(
                created_at__year = current_year,
                request_type=rt, created_at__month=current_month)))
        context["rts_count"] = rts_count

        active_requests_by_month = []
        open_requests_by_month = []
        closed_requests_by_month = []
        pending_requests_by_month = []


        current_year = datetime.now().year
        current_year_requests = Request.objects.filter(
            created_at__year=current_year)
        for month in range(1, 13):
            open_c = len(Request.objects.filter(
                created_at__year=current_year, created_at__month=month, status=status_open))
            closed_c = len(Request.objects.filter(
                created_at__year=current_year, created_at__month=month, status=status_closed))
            pending_c = len(Request.objects.filter(
                created_at__year=current_year, created_at__month=month, status=status_pending))
            active_c = len(Request.objects.filter(
                created_at__year=current_year, created_at__month=month, status=status_answered
            )) + len(Request.objects.filter(
                created_at__year=current_year, created_at__month=month, status=status_requestor_replied
            )
            )

            if open_c != 0:
                open_requests_by_month.append(
                    open_c)
            else:
                open_requests_by_month.append(
                    open_c)
            if closed_c != 0:
                closed_requests_by_month.append(
                    closed_c)
            else:
                closed_requests_by_month.append(
                    closed_c)
            if pending_c != 0:
                pending_requests_by_month.append(
                    pending_c)
            else:
                pending_requests_by_month.append(
                    pending_c)
            
            if active_c != 0:
                active_requests_by_month.append(
                    active_c)
            else:
                active_requests_by_month.append(
                    active_c)
        
        # Pie Chart data for current month
        context['active_requests_by_month'] = active_requests_by_month
        context["open_requests_by_month"] = open_requests_by_month
        context["closed_requests_by_month"] = closed_requests_by_month
        context["pending_requests_by_month"] = pending_requests_by_month
        
        answered_count = Request.objects.filter(created_at__year = current_year,
            status=status_answered, created_at__month=current_month).count

        
        open_count = Request.objects.filter(created_at__year = current_year,
            created_at__month=current_month, status = status_open).count

        
        closed_count = Request.objects.filter(created_at__year = current_year,
            created_at__month=current_month, status = status_closed).count

        
        requestor_replied_count = Request.objects.filter(created_at__year = current_year,
            status=status_requestor_replied, created_at__month=current_month).count

        
        pending_count = Request.objects.filter(
            created_at__year = current_year,
            created_at__month=current_month, status = status_pending).count
        context["answered_count"] = answered_count
        context["open_count"] = open_count
        context["closed_count"] = closed_count
        context["requestor_replied_count"] = requestor_replied_count
        context["pending_count"] = pending_count
        # Resolution for current month
        requests_for_current_month = len(Request.objects.filter(
            created_at__year = current_year,
            created_at__month=current_month))

        closed_requests_for_current_month = len(Request.objects.filter(created_at__year = current_year,
            created_at__month=current_month, status = status_closed))
        
        try:
            monthly_resolution_rate = round((closed_requests_for_current_month /
                                        requests_for_current_month)*100)
            context["monthly_resolution_rate"] = monthly_resolution_rate
        except ZeroDivisionError:
            monthly_resolution_rate = 0
            context["monthly_resolution_rate"] = monthly_resolution_rate
        #Annual Resolution Rate
        requests_for_current_year = len(Request.objects.filter(
            created_at__year = current_year

        ))

        closed_requests_for_current_year = len(Request.objects.filter(
            status = status_closed,
            created_at__year = current_year
        ))

        try:
            annual_resolution_rate = round((closed_requests_for_current_year/requests_for_current_year)*100)
            context['annual_resolution_rate'] = annual_resolution_rate
        except ZeroDivisionError:
            annual_resolution_rate = 0
            context['annual_resolution_rate'] = annual_resolution_rate

        return render(request, 'admin_user/dashboard.html', context)
    else:
        return HttpResponse("Hooold up! You do not have the privilege to access this page")
        

@login_required
def active(request):
    user = request.user
    context = {}
    #Get admin user privilege status for current user
    admin_privilege = get_admin_user_privilege(user)
    context['admin_privilege'] = admin_privilege


    # #Get officer user privilege status for current user
    # officer_privilege = get_officer_user_privilege(user)
    # context['officer_privilege'] = officer_privilege

    # #Get branch user privilege status for current user
    # branch_privilege = get_branch_user_privilege(user)
    # context['branch_privileges'] = branch_privilege

    if admin_privilege or user.get_user_type_display() == "admin":
        context['page'] = 'active'
        #Status types for queries
        status_requestor_replied = Status.objects.get(slug="requestor-replied")
        status_answered = Status.objects.get(slug="answered")
        #Active requests
        active_requests = Request.objects.filter(Q(status = status_answered) | Q(status = status_requestor_replied))
        context["active_requests"] = active_requests
        return render(request,'admin_user/request/active.html',context)
    else:
        return HttpResponse("Hooold up! You do not have the privilege to access this page")

@login_required
def open(request):
    user = request.user
    context = {}
    #Get admin user privilege status for current user
    admin_privilege = get_admin_user_privilege(user)
    context['admin_privilege'] = admin_privilege


    # #Get officer user privilege status for current user
    # officer_privilege = get_officer_user_privilege(user)
    # context['officer_privilege'] = officer_privilege

    # #Get branch user privilege status for current user
    # branch_privilege = get_branch_user_privilege(user)
    # context['branch_privileges'] = branch_privilege
    if admin_privilege or user.get_user_type_display() == "admin":
        context['page'] = 'open'
        #Status types for queries
        status_open = Status.objects.get(slug="open")
        #Assign Form
        form = AssignRequest()
        context["form"] = form
        #Open request
        open_requests = Request.objects.filter(status=status_open)
        context["open_requests"] = open_requests
        return render(request,'admin_user/request/open.html',context)
    else:
        return HttpResponse("Hooold up! You do not have the privilege to access this page")


@login_required
def pending(request):
    user = request.user
    context = {}

    #Get admin user privilege status for current user
    admin_privilege = get_admin_user_privilege(user)
    context['admin_privilege'] = admin_privilege


    # #Get officer user privilege status for current user
    # officer_privilege = get_officer_user_privilege(user)
    # context['officer_privilege'] = officer_privilege

    # #Get branch user privilege status for current user
    # branch_privilege = get_branch_user_privilege(user)
    # context['branch_privileges'] = branch_privilege
    if admin_privilege or user.get_user_type_display() == "admin":
        context['page'] = 'pending'
        #Status types for queries
        status_pending = Status.objects.get(slug="pending")
        #Pending requests
        pending_requests = Request.objects.filter(
        status = status_pending)
        context["pending_requests"] = pending_requests
        return render(request,'admin_user/request/pending.html',context)
    else:
        return HttpResponse("Hooold up! You do not have the privilege to access this page")

    

@login_required
def closed(request):
    user = request.user
    context = {}
    #Get admin user privilege status for current user
    admin_privilege = get_admin_user_privilege(user)
    context['admin_privilege'] = admin_privilege


    # #Get officer user privilege status for current user
    # officer_privilege = get_officer_user_privilege(user)
    # context['officer_privilege'] = officer_privilege

    # #Get branch user privilege status for current user
    # branch_privilege = get_branch_user_privilege(user)
    # context['branch_privileges'] = branch_privilege
    if admin_privilege or user.get_user_type_display() == "admin":
        context['page'] = 'closed'
        #Status types for queries
        status_closed = Status.objects.get(slug="closed")
        #Closed Requests
        closed_requests = Request.objects.filter(status=status_closed,is_archieved = False)
        context["closed_requests"] = closed_requests
        return render(request,'admin_user/request/closed.html',context)
    else:
        return HttpResponse("Hooold up! You do not have the privilege to access this page")

@login_required
def request_detail(request,request_id):
    user = request.user
    context = {}
    #Get admin user privilege status for current user
    admin_privilege = get_admin_user_privilege(user)
    context['admin_privilege'] = admin_privilege

    # #Get officer user privilege status for current user
    # officer_privilege = get_officer_user_privilege(user)
    # context['officer_privilege'] = officer_privilege

    # #Get branch user privilege status for current user
    # branch_privilege = get_branch_user_privilege(user)
    # context['branch_privileges'] = branch_privilege

    if admin_privilege or user.get_user_type_display() == "admin":
        rq = Request.objects.get(request_id = request_id)
        attechments = Attachment.objects.filter(request=rq)
        attachments_with_comments = Attachment.objects.exclude(
            comment__isnull=True)
        initiator = rq.initiator
        # initiator = User.objects.get(id=initiator_id)
        context["attachments_with_comments"] = attachments_with_comments
        context["request"] = rq
        context["attachments"] = attechments
        context["initiator"] = initiator
        recent_comments = Comment.objects.filter(
            request=rq).all()[:5]
        comments = Comment.objects.filter(request=rq).order_by("created_at")

        context["recent_comments"] = reversed(recent_comments)
        context["comments"] = comments
        return render(request,'admin_user/request/request.html',context)
    else:
        return HttpResponse("Hooold up! You do not have the privilege to access this page")


@login_required
def archieve(request):
    context = {}
    archieved_requests = Request.objects.filter(is_archieved = True)
    context['archieved_requests'] = archieved_requests

    context['page'] = 'archieved'
    return render(request,'admin_user/request/archieved.html',context)


def request_assign(request,request_id):
    context = {}
    instance = Request.objects.get(request_id = request_id)
    context['instance'] = instance
    return render(request,'admin_user/assign_modal.html',context)

