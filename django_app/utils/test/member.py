from myuser.models import Myuser
from post.models import Post

__all__ = (
    'make_dummy_users', 'make_dummy_post'
)

def make_dummy_user(username):
    password = 'test_password'
    user = Myuser.objects.create_user(username, password)
    return user

def make_dummy_users():
    users = []
    for i in range(10):
        user = make_dummy_user('username{}'.format(i + 1))
        users.append(user)
    return users


def make_dummy_post():
    # 유저를 생성
    user = make_dummy_user("username")

    # 생성한 유저가 작성한 포스트를 하나 생성
    # author = user.id
    post = Post.objects.create(author=user)
    return post