from django.test import TransactionTestCase


class ProfileViewTest(TransactionTestCase):
    # login_required는 로그인 하지 않았을 때 settings에서 설정한
    # LOGIN_URL = 'myuser:login'로 리다이렉트 해준다
    # 로그인 하지 않았을 때 로그인 뷰로 잘 보내주나 확인
    def test_user_not_authenticated_profile(self):
        # 로그인하지 않고 프로필 페이지로 접근
        url_profile = '/myuser/profile/'
        response = self.client.get(url_profile)
        self.assertRedirects(
            response,
            '/myuser/login/?next={}'.format(
                url_profile
            )
        )

    def test_user_not_authenticated_change_profile_image(self):
        # 로그인하지 않고 프로필 이미지 변경 페이지로 접근
        url_change_profile_image = '/myuser/change_profile_img/'
        response = self.client.get(url_change_profile_image)
        self.assertRedirects(
            response,
            '/myuser/login/?next={}'.format(
                url_change_profile_image
            )
        )

    def test_user_not_authenticated_logout(self):
        # 로그인하지 않고 로그아웃 페이지로 접근
        url_logout = '/myuser/logout/'
        response = self.client.get(url_logout)
        self.assertRedirects(
            response,
            '/myuser/login/?next={}'.format(
                url_logout
            )
        )




