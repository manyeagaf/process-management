from ast import Add
import json
from django.shortcuts import redirect, render, get_object_or_404
from tickets.models import Request, Comment, Attachment, RequestType, Status
from django.contrib.auth.decorators import permission_required, login_required
from tickets.forms import AssignRequest, CreateRequest, RequestForm
from users.models import User
from datetime import datetime
from random import randrange, sample, choice
from datetime import timedelta
import string
from django.utils.decorators import method_decorator
from django.core import serializers
from django.http import JsonResponse,HttpResponse
from django.db.models import Q
from users.views import get_officer_user_privilege,get_admin_user_privilege,get_branch_user_privilege


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


    #Status types for queries
    status_open = Status.objects.get(slug="open")
    status_closed = Status.objects.get(slug="closed")
    status_pending = Status.objects.get(slug="pending")
    status_requestor_replied = Status.objects.get(slug="requestor-replied")
    status_answered = Status.objects.get(slug="answered")
    current_month = datetime.now().month
    if officer_privilege or user.get_user_type_display() == 'officer' or user.get_user_type_display() == 'admin':
           
        # Summary
        my_requests_this_month = Request.objects.filter(
            assignee=user, created_at__month=current_month)
        context["my_requests_this_month"] = my_requests_this_month

        pending_this_month = Request.objects.filter(
            assignee=user, created_at__month=current_month, status = status_pending)
        context["pending_this_month"] = pending_this_month
        closed_this_month = Request.objects.filter(
            status = status_closed, assignee=user, created_at__month=current_month)
        context["closed_this_month"] = closed_this_month

        # Bar Graph
        request_types = RequestType.objects.all()
        rts = [i.request_type for i in request_types]
        context["rts"] = rts
        rts_count = []
        for rt in request_types:
            rts_count.append(len(Request.objects.filter(assignee=user,
                                                        request_type=rt, created_at__month=current_month)))
        context["rts_count"] = rts_count

        # Resolution Rate
        try:

            resolution_rate = round((len(closed_this_month) /
                                    len(my_requests_this_month))*100)

            context["resolution_rate"] = resolution_rate
        except ZeroDivisionError:
            resolution_rate = 0

            context["resolution_rate"] = resolution_rate
        
        return render(request, 'officer/dashboard.html', context)
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
    context['branch_privilege'] = branch_privilege

    context['page'] = 'active'
    status_open = Status.objects.get(slug="open")
    status_closed = Status.objects.get(slug="closed")
    status_pending = Status.objects.get(slug="pending")
    status_requestor_replied = Status.objects.get(slug="requestor-replied")
    status_answered = Status.objects.get(slug="answered")
    if officer_privilege or user.get_user_type_display() == 'officer':

        active_requests = Request.objects.filter(Q(status = status_answered) | Q(status = status_requestor_replied), Q(assignee = user))
        context["active_requests"] = active_requests
        return render(request,'officer/request/active.html',context)
    else:
        return HttpResponse("Hooold up! You do not have the privilege to access this page")


@login_required
def assigned(request):
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

    context['page'] = 'assigned'
    status_open = Status.objects.get(slug="open")
    status_closed = Status.objects.get(slug="closed")
    status_pending = Status.objects.get(slug="pending")
    status_requestor_replied = Status.objects.get(slug="requestor-replied")
    status_answered = Status.objects.get(slug="answered")
    if officer_privilege or user.get_user_type_display() == 'officer':

        my_requests = Request.objects.filter(assignee=user)
        context["my_requests"] = my_requests
        return render(request,'officer/request/assigned.html',context)
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
    context['branch_privilege'] = branch_privilege
    context['page'] = 'pending'

    status_open = Status.objects.get(slug="open")
    status_closed = Status.objects.get(slug="closed")
    status_pending = Status.objects.get(slug="pending")
    status_requestor_replied = Status.objects.get(slug="requestor-replied")
    status_answered = Status.objects.get(slug="answered")
    if officer_privilege or user.get_user_type_display() == 'officer':

        pending_requests = Request.objects.filter(
                            assignee=user, status = status_pending)
        context["pending_requests"] = pending_requests
        return render(request,'officer/request/pending.html',context)
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
    context['branch_privilege'] = branch_privilege
    context['page'] = 'closed'
    status_open = Status.objects.get(slug="open")
    status_closed = Status.objects.get(slug="closed")
    status_pending = Status.objects.get(slug="pending")
    status_requestor_replied = Status.objects.get(slug="requestor-replied")
    status_answered = Status.objects.get(slug="answered")
    if officer_privilege or user.get_user_type_display() == 'officer':

        completed_requests = Request.objects.filter(
                            assignee=user, status = status_closed,is_archieved = False)
        context["closed_requests"] = completed_requests
        return render(request,'officer/request/closed.html',context)
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
    context['branch_privilege'] = branch_privilege
    if officer_privilege or user.get_user_type_display() == 'officer':

        rq = Request.objects.get(request_id=request_id)
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
        return render(request, 'officer/request/request.html', context) 
    else:
        return HttpResponse("Hooold up! You do not have the privilege to access this page")

