from django.test import TransactionTestCase

from utils.test import make_dummy_post


class PostListViewTest(TransactionTestCase):
    def test_user_not_authenticated_post_add(self):
        url_post_add = '/post/add/'
        response = self.client.get(url_post_add)
        self.assertRedirects(
            response,
            '/myuser/login/?next={}'.format(
                url_post_add
            )
        )

    def test_user_not_authenticated_post_delete_on_exist_post(self):
        # 존재하는 포스트를 지우는 페이지에 접근

        post = make_dummy_post()

        url_post_delete = '/post/{}/delete/'.format(post.id)
        response = self.client.get(url_post_delete)
        self.assertRedirects(
            response,
            '/myuser/login/?next={}'.format(
                url_post_delete
            )
        )

    def test_user_not_authenticated_post_delete_on_does_not_exist_post(self):
        # 없는 포스트를  삭제하는 페이지에 접근
        ulr_post_delete = '/post/0/delete/'
        response = self.client.get(ulr_post_delete)
        self.assertRedirects(
            response,
            '/myuser/login/?next={}'.format(
                ulr_post_delete
            )
        )

    def test_user_not_authenticated_post_like_toggle(self):
        post = make_dummy_post()

        url_post_like_toggle = '/post/{}/like/toggle/'.format(post.id)
        response = self.client.get(url_post_like_toggle)
        self.assertRedirects(
            response,
            '/myuser/login/?next={}'.format(
                url_post_like_toggle
            )
        )
