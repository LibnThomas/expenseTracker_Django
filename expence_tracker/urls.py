from django.urls import path
from expence_tracker import views

urlpatterns=[
	path('',views.loginfun,name="login"),
	path('expense/',views.expence,name="expence"),
	path('expense/bar_chart_view/',views.summary_chart,name="barchart")

]