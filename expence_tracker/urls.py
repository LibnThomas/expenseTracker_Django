from django.urls import path
from expence_tracker import views

urlpatterns=[
	path('',views.loginfun),
	path('expense/',views.expence)

]