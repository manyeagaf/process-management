from datetime import datetime
from django.db import models
from django.urls import reverse
from users.models import User
import calendar
import uuid





class RequestType(models.Model):
    slug = models.SlugField(max_length=250, unique=True, null=True, blank=True)
    request_type = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.request_type


class Status(models.Model):
    slug = models.SlugField(max_length=250, unique=True, null=True, blank=True)
    status = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return self.slug


class Request(models.Model):
    title = models.CharField(max_length=450, null=True, blank=True)
    customer_name = models.CharField(max_length=300,)
    # BRANCH_CHOICES = (
    #     (2, "Ebankese Branch"),
    #     (3, "Accra Central Branch"),
    #     (4, "Republic Court Branch"),
    #     (5, "Kumasi Branch"),
    #     (6, "Tema Branch"),
    #     (7, "Legon Branch"),
    #     (8, "Abossey Okai Branch"),
    #     (9, "Tudu Branch"),
    #     (10, "Techiman Branch"),
    #     (11, "KNUST Brach"),
    #     (12, "Tamale Branch"),
    #     (13, "Koforidua Branch"),
    #     (14, "Baatsona Branch"),
    #     (15, "Private Panking"),
    #     (16, "Ashaiman Branch"),
    #     (17, "Takoradi Branch"),
    #     (18, "Kasoa Branch"),
    #     (19, "Post Office Square Branch"),
    #     (20, "Adabraka Branch"),
    #     (21, "Agona Swedru Branch"),
    #     (22, "Cape Coast Branch"),
    #     (23, "Winneba Branch"),
    #     (24, "Asamankese Branch"),
    #     (25, "Dansoman Branch"),
    #     (26, "Accra Newtown Branch"),
    #     (27, "Sefwi Wiawso"),
    #     (28, "Essam Branch"),
    #     (29, "Asankragua Branch"),
    #     (30, "Sefwi Bekwai Branch "),
    #     (31, "Akontombra Branch"),
    #     (32, "Juaboso"),
    #     (33, "Asempaneye Branch"),
    #     (34, "Madina Branch"),
    #     (35, "Goaso Branch"),
    #     (36, "Achimota Branch"),
    #     (37, "Asokwa Branch"),
    #     (38, "Tema Community 25 Branch"),
    #     (39, "Bolgatanga Branch"),
    #     (40, "Adjiringanor Branch"),
    # )
    # branch = models.PositiveBigIntegerField(
    #     choices=BRANCH_CHOICES, null=True, blank=True)

    request_type = models.ForeignKey(
        RequestType, on_delete=models.SET_NULL, null=True, blank=True)
    request_id = models.CharField(max_length=13,null=True,blank = True)
    initiator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='initiator')
    assignee = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assignee')

    ASSIGNEE_STATUS_CHOICES = (
        (1, "Received"),
        (2, "Completed"),

    )
    status = models.ForeignKey(
        Status, null=True, blank=True, on_delete=models.SET_NULL)
    assignee_status = models.PositiveBigIntegerField(
        choices=ASSIGNEE_STATUS_CHOICES, default=1)
    is_assigned = models.BooleanField(default=False)
    assigned_at = models.DateTimeField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    is_archieved = models.BooleanField(default=False)
    archieved_at = models.DateTimeField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def get_absolute_url(self):
        return reverse("tickets:request", kwargs={"pk": self.pk})
    
    def __str__(self):
        return str(self.id)

class Comment(models.Model):
    slug = models.SlugField(null=True, blank=True, unique=True)
    comment = models.TextField(max_length=500)
    request = models.ForeignKey(
        Request, on_delete=models.CASCADE, null=True, blank=True,)
    owner = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='owner')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.comment


class Attachment(models.Model):

    document = models.FileField(upload_to='documents/%Y/%m/%d/')
    request = models.ForeignKey(
        Request, on_delete=models.CASCADE, null=True, blank=True, related_name='request')
    comment = models.ForeignKey(
        Comment, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.document.url

