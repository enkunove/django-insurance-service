from django.urls import path, re_path
from . import views
from .views import EmployeeCreateView, CustomerCreateView, OwnerCreateView, RealtyCreateView, RealtyUpdateView, \
    RealtyDeleteView, DealCreateView, DealUpdateView, DealDeleteView, DealAdminCreateView, CustomerAdminCreateView, \
    CustomerAdminUpdateView, EmployeeAdminUpdateView, EmployeeAdminCreateView

urlpatterns = [
    path('employee/', EmployeeCreateView.as_view(), name="assign-employee"),
    path('customer/', CustomerCreateView.as_view(), name="assign-customer"),
    path('customers/', views.customers, name="customers"),
    path('customer-admin/', CustomerAdminCreateView.as_view(), name="admin-customer"),
    re_path(r'^customer-update/(?P<pk>\d+)/$', CustomerAdminUpdateView.as_view(), name="customer-update"),
    path('owner/', OwnerCreateView.as_view(), name="assign-owner"),
    path('insurances-list', views.insurances, name="insurances-list"),
    path('my-insurances', views.my_insurances, name="my-my_insurances"),
    re_path(r'^insurances/(?P<id>\d+)/$', views.insurance, name="realty-detail"),
    path('realty-add/', RealtyCreateView.as_view(), name="realty-add"),
    re_path(r'^insurance-update/(?P<pk>\d+)/$', RealtyUpdateView.as_view(), name="realty-update"),
    re_path(r'^insurance-delete/(?P<pk>\d+)/$', RealtyDeleteView.as_view(), name="realty-delete"),
    re_path(r'^deal-create/(?P<realty_pk>\d+)/$', DealCreateView.as_view(), name="deal-create"),
    path('deal-create-admin/', DealAdminCreateView.as_view(), name="deal-admin-create"),
    re_path(r'^deal-update/(?P<pk>\d+)/$', DealUpdateView.as_view(), name="deal-update"),
    re_path(r'^deal-delete/(?P<pk>\d+)/$', DealDeleteView.as_view(), name="deal-delete"),
    path('deals/', views.deals, name="deals"),
    path('my-deals/', views.my_deals, name="my-deals"),
    re_path(r'^employee-update/(?P<pk>\d+)/$', EmployeeAdminUpdateView.as_view(), name="employee-update"),
    path('employees/', views.employees, name="employees"),
    path('employee-admin/', EmployeeAdminCreateView.as_view(), name="admin-employee"),

]