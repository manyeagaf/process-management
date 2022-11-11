from logging import PlaceHolder
from django import forms
from pkg_resources import require
from .models import Request, Attachment, Comment, RequestType
from django.forms import ClearableFileInput
from users.models import User


class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        exclude = ("request", "comment",)
        widgets = {
            "document": ClearableFileInput(attrs={"multiple": True}),
        }


class RequestForm(AttachmentForm):
    message = forms.Textarea()
    class Meta:
        model = Request
        exclude = ("assignee", "status", "initiator",
                   "assignee_status", "slug")
        # widgets = {
        #     "attachments": ClearableFileInput(attrs={"multiple": True}),
        # }

    # def clean_attachment(self):
    #     attachment = self.cleaned_data['attachment']
    #     valid_extensions = ['pdf']
    #     extension = attachment.rsplit('.', 1)[1].lower()
    #     if extension not in valid_extensions:
    #         raise forms.ValidationError('The given URL does not '
    #                                     'match valid image extensions.')
    #     return attachment


class CreateRequest(forms.Form):
    
    title = forms.CharField(max_length=450,required=True)
    request_type = forms.ModelChoiceField(queryset=RequestType.objects.all(),widget=forms.Select,required=True)
    customer_name = forms.CharField(max_length=255,required=True)
    message = forms.CharField(max_length=200, widget=forms.Textarea,required=False)
    documents = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}),required=True)
    
class AddComment(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ("slug", "request", "owner")

class AssignRequest(forms.Form):
    assign_to = forms.ModelChoiceField(
        queryset=User.objects.filter(user_type=2,is_active=True),empty_label = "Select Officer")
    
