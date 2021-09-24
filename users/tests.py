from django.test import TestCase, Client
from unittest.mock import MagicMock, patch

from .models import User

class KakaoLoginTest(TestCase):

    def setUp(self):
        User.objects.create(
            id           = 2,
            email        = 'twotwo@kakao.com',
            birth_day    = '2002-02-02',
            phone_number = '010-2222-2222',
            name         = '두번째님',
            kakao_id     = '222222222',
        )
    

    def tearDown(self):
        User.objects.all().delete()
    

    @patch("users.views.requests")
    def test_kakao_signin_success(self, mocked_requests):
        client = Client()
        class MockedResponse:
            def json(self):
                return {
                    "id": 222222222,
                    "kakao_account": {
                        "profile"   : {"nickname": "두번째님"},
                        "email"     : "twotwo@kakao.com",
                        "age_range" : "20~29",
                        "birthday"  : "0202",
                        }
                    }

        mocked_requests.get = MagicMock(return_value = MockedResponse())
        headers             = {"HTTP_Authorization": "Fake_access_token"}
        response            = client.post("/users/sign-in/kakao", content_type = 'application/json' , **headers)
        self.assertEqual(response.status_code, 200)


    @patch("users.views.requests")
    def test_kakao_login_fail(self, mocked_requests):
        client   = Client()
        class MockedResponse:
            def json(self):
                return {
                }
        mocked_requests.get = MagicMock(return_value = MockedResponse())
        headers  = {"HTTP_Authorization" : "Fake_access_token"}
        response = client.post('/users/sign-in/kakao', content_type='application/json', **headers)
        self.assertEqual(response.status_code, 400)  
        