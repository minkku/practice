from django.shortcuts import render

# Create your views here.
import json

from django.http import JsonResponse
from django.views import View

from owners.models import Owner, Dog

class OwnerList(View):
    def post(self, request) :
        data    = json.loads(request.body)

        owner_name = data["name"]
        owner_email = data["email"]
        owner_age = data["age"]

        Owner.objects.create(
            name = owner_name,
            email = owner_email,
            age = owner_age
        )

        return JsonResponse({ 'message': '너가 해라. 주인. ' }, status=201)

class DogList(View):
    def post(self, request) :
        data    = json.loads(request.body)

        dog_name = data["name"]
        dog_age = data["age"]
        owner = Owner.objects.get(name=data["owner"])

        Dog.objects.create(
            name = dog_name,
            age = dog_age,
            owner = owner
        )
        
        return JsonResponse({'message': '니가 주인이가? '}, status=201)

    def get(self, request) :
        dogs = Dog.objects.all()
        result = []

        for dog in dogs :
            result.append(
                {
                    "이름" : dog.name,
                    "나이" : dog.age,
                    "주인" : dog.owner.name
                }
            )
        
        return JsonResponse({ '갱쥐 정보': result }, status=200)