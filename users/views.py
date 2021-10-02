import json, re, requests, bcrypt, jwt, random

from django.views import View
from django.http  import JsonResponse
from datetime     import datetime, timedelta

from my_settings  import SECRET_KEY, ALGORITHM
from users.models import User

class SignUpView(View):
    def post(self, request):
        data           = json.loads(request.body)
        REGEX_EMAIL    = re.compile("^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
        REGEX_PASSWORD = re.compile("^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$") 

        password = data["password"]

        if User.objects.filter(email = data["email"]).exists():
            return JsonResponse({"MESSAGE" : "DUPLICATED EMAIL"}, status = 400)

        if not REGEX_EMAIL.match(data["email"]):
            return JsonResponse({"MESSAGE":"EMAIL_ERROR"}, status = 400)

        if not REGEX_PASSWORD.match(data["password"]):
            return JsonResponse({"MESSAGE" : "PASSWORD_ERROR"}, status = 400)
        
        hashed_password  = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        decoded_password = hashed_password.decode("utf-8")

        User.objects.create(
            name      = data["name"],
            birth_day = data["birth_day"], 
            email     = data["email"],
            password  = decoded_password
        )

        return JsonResponse({"MESSAGE" : "SUCCESS"}, status = 201)


class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            if not User.objects.filter(email = data["email"]).exists():
                return JsonResponse({"MESSAGE" : "INVALID_USER"}, status = 401)

            user = User.objects.get(email = data["email"])

            if not bcrypt.checkpw(data["password"].encode("utf-8"), user.password.encode("utf-8")):
                return JsonResponse({"MESSAGE": "INVALID_PASSWORD"}, status = 401)
            
            access_token = jwt.encode({"id": user.id , 'exp':datetime.utcnow() + timedelta(days=3)}, SECRET_KEY , algorithm="HS256")
            return JsonResponse({"MESSAGE" : "SUCCESS", 'token' : access_token, "user_name" : user.name}, status = 200)

        except KeyError:
            return JsonResponse({"MESSAGE" : "KEY_ERROR"}, status=400)


class KakaoSignInView(View):
    def post(self, request):
        try:
            access_token = request.headers["Authorization"]
            response     = requests.get('https://kapi.kakao.com/v2/user/me', headers = ({"Authorization" : f'Bearer {access_token}'})).json()
      
            email    = response["kakao_account"]["email"]
            name     = response["kakao_account"]["profile"]["nickname"]
            kakao_id = response["id"]

            birthday  = response["kakao_account"]["birthday"]
            age_range = response["kakao_account"]["age_range"]

            birth_min = int(list(age_range.split('~'))[0])
            birth_max = int(list(age_range.split('~'))[1])
            month     = birthday[:2]
            day       = birthday[2:] 
            
            birth_year = 2021-(random.randrange(birth_min, birth_max+1))
            print(birth_year)
            
            birth_day = f'{birth_year}-{month}-{day}'
            
            if User.objects.filter(kakao_id=kakao_id).exists():
                user  = User.objects.get(kakao_id = kakao_id)
                token = jwt.encode({"id" : user.id, 'exp':datetime.utcnow() + timedelta(days=3)}, SECRET_KEY, algorithm= ALGORITHM)

            if not User.objects.filter(kakao_id=kakao_id).exists():
                User.objects.create(
                    kakao_id  = kakao_id,
                    email     = email,
                    name      = name,
                    birth_day = birth_day
                )
                user  = User.objects.get(kakao_id = kakao_id)
                token = jwt.encode({"id" : user.id, 'exp':datetime.utcnow() + timedelta(days=3)}, SECRET_KEY, algorithm= ALGORITHM)
            
            return JsonResponse({"MESSASGE" :"로그인 성공!", 'token' : token}, status = 200)

        except KeyError:
            return JsonResponse({"MESSAGE":"KEY_ERROR"}, status = 400)
            
        except ValueError:
            return JsonResponse({"MESSAGE": "VALUE_ERROR"}, status = 400)
