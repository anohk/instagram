import random

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from myuser.models import Myuser
from post.models import Post
from utils.test.member import make_dummy_users


class BaseTestCase(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def make_user_and_login(self):
        # 유저를 생성
        test_username = 'test_username'
        test_password = 'test_password'
        user = Myuser.objects.create_user(test_username, test_password)

        # 유저를 로그인 시킴
        self.browser.get(self.live_server_url + '/myuser/login/')
        input_username = self.browser.find_element_by_id('id_username')
        input_username.send_keys(test_username)
        input_password = self.browser.find_element_by_id('id_password')
        input_password.send_keys(test_password)
        input_password.send_keys(Keys.ENTER)

        return user


class NewVisitorTest(BaseTestCase):
    def test_first_visitor_redirect_to_signup(self):
        # 로그인하지 않은 유저가 myuser:signup으로 잘 이동했는지 확인
        self.browser.get(self.live_server_url)
        self.assertEqual(self.live_server_url + '/myuser/signup/', self.browser.current_url)

    def test_logged_in_user_redirect_to_post(self):
        # 로그인 한 유저가 post:list로 잘 이동했는지 확인
        self.make_user_and_login()

        # 이후 다시 root url로 요청
        self.browser.get(self.live_server_url)
        self.assertEqual(self.live_server_url + '/post/', self.browser.current_url)


class ProfileTest(BaseTestCase):
    """
    프로필 페이지에서의 동작을 테스트한다
    """

    def access_profile_page_and_check_status(self, status_name, num, unit):
        self.browser.get(self.live_server_url + '/myuser/profile')
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('{status_name} {num}{unit}'.format(
            status_name=status_name,
            num=num,
            unit=unit,
        ), page_text)

    def test_profile_display_status_post_count(self):
        # 테스트할 유저를 생성
        user = self.make_user_and_login()

        #  1에서 10중 임의의 개수로 Post 객체를 생성
        num = random.randrange(1, 10)
        for i in range(num):
            Post.objects.create(
                author=user,
            )

        self.access_profile_page_and_check_status(
            status_name='게시물',
            num=num,
            unit='개',
        )

    def test_profile_display_status_follower_count(self):
        user = self.make_user_and_login()
        users = make_dummy_users()

        num = random.randrange(1, 10)
        for i in range(num):
            users[i].follow(user)

        self.access_profile_page_and_check_status(
            status_name='팔로워',
            num=num,
            unit='명',
        )

    def test_profile_display_status_following_count(self):
        user = self.make_user_and_login()
        users = make_dummy_users()

        num = random.randrange(1, 10)
        for i in range(num):
            user.follow(users[i])

        self.access_profile_page_and_check_status(
            status_name='팔로우',
            num=num,
            unit='명',
        )
    #
    # # 프로필에 프로필 이미지가 잘 나오는지 테스트
    # def test_profile_display_profile_image(self):
    #     # 테스트 유저 생성
    #     user = self.make_user_and_login()
    #
    #     # 유저 프로필 이미지 등록
    #     c = Client()
    #     file = SimpleUploadedFile("file.png", "file_content", content_type='image')
    #
    #
    #     # 유저 프로필 접근
    #     self.browser.get(self.live_server_url + '/myuser/profile')
    #     page_text = self.browser.find_element_by_tag_name('body').text
    #
    #     # 유저 프로필 이미지가 HTML에서 보여지는지 확인

    # profile image 가 change 되는지 테스트
    # def test_change_profile_image(self):

