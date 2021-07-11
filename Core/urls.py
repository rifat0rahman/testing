from typing import ValuesView
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('issueSubmitted/',views.successIssue,name='success'),
    path('reports/',views.reports,name='reports'),
    path('delete/<id>',views.delete_report,name='delete'),
]
