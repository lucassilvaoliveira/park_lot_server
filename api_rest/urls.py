from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('customer', views.createOrUpdateCustomer, name='create_or_update_customer'),
    path('customers', views.listCustomers, name='list_customers'),
    path('plan', views.createOrUpdatePlan, name='create_or_update_plan'),
    path('customer-plan', views.vinculeCustomerToPlan, name='vincule_customer_to_plan'),
    path('vehicle', views.createOrUpdateVehicle, name='create_or_update_vehicle'),
    path('contract', views.createOrUpdateContract, name='create_or_update_contract'),
    path('contract-rule', views.createOrUpdateContractRule, name='create_or_update_contract_rule'),
    path('parkmovement/entry', views.parkMovementEntry, name='park_movement_entry'),
    path('parkmovement/exit', views.parkMovementExit, name='park_movement_exit'),
    path('parkmovements', views.listParkMovements, name='list_park_movements')
]