# @login_required
# def officer(request, slug = None,pk = None):
#     user = request.user
#     if user.get_user_type_display() == 'officer':
#         status_open = Status.objects.get(slug="open")
#         status_closed = Status.objects.get(slug="closed")
#         status_pending = Status.objects.get(slug="pending")
#         status_requestor_replied = Status.objects.get(slug="requestor-replied")
#         status_answered = Status.objects.get(slug="answered")
#         context = {}
#         if pk:
#             context['pk'] = pk
#             rq = Request.objects.get(pk=pk)
#             attechments = Attachment.objects.filter(request=rq)
#             attachments_with_comments = Attachment.objects.exclude(
#                 comment__isnull=True)
#             initiator = rq.initiator
#             # initiator = User.objects.get(pk=initiator_pk)
#             context["attachments_with_comments"] = attachments_with_comments
#             context["request"] = rq
#             context["attachments"] = attechments
#             context["initiator"] = initiator
#             recent_comments = Comment.objects.filter(
#                 request=rq).all()[:5]
#             comments = Comment.objects.filter(request=rq).order_by("created_at")

#             context["recent_comments"] = reversed(recent_comments)
#             context["comments"] = comments
#             return render(request, 'officer/dashboard.html', context) 
#         else:

#             if slug:
#                 context['category'] = True
#                 context['slug'] = slug
#                 if slug == "assigned":
                    
#                     my_requests = Request.objects.filter(assignee=user)
#                     context["my_requests"] = my_requests
                    
#                 elif slug == "closed":
#                     completed_requests = Request.objects.filter(
#                         assignee=user, status = status_closed)
#                     context["closed_requests"] = completed_requests
                

#                 elif slug == "pending":
#                     pending_requests = Request.objects.filter(
#                         assignee=user, is_closed=False)
#                     context["pending_requests"] = pending_requests

#                 else:
#                     active_requests = Request.objects.filter(Q(status = status_answered) | Q(status = status_requestor_replied) & Q(assignee = user))
#                     context["active_requests"] = active_requests
#             else:
#                 current_month = datetime.now().month
                
#                 # Summary
#                 my_requests_this_month = Request.objects.filter(
#                     assignee=user, created_at__month=current_month, is_assigned=True)
#                 context["my_requests_this_month"] = my_requests_this_month

#                 pending_this_month = Request.objects.filter(
#                     assignee=user, created_at__month=current_month, is_assigned=True, is_closed=False)
#                 context["pending_this_month"] = pending_this_month
#                 closed_this_month = Request.objects.filter(
#                     is_closed=True, assignee=user, created_at__month=current_month)
#                 context["closed_this_month"] = closed_this_month

#                 # Bar Graph
#                 request_types = RequestType.objects.all()
#                 rts = [i.request_type for i in request_types]
#                 context["rts"] = rts
#                 rts_count = []
#                 for rt in request_types:
#                     rts_count.append(len(Request.objects.filter(assignee=user,
#                                                                 request_type=rt, created_at__month=current_month)))
#                 context["rts_count"] = rts_count

#                 # Resolution Rate
#                 try:

#                     resolution_rate = round((len(closed_this_month) /
#                                             len(my_requests_this_month))*100)

#                     context["resolution_rate"] = resolution_rate
#                 except ZeroDivisionError:
#                     resolution_rate = 0

#                     context["resolution_rate"] = resolution_rate
                
#             return render(request, 'officer/dashboard.html', context)
#     else:
#         return redirect('/')
        