from ast import Add
import json
from django.shortcuts import redirect, render, get_object_or_404
from .models import Request, Comment, Attachment, RequestType, Status
from django.contrib.auth.decorators import permission_required, login_required
from users.models import User
from datetime import datetime
from random import randrange, sample, choice,randint
from datetime import timedelta
import string
from django.utils.decorators import method_decorator
from django.core import serializers
from django.http import JsonResponse,HttpResponse
from users.views import get_admin_user_privilege,get_branch_user_privilege,get_officer_user_privilege
from django.core.mail import send_mail
from django.contrib import messages


# class RequestsDatatable(ServerSideDatatableView):
    
#     columns = ["request_id"]
    
#     @method_decorator(login_required)
#     def dispatch(self, *args, **kwargs):
#         return super(RequestsDatatable, self).dispatch(*args, **kwargs)

#     def get_queryset(self):
#         return Request.objects.all()


@login_required
def getsubmitted(request):
    if request.method == "GET":
        data = serializers.serialize(
            "json", queryset=Request.objects.filter(initiator=request.user))
    print(data)
    return JsonResponse({"submitted": data})


def random_date(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)


d1 = datetime.strptime('1/1/2022 1:30 PM', '%m/%d/%Y %I:%M %p')
d2 = datetime.strptime('7/12/2022 4:50 AM', '%m/%d/%Y %I:%M %p')
# print(random_date(d1, d2))

def generate_request_id():
    request_ids = [r.id for r in Request.objects.all().only('request_id')]
    id_list = [str(randint(1,9))]
    for i in range(12):
        id_list.append(str(randint(0,9)))
    request_id = ''.join(id_list)
    while(request_id in request_ids):
        id_list = [str(randint(1,9))]
        for i in range(12):
            id_list.append(str(randint(0,9)))
        request_id = ''.join(id_list)
    return request_id

def fake_requests(n):
    r_types = RequestType.objects.all()
    status = Status.objects.get(slug="open")
    for i in range(n):
        request_id = generate_request_id()
        initiator = choice(User.objects.filter(user_type=1))
        r_type = choice(r_types)
        c_fname = ''.join(choice(string.ascii_letters) for x in range(5))
        title = ''.join(choice(string.ascii_letters) for x in range(5))
        rq = Request(title = title,request_id = request_id,
                     initiator=initiator,
                     customer_name=c_fname, request_type=r_type, status=status
                     )
        rq.created_at = random_date(d1, d2)
        rq.save()

def limit_check():
    all_requests = Request.objects.all()
    if len(all_requests) >= 890:
        return True
    return False



@ login_required
def request_detail(request, request_id):
    context = {}

    rq = Request.objects.get(request_id=request_id)
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
    print(generate_request_id())
    return render(request, 'requests/request_detail.html', context)

@ login_required
def comment_create(request, request_id):
    user = request.user
    rq = get_object_or_404(Request, request_id=request_id)
    message = request.POST.get("message")
    files = request.FILES.getlist("filepond")
    if rq.assignee == user:
        rq.status = Status.objects.get(slug = "answered")
    else:
        rq.status = Status.objects.get(slug = "requestor-replied")
    rq.save()
    comment = Comment.objects.create(
        comment=message,
        request=rq,
        owner=request.user,
    )
    comment.save()
    for file in files:
        attachment = Attachment(document=file)
        attachment.request = rq
        attachment.comment = comment
        attachment.save()
    # send_mail()
    return redirect(f"/{user.get_user_type_display()}/requests/{request_id}")


@ login_required
def request_create(request):
    user = request.user
    if not limit_check():
        title = request.POST.get('title')
        status = Status.objects.get(slug="open")
        customer_name = request.POST.get("customer_name")
        request_type_id = request.POST.get("request_type")
        request_type = RequestType.objects.get(id=request_type_id)
        files = request.FILES.getlist("documents")
        message = request.POST.get("message")
        
        request_id = generate_request_id()
        rq = Request.objects.create(title = title,request_id = request_id,
            customer_name=customer_name, initiator=request.user, request_type=request_type, status=status)
        comment = Comment.objects.create(
            request =rq,
            comment =message,
            owner =user,
        )
        
        for file in files:
            attachment = Attachment(document=file)
            attachment.request = rq
            attachment.save()
        messages.success(request,"Request {} created successfilly".format(rq.request_id))
        return redirect("/")
    else:
        return HttpResponse("Cannot create request.Please contact the developer for assistance")
    
@login_required
def assign_request(request, request_id):

    user = request.user
    #Get admin user privilege status for current user
    admin_privilege = get_admin_user_privilege(user)

    #Get officer user privilege status for current user
    officer_privilege = get_officer_user_privilege(user)

    #Get branch user privilege status for current user
    branch_privilege = get_branch_user_privilege(user)
    if user.get_user_type_display() == "admin" or admin_privilege:
        rq = Request.objects.get(request_id=request_id)
        
        assign_to = request.POST.get("assign_to")
        assignee = User.objects.get(id=int(assign_to))
        rq.assignee = assignee
        rq.is_assigned = True
        rq.assigned_at = datetime.now()
        rq.status = Status.objects.get(slug="pending")
        rq.save()
        messages.success(request,"Request {} assigned to {}".format(request_id,assignee),),
        return redirect("/admin/open/")
    else:
        return HttpResponse("Hooold up! You do not have the privilege to access this page")

@login_required
def close_request(request,request_id):
    user = request.user
    rq = Request.objects.get(request_id = request_id)
    rq.status = Status.objects.get(slug = "closed")
    rq.closed_at = datetime.now()
    rq.save()
    date = "Closed on " + str(datetime.now().ctime()) + " by " + str(user)
    comment = Comment.objects.create(comment = date,request = rq,owner = user)
    messages.success(request,"Request {} closed by {} at {}".format(request_id,user,datetime.now().ctime(),),),
    return redirect("/"+user.get_user_type_display()+"/closed/")

@login_required
def open_request(request,pk):
    user = request.user
    rq = Request.objects.get(id = pk)
    if rq.is_assigned == True:
        rq.status = Status.objects.get(slug = "pending")
    else:
        rq.status = Status.objects.filter(slug = "open")
    rq.is_closed = False
    rq.save()
    return redirect("/"+user.get_user_type_display()+"/requests/" + str(pk))

# Archive Requests
def archieve_requests():
    current_date = datetime.now().date()
    closed_requests = Request.objects.filter(status = Status.objects.get(slug = 'closed'),is_archieved = False) 
    for rq in closed_requests:
        
        if current_date.month-rq.closed_at.month>1 or  (current_date.month-rq.closed_at.month == 1 and current_date.day >= rq.closed_at.day):
            rq.is_archieved = True
            rq.archieved_at = datetime.now()
            rq.save()
