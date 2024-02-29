from django.contrib import admin

from .models import Customer, Contract, Plan, CustomerPlan, Contract, ContractRule, ParkMovement, Vehicle

admin.site.register(Customer)
admin.site.register(Contract)
admin.site.register(Plan)
admin.site.register(CustomerPlan)
admin.site.register(ContractRule)
admin.site.register(ParkMovement)
admin.site.register(Vehicle)