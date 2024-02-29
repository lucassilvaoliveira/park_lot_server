from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime

from api_rest.serializers import ContractRuleSerializer, ContractSerializer, CustomerPlanSerializer, CustomerSerializer, ParkMovementSerializer, PlanSerializer, VehicleSerializer

from .models import Customer, Contract, Plan, CustomerPlan, Contract, ContractRule, ParkMovement, Vehicle

import json

@api_view(['PUT'])
def createOrUpdateCustomer(request):
    if request.method == 'PUT':
        new_customer_data = request.data

        try:
            customer_id = new_customer_data.get('id')
            if customer_id:
                customer = Customer.objects.get(pk=customer_id)
            else:
                customer = Customer()

            customer.name = new_customer_data['name']
            card_id = new_customer_data.get('card_id')
            if card_id:
                customer.card_id = card_id
            else:
                customer.card_id = None

            customer.save()
            return Response({'success': 'Customer created/edited successfully'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'error': 'Invalid request method'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def listCustomers(request):
    if request.method == 'GET':

        customers = Customer.objects.all()

        serializer = CustomerSerializer(customers, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def createOrUpdateContractRule(request):
    if request.method == 'PUT':
        new_contract_rule = request.data

        try:
            contract_rule = ContractRule.objects.get(contract_id=new_contract_rule['contract_id']).first()

            return Response({ "error": "some contract rule already exists with this contract" }, status=status.HTTP_400_BAD_REQUEST)
        except ContractRule.DoesNotExist:
            serializer = ContractRuleSerializer(data=new_contract_rule)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def createOrUpdatePlan(request):
    if request.method == 'PUT':
        plan = request.data

        serializer = PlanSerializer(data=plan)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def vinculeCustomerToPlan(request):
    if request.method == 'PUT':
        customer_id = request.data.get('customer_id')
        plan_id = request.data.get('plan_id')

        customer = Customer.objects.filter(id=customer_id).first()
        plan = Plan.objects.filter(id=plan_id).first()

        if not customer:
            return Response({ "error": "no customer founded" }, status=status.HTTP_404_NOT_FOUND)
        
        if not plan:
            return Response({ "error": "no plan founded" }, status=status.HTTP_404_NOT_FOUND)
        
        customer_plan = CustomerPlan.objects.create(customer_id=customer, plan_id=plan, due_date=datetime.now)

        if customer_plan.pk is not None:
            customer_plan.save()
            return Response(customer_plan.data, status=status.HTTP_201_CREATED)


    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def createOrUpdateVehicle(request):
    if request.method == 'PUT':
        new_vehicle_data = request.data

        try:
            vehicle = Vehicle.objects.get(plate=new_vehicle_data['plate'])
            serializer = VehicleSerializer(vehicle, data=new_vehicle_data)
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
        except Vehicle.DoesNotExist:
            customer_id = new_vehicle_data.get('customer_id')
            customer = Customer.objects.filter(id=customer_id).first()

            if not customer:
                return Response({'error': 'Customer not found'}, status=status.HTTP_400_BAD_REQUEST)

            if not new_vehicle_data['model']:
                new_vehicle_data['model'] = None
            if not new_vehicle_data['description']:
                new_vehicle_data['description'] = None

            serializer = VehicleSerializer(data=new_vehicle_data)
            if serializer.is_valid():
                serializer.save(customer_id=customer)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def createOrUpdateContract(request):
    if request.method == 'PUT':
        new_contract_data = request.data

        try:
            contract = Contract.objects.get(description=new_contract_data['description'])
            serializer = ContractSerializer(contract, data=new_contract_data)
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
        except Contract.DoesNotExist:
            serializer = ContractSerializer(data=new_contract_data)
            if serializer.is_valid():
                contract = serializer.save()
                
                rules = new_contract_data.get('rules', [])
                for rule_data in rules:
                    until = rule_data.get('until')
                    value = rule_data.get('value')
                    ContractRule.objects.create(contract_id=contract, until=until, value=value)

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def createCustomerPlan(request):
    if request.method == 'POST':
        customerPlan = request.data

        serializer = CustomerPlanSerializer(data=customerPlan)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def listParkMovements(request):
    if request.method == 'GET':
        park_movements = ParkMovement.objects.all()
        data = []

        for movement in park_movements:
            plate = movement.vehicle_id.plate
            entry_date = movement.entry_date
            card_id = movement.vehicle_id.customer_id.card_id if movement.vehicle_id.customer_id and movement.vehicle_id.customer_id.card_id else None

            data.append({ "plate": plate, "entry_date": entry_date, 'card_id': card_id })

        return JsonResponse(data, safe=False)

    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def parkMovementEntry(request):
    if request.method == 'POST':
        new_vehicle = request.data

        try:
            vehicle = Vehicle.objects.get(plate=new_vehicle['plate'])

            park_movement_with_this_plate_already_exists = ParkMovement.objects.filter(vehicle_id=vehicle.id).exists()

            if not park_movement_with_this_plate_already_exists:
                customer = Customer.objects.filter(id=vehicle.customer_id)

                if customer.exists():
                    serializer = ParkMovement.objects.create(
                        entry_date=datetime.now, 
                        vehicle_id=vehicle.data,
                        value=50
                    )

                    if serializer.pk is not None:
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    else:
                        return Response({ "error": "cannot create park movement, please try again 1" }, status=status.HTTP_400_BAD_REQUEST)
                else:
                    serializer = ParkMovement.objects.create(
                        entry_date=datetime.now, 
                        vehicle_id=vehicle.data,
                        value=50
                    )

                    if serializer.pk is not None:
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    else:
                        return Response({ "error": "cannot create park movement, please try again 2" }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({ "error": "park movement with this plate already exists" }, status=status.HTTP_400_BAD_REQUEST)
        except Vehicle.DoesNotExist:
            serializer = Vehicle.objects.create(plate=new_vehicle['plate'])
            if serializer.pk is not None:
                park_movement = ParkMovement.objects.create(
                    entry_date=datetime.now, 
                    vehicle_id=serializer,
                    value=50
                )

                if park_movement.pk is not None:

                    serialized_data = {
                        "entry_date": park_movement.entry_date,
                        "vehicle_id": park_movement.vehicle_id.id,
                        "value": park_movement.value
                    }

                    returned_park_movement = ParkMovementSerializer(data=serialized_data)

                    if returned_park_movement.is_valid():
                        return Response(returned_park_movement.data, status=status.HTTP_201_CREATED)
                    else:
                        return Response({ "error": "Something was wrong... please try again" }, status=status.HTTP_400_BAD_REQUEST)

                else:
                    return Response({ "error": "cannot create park movement, please try again 3" }, status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def parkMovementExit(request):
    if request.method == 'POST':
        plate = request.data.get('plate')

        try:
            vehicle = Vehicle.objects.get(plate=plate)

            park_movement = ParkMovement.objects.filter(vehicle_id=vehicle)

            if park_movement.exists():
                park_movement = park_movement.first()
                customer = vehicle.customer_id

                customer_plan = CustomerPlan.objects.filter(customer_id=customer).first()

                if customer_plan:
                    park_movement.exit_date = datetime.now()
                    park_movement.save()
                    return Response({"message": "No charge required."}, status=status.HTTP_200_OK)

                contract = Contract.objects.filter(description="Contrato oficial para testes").first()

                current_time = timezone.now()
                entry_time = park_movement.entry_date
                time_difference = (current_time - entry_time).total_seconds() / 60

                contract_rule = ContractRule.objects.filter(contract_id=contract, until__gte=time_difference).order_by('until').first()

                if contract_rule:
                    if contract_rule.value > contract.max_value:
                        return Response({ "charge": contract.max_value }, status=status.HTTP_200_OK)
                    else:
                        return Response({ "charge": contract_rule.value }, status=status.HTTP_200_OK)
                else:
                    return Response({ "charge": contract.max_value }, status=status.HTTP_200_OK)

        except Vehicle.DoesNotExist:
            return Response({"error": "Vehicle with this plate doesn't exist."}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"error": "Bad request."}, status=status.HTTP_400_BAD_REQUEST)
