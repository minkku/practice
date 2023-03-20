from django.shortcuts import render

# Create your views here.
import json

# JSON으로 데이터를 다시 바꿔 응답하기 위한 모듈
from django.http import JsonResponse
from django.views import View

# 모델에서 정의한 class들 가져오기
from owners.models import Owner, Dog

class OwnerList(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            owner_name = data["name"]       # 배열 안에 있는 str은 테이블 안에 명시되어 있는 컬럼 명을 뜻한다. 
            owner_email = data["email"]
            owner_age = data["age"]

            # Owner 테이블에 데이터를 생성하는 코드
            Owner.objects.create(
                name=owner_name,
                email=owner_email,
                age=owner_age
            )
            return JsonResponse({ 'message': 'Owner created successfully.' }, status=201)
        except KeyError:
            return JsonResponse({ 'message': 'Invalid input.' }, status=400)

    def get(self, request):
        try:
            owners = Owner.objects.all()
            results = []

            for owner in owners:
                dog_list = [
                    {
                        "이름": dog.name,
                        "나이": dog.age
                    } for dog in Dog.objects.filter(owner=owner)
                ]

                results.append(
                    {
                        "이름": owner.name,
                        "이메일": owner.email,
                        "나이": owner.age,
                        "강아지": dog_list
                    }
                )

            return JsonResponse({'주인+강아지 리스트': results}, status=200)
        except:
            return JsonResponse({'message': 'Something went wrong.'}, status=500)


class DogList(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            dog_name = data["name"]
            dog_age = data["age"]
            owner_id = data["owner"]

            # owner_id로 Owner 모델에서 owner 객체 가져오기
            owner = Owner.objects.get(id=owner_id)

            Dog.objects.create(
                name=dog_name,
                age=dog_age,
                owner=owner # owner_id 대신 owner 필드 사용
            )
            return JsonResponse({'message': 'Dog created successfully.'}, status=201)
        except KeyError:
            return JsonResponse({'message': 'Invalid input.'}, status=400)
        except Owner.DoesNotExist:
            return JsonResponse({'message': 'Owner does not exist.'}, status=404)



    def get(self, request):
        try:
            dogs = Dog.objects.all()
            result = []

            for dog in dogs:
                result.append(
                    {
                        "이름": dog.name,
                        "나이": dog.age,
                        "주인": dog.owner.name
                    }
                )

            return JsonResponse({ '강아지 정보': result }, status=200)
        except:
            return JsonResponse({'message': 'Something went wrong.'}, status=500)
