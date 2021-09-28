from uuid import uuid4
import json, jwt

from django.test import TestCase, Client

from users.models    import User
from movies.models   import Movie, Theater, MovieTheater
from bookings.models import Booking, SeatNumber
from my_settings     import SECRET_KEY, ALGORITHM

class BookingTest(TestCase):
    def setUp(self):
        #유저 정보 bulk_create
        User.objects.bulk_create(
            [
                #POST METHOD를 테스트하기 위한 1번 유저
                User(
                    id           = 1,
                    password     = 'abcd1234',
                    email        = 'ggg@gmail.com',
                    birth_day    = '1999-8-8',
                    name         = '위코더',
                    phone_number = '010-9999-9999',
                    kakao_id     = 'kakaotalk'
                ),
                #GET METHOD를 테스트하기 위한 2번 유저
                User(
                    id           = 2,
                    password     = 'qwerty1353',
                    email        = 'wecode@gmail.com',
                    birth_day    = '1991-5-8',
                    name         = '김코더',
                    phone_number = '010-1111-2222',
                    kakao_id     = 'sorry'
                ),
                #GET METHOD를 테스트하기 위한 3번 유저
                User(
                    id           = 3,
                    password     = 'passpass',
                    email        = 'ht@gmail.com',
                    birth_day    = '1994-6-10',
                    name         = '송코더',
                    phone_number = '010-5678-1234',
                    kakao_id     = 'realkakao'
                )
            ]
        )

        self.access_token1, self.access_token2, self.access_token3 = (
            jwt.encode({'id' : User.objects.get(id = i).id}, SECRET_KEY, ALGORITHM) for i in range(1,4)
        )

        #영화 정보 bulk_create
        Movie.objects.bulk_create(
            [
                Movie(
                    id             = 1,
                    ko_name        = '헬리콥터와 마법사의 똥',
                    en_name        = "Helicopter and magician's foo",
                    release_date   = '2021-9-15',
                    close_date     = '2021-12-14',
                    screening_type = '2D',
                    running_time   = 145,
                    age_grade      = 12,
                    rating         = 1.5,
                    description    = '정말 신나는 똥쟁이 마법사의 대모험',
                    total_audience = 2
                ),
                Movie(
                    id             = 2,
                    ko_name        = '기저귀',
                    en_name        = "Miracle",
                    release_date   = '2021-9-14',
                    close_date     = '2021-12-13',
                    screening_type = '2D',
                    running_time   = 1600,
                    age_grade      = 12,
                    rating         = 9.9,
                    description    = '똥냄새나는 기저귀',
                    total_audience = 200
                ),
            ]
        )

        #영화관 정보 create
        Theater.objects.create(
            id       = 1,
            location = '강남'
        )

        #영화관에서 상영하는 영화정보 bulk_create
        MovieTheater.objects.bulk_create(
            [
                MovieTheater(
                    id         = 1,
                    movie_id   = 1,
                    theater_id = 1,
                    start_time = '2021-9-18 17:50'
                ),
                MovieTheater(
                    id         = 2,
                    movie_id   = 2,
                    theater_id = 1,
                    start_time = '2021-9-19 12:50'
                ),
            ]
        )

        #예매 내역 bulk_create
        Booking.objects.bulk_create(
            [
                #POST METHOD를 테스트하기 위한 예매 정보
                #예매가 완료된 좌석을 예매하는 경우를 test하기 위한 SeatNumber의 Foreignkey로 사용
                Booking(
                    id               = 2,
                    user_id          = 1,
                    booking_number   = uuid4().hex,
                    movie_theater_id = 1,
                    price            = 2,
                    adult            = 1,
                    teenager         = 1,
                    kid              = 1
                ),
                #GET METHOD를 테스트하기 위한 예매 정보
                Booking(
                    id               = 3,
                    user_id          = 2,
                    booking_number   = '11111111', #임의의 예매 번호라고 가정
                    movie_theater_id = 1,
                    price            = 13000,
                    adult            = 2,
                    teenager         = 1,
                    kid              = 1
                ),
                #GET METHOD를 테스트하기 위한 예매 정보
                Booking(
                    id               = 4,
                    user_id          = 2,
                    booking_number   = '22222222', #임의의 예매 번호라고 가정
                    movie_theater_id = 2,
                    price            = 10000,
                    adult            = 1,
                    teenager         = 1,
                    kid              = 1
                )
            ]
        )

        #POST METHOD를 테스트하기 위한 좌석 번호 create(이미 예매가 완료된 좌석인지 확인)
        SeatNumber.objects.create(
            id          = 5,
            booking_id  = 2,
            seat_number = 'B1'
        )

        #GET METHOD를 테스트하기 위한 좌석 번호 bulk_create
        SeatNumber.objects.bulk_create(
            [
                SeatNumber(
                    id          = 10,
                    booking_id  = 3,
                    seat_number = 'C1'
                ),
                SeatNumber(
                    id          = 11,
                    booking_id  = 3,
                    seat_number = 'C2'
                ),
                SeatNumber(
                    id          = 12,
                    booking_id  = 3,
                    seat_number = 'C3'
                ),
                SeatNumber(
                    id          = 13,
                    booking_id  = 3,
                    seat_number = 'C4'
                ),
                SeatNumber(
                    id          = 14,
                    booking_id  = 4,
                    seat_number = 'D1'
                ),
                SeatNumber(
                    id          = 15,
                    booking_id  = 4,
                    seat_number = 'D2'
                ),
                SeatNumber(
                    id          = 16,
                    booking_id  = 4,
                    seat_number = 'D3'
                ),
            ]
        )

    def tearDown(self):
        User.objects.all().delete()
        Movie.objects.all().delete()
        Theater.objects.all().delete()
        MovieTheater.objects.all().delete()
        SeatNumber.objects.all().delete()
        Booking.objects.all().delete()

    #POST METHOD 요청시 성공 case
    def test_bookingview_post_success(self):
        client       = Client()
        header       = {'HTTP_Authorization' : self.access_token1}
        booking_view = {
            'movie_id'    : 1,
            'theater_id'  : 1,
            'start_time'  : '2021-09-18 17:50',
            'price'       : 10000,
            'adult'       : 3,
            'teenager'    : 1,
            'kid'         : 0
        }
        response = client.post('/bookings?seat-number=Z1&seat-number=Z2&seat-number=Z3&seat-number=Z4', json.dumps(booking_view), content_type = 'application/json', **header)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(),{
            'MESSAGE' : 'CREATED'
        })

    #POST METHOD 요청시 실패 case(영화관 또는 영화 데이터가 존재하지 않을 때)
    def test_bookingview_post_fail_does_not_exists(self):
        client       = Client()
        header       = {'HTTP_Authorization' : self.access_token1}
        booking_view = {
            'movie_id'    : 5,
            'theater_id'  : 1,
            'start_time'  : '2021-09-20 09:00',
            'price'       : 10000,
            'adult'       : 3,
            'teenager'    : 1,
            'kid'         : 0
        }
        response = client.post('/bookings?seat-number=A1&seat-number=A2&seat-number=A3&seat-number=A4', json.dumps(booking_view), content_type = 'application/json', **header)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),{'MESSAGE' : 'MOVIE OR THEATER DOES NOT EXISTS'})

    #POST METHOD 요청시 실패 case(데이터가 누락되어 요청되었을 때)
    def test_bookingview_post_fail_key_error(self):
        client       = Client()
        header       = {'HTTP_Authorization' : self.access_token1}
        booking_view = {
            'theater_id'  : 1,
            'price'       : 10000,
            'adult'       : 3,
            'teenager'    : 1,
            'kid'         : 0
        }
        response = client.post('/bookings?seat-number=A1&seat-number=A2&seat-number=A3&seat-number=A4', json.dumps(booking_view), content_type = 'application/json', **header)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),{'MESSAGE' : 'KEY ERROR'})

    #POST METHOD 요청시 실패 case(유효하지 않은 값이 입력되었을 때)
    def test_bookingview_post_fail_value_error(self):
        client       = Client()
        header       = {'HTTP_Authorization' : self.access_token1}
        booking_view = {
            'movie_id'    : 'a',
            'theater_id'  : 1,
            'start_time'  : '2021-09-20 09:00',
            'price'       : 10000,
            'adult'       : 3,
            'teenager'    : 1,
            'kid'         : 0
        }
        response = client.post('/bookings?seat-number=A1&seat-number=A2&seat-number=A3&seat-number=A4', json.dumps(booking_view), content_type = 'application/json', **header)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),{'MESSAGE' : 'VALUE ERROR'})

    #POST METHOD 요청시 실패 case(이미 예매가 완료된 좌석을 예매하려고 할 때)
    def test_bookingview_post_fail_seatnumbers_already_exist(self):
        client       = Client()
        header       = {'HTTP_Authorization' : self.access_token1}
        booking_view = {
            'movie_id'    : 1,
            'theater_id'  : 1,
            'price'       : 10000,
            'adult'       : 3,
            'teenager'    : 1,
            'kid'         : 0
        }
        response = client.post('/bookings?seat-number=A1&seat-number=B1&seat-number=A3&seat-number=A4', json.dumps(booking_view), content_type = 'application/json', **header)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),{'MESSAGE' : 'ALREADY EXISTS'})

    #POST METHOD 요청시 실패 case(인원 수와 좌석 수가 일치하지 않을 때)
    def test_bookingview_post_fail_the_number_of_seats_does_not_matched(self):
        client       = Client()
        header       = {'HTTP_Authorization' : self.access_token1}
        #access_token = header['HTTP_Authorization']
        #user_id      = jwt.decode(access_token)['id']
        booking_view = {
            'movie_id'    : 1,
            'theater_id'  : 1,
            'start_time'  : '2021-09-18 17:50',
            'price'       : 10000,
            'adult'       : 3,
            'teenager'    : 1,
            'kid'         : 0
        }
        response = client.post('/bookings?seat-number=A1&seat-number=A2&seat-number=A3', json.dumps(booking_view), content_type = 'application/json', **header)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),{
            'MESSAGE' : 'THE NUMBER OF SEATS DOES NOT MATCHED'
        })

    #GET METHOD 요청시 성공 case
    def test_bookingview_get_booking_history_success(self):
        client       = Client()
        header       = {'HTTP_Authorization' : self.access_token2}
        response     = client.get('/bookings/histories', **header)
        self.maxDiff = None
        self.assertEqual(response.json(),{
            'history' : [
                {
                    "korean_name"    : '헬리콥터와 마법사의 똥',
                    "english_name"   : "Helicopter and magician's foo",
                    "booking_number" : '11111111',
                    "start_time"     : '2021-09-18T17:50:00',
                    "seat_number"    : ['C1','C2','C3','C4'],
                    "adult"          : 2,
                    "teenager"       : 1,
                    "kid"            : 1,
                    "price"          : 13000
                },
                {
                    "korean_name"    : '기저귀',
                    "english_name"   : "Miracle",
                    "booking_number" : '22222222',
                    "start_time"     : '2021-09-19T12:50:00',
                    "seat_number"    : ['D1','D2','D3'],
                    "adult"          : 1,
                    "teenager"       : 1,
                    "kid"            : 1,
                    "price"          : 10000
                }
            ]
        }
        )
        self.assertEqual(response.status_code, 200)

    #GET METHOD 요청시 실패 case(예매 정보가 없을 때)
    def test_bookingview_get_booking_history_fail_booking_histories_does_not_exist(self):
        client   = Client()
        header   = {'HTTP_Authorization' : self.access_token3}
        response = client.get('/bookings/histories', **header)
        self.assertEqual(response.json(),{'MESSAGE' : 'HISTORY DOES NOT EXISTS'})
        self.assertEqual(response.status_code, 400)
    