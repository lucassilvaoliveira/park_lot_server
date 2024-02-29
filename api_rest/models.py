from datetime import datetime
from django.db import models

# Create your models here.

class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    card_id = models.CharField(max_length=10, null=True)

    def __str__(self) -> str:
        return super().__str__()
    
class Vehicle(models.Model):
    id = models.AutoField(primary_key=True)
    plate = models.CharField(max_length=10)
    model = models.CharField(max_length=30, null=True)
    description = models.CharField(max_length=50, null=True)
    customer_id = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return super().__str__()

class Plan(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=50)
    value = models.FloatField()

    def __str__(self) -> str:
        return super().__str__()
    
class CustomerPlan(models.Model):
    id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(Customer, on_delete=models.SET)
    plan_id = models.ForeignKey(Plan, on_delete=models.SET)
    due_date = models.DateTimeField()

    def __str__(self) -> str:
        return super().__str__()
    
class Contract(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=50)
    max_value = models.FloatField(null=True)

    def __str__(self) -> str:
        return super().__str__()
    
class ContractRule(models.Model):
    id = models.AutoField(primary_key=True)
    contract_id = models.ForeignKey(Contract, on_delete=models.SET)
    until = models.IntegerField()
    value = models.FloatField()

    def __str__(self) -> str:
        return super().__str__()

class ParkMovement(models.Model):
    id = models.AutoField(primary_key=True)
    entry_date = models.DateTimeField(auto_now_add=True)
    exit_date = models.DateTimeField(null=True)
    vehicle_id = models.ForeignKey(Vehicle, on_delete=models.SET)
    value = models.FloatField(null=True)

    def __str__(self) -> str:
        return super().__str__()