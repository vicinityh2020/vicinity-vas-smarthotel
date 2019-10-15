import uuid
import json
import requests
import rest_framework.status as status
from rest_framework.response import Response
from rest_framework.views import APIView

import logging
logger = logging.getLogger(__name__)
from datetime import datetime
from .thing_descriptors import *
from .utils import *
from .forms import ReservationForm
from django.views import View
from django.shortcuts import render
from django_eventstream import send_event


class ObjectsView(APIView):
    service_object_descriptor = {
        'adapter-id': ADAPTER_ID,
        'thing-descriptions': [
            {
                'oid': SMART_HOTEL_OID,
                'name': 'Dummy smart hotel for BARTER demo',
                'type': 'core:Service',
                'version': '0.1',
                'keywords': ['hotel', 'iot'],
                'properties': [HOTEL_INFO],
                'events': [],
                'actions': []
            }
        ]
    }

    def get(self, request):
        return Response(self.service_object_descriptor, status=status.HTTP_200_OK)


class SmartHotelView(APIView):

    def put(self, request, pid):
        input_data = request.data
        if pid not in PID:
            data = {
                'error': True,
                'message': 'Invalid PID',
                'status': status.HTTP_404_NOT_FOUND
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)

        if not input_data:
            data = {
                'error': True,
                'message': 'Missing input parameters',
                'status': status.HTTP_400_BAD_REQUEST
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        if pid == 'smart_hotel_dummy_iot_service':
            try:
                name = input_data['name']
            except Exception as e:
                logger.error(e)
                data = {
                    'error': True,
                    'message': 'Invalid input parameters',
                    'status': status.HTTP_400_BAD_REQUEST
                }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            output = dict()
            if name != "Demo hotel Novi Sad":
                data = {
                    'error': True,
                    'message': 'Unknown hotel',
                    'status': status.HTTP_400_BAD_REQUEST
                }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            output['name'] = "Demo hotel Novi Sad"
            output['address'] = "Brace Ribnikar 54"
            output['state'] = "Serbia"
            output['city'] = "Novi Sad"
        return Response(output, status=status.HTTP_200_OK)


class EventHandler(APIView):

    def put(self, request, iid, oid, eid):
        # Get info about reservation status from Smart Garage
        smart_garage_notification = request.data
        # Send info about parking reservation to frontend via channels
        send_event('parking_reservation', 'message', {
            'status': 'reserved',
            "payment_id": smart_garage_notification['payment_id'],
            "payment_address": smart_garage_notification['payment_address'],
            "payment_amount": smart_garage_notification['payment_amount']
        })
        return Response({}, status=status.HTTP_200_OK)


class LandingPage(View):
    def get(self, request):
        form = ReservationForm()
        return render(request, 'apis/hotel.html', {"form": form})

    def post(self, request):
        input_data = request.POST
        context = dict()
        context['checked_in'] = False
        context['parking_reserved'] = "No"
        try:
            name = input_data['name']
            email = input_data['email']
            valid_from = datetime.strptime(input_data['valid_from'], "%Y/%m/%d  %H:%M")
            valid_until = datetime.strptime(input_data['valid_until'], "%Y/%m/%d  %H:%M")
            reservation = input_data['reservation'] if 'reservation' in input_data else False
        except Exception as e:
            logger.error(e)
            return render(request, 'apis/hotel.html', {"output": context})

        if reservation:
            # call SmartGarage API service to reserve parking space
            url = 'http://localhost:9997/agent/remote/objects/{oid}/properties/reserve_parking'.format(
                oid=SMART_GARAGE_SERVICE_OID)
            headers = {'infrastructure-id': SMART_HOTEL_OID,
                       'adapter-id': ADAPTER_ID}
            body = {
                "name": name,
                "email": email,
                "valid_from": datetime.strftime(valid_from, "%m/%d/%Y  %H:%M:%S"),
                "valid_until": datetime.strftime(valid_until, "%m/%d/%Y  %H:%M:%S")
            }
            try:
                r = requests.put(url, headers=headers, data=json.dumps(body))
                result = r.json()
                logger.info("Payment information: {}".format(result))
                if result['error']:
                    return render(request, 'apis/hotel.html', {"output": context})
            except Exception as e:
                logger.error(e)
                return render(request, 'apis/hotel.html', {"output": context})
            # Subscribe to Smart Garage Events
            url = 'http://localhost:9997/agent/objects/{oid}/events/{eid}'.format(
                oid=SMART_GARAGE_SERVICE_OID, eid=SMART_GARAGE_EID)
            headers = {'infrastructure-id': SMART_HOTEL_OID,
                       'adapter-id': ADAPTER_ID}
            r = requests.post(url, headers=headers)
            logger.info("Subscription: {}".format(r.json()))

            # call API for sending amount to specified address
            url = 'http://localhost:9997/agent/remote/objects/{oid}/properties/send_payment'.format(
                oid=BARTER_DASH_SERVICE_OID)
            headers = {'infrastructure-id': SMART_HOTEL_OID,
                       'adapter-id': ADAPTER_ID}
            body = {
                "wallet_name": DASH_WALLET_NAME,
                "wallet_secret": DASH_WALLET_SECRET,
                "destination_address": result['message'][0]['payment_address'],
                "amount_duffs": result['message'][0]['payment_amount']*100000000,
                "instant_send": False
            }

            try:
                r = requests.put(url, headers=headers, data=json.dumps(body))
                result = r.json()
                logger.info("Payment sent: {}".format(result))
                if result['error']:
                    return render(request, 'apis/hotel.html', {"output": context})
            except Exception as e:
                logger.error(e)
                return render(request, 'apis/hotel.html', {"output": context})
            context['parking_reserved'] = "Pending"
        context['checked_in'] = True
        return render(request, 'apis/hotel.html', {"output": context})


class TestPage(APIView):
    def get(self, request):
        send_event('parking_reservation', 'message', {
            'status': 'reserved',
            "payment_amount": 0.20365478,
            "payment_address": "Testaddresssuhsvvhsfvasfvnb",
            "payment_id": "Testisdksvfsfnvvladfhvfvsfv",

        })
        return Response({"message": "test"}, status=status.HTTP_201_CREATED)