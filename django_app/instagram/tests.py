"""
1. index URL로 접근했을 때 로그인하지 않았을 경우 myuser:signup으로 가는지 확인
2. 위와 같은데 로그인 했을 경우 post:list로 가는지 확인
    2-1: 테스트용 유저를 생성
    2-2: 해당 유저 정보로 myuser:login 에 POST요청 (로그인
    2-3: 이후 테스트 실행
"""
import re

from django.test import LiveServerTestCase, Client

from myuser.models import Myuser


def remove_csrf(html_code):
    return re.sub(r'name=\'csrf.+', '', html_code)


class IndexTest(LiveServerTestCase):
    def setUp(self):
        self.client = Client()

    def tearDown(self):
        pass

    def test_user_is_not_authenticated_redirect_to_signup(self):
        response = self.client.get('/')
        self.assertRedirects(response, '/myuser/signup/')

    def test_user_is_authenticated_redirect_to_post_list(self):
        # 유저를 로그인 시킨다
        # 테스트용 유저를 생성한다(ORM)
        test_username = 'test_user'
        test_password = 'test_password'
        Myuser.objects.create_user(test_username, test_password)
        # myuser:login으로 POST요청을 보낸다 (self.client.post)
        self.client.post(
            '/myuser/login/',
            {
                'username': test_username,
                'password': test_password,
            }
        )
        # 이후 root url('/')의 response를 받아온다
        response = self.client.get('/')
        # 해당 response가 /post/로 잘 redirect되는지 확인
        self.assertRedirects(response, '/post/')
