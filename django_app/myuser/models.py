from django.db import models, IntegrityError
from django.utils import timezone


class Myuser(models.Model):
    username = models.CharField('user name', max_length=30, unique=True)
    last_name = models.CharField('last name', max_length=30)
    first_name = models.CharField('first name', max_length=30)
    nickname = models.CharField('nickname', max_length=30)
    email = models.EmailField('email', max_length=100, blank=True, )
    date_joined = models.DateTimeField('date joined', auto_now_add=timezone.now())
    last_modified = models.DateTimeField('last modified', auto_now=timezone.now())
    following = models.ManyToManyField(
        'self',
        related_name='follower_set',
        symmetrical=False,
        blank=True,
    )

    def __str__(self):
        return self.username

    def follow(self, user):
        self.following.add(user)

    def unfollow(self, user):
        self.following.remove(user)

    @property
    def followers(self):
        return self.follower_set.all()

    def change_nickname(self, new_nickname):
        self.nickname = new_nickname
        self.save()

    @staticmethod
    def create_dummy_user(num):
        import random
        last_name_list = ['la', 'na', 'kim', 'jeon', 'park']
        first_name_list = ['alal', 'ella', 'hauen', 'dandan']
        nickname_list = ['aa', 'bb', 'cc']
        created_count = 0

        for i in range(num):

            try:
                Myuser.objects.create(
                    username='User{}'.format(i + 1),
                    last_name=random.choice(last_name_list),
                    first_name=random.choice(first_name_list),
                    nickname=random.choice(nickname_list),
                )
                created_count += 1
            except IntegrityError as e:
                print(e)

        return created_count

    @staticmethod
    def assign_global_variables():
        # sys모듈은 파이썬 인터프리터 관련 내장 모듈임
        import sys
        # __main__모듈을 module변수에 할당
        module = sys.modules['__main__']
        users = Myuser.objects.filter(username__startswith='User')
        for index, user in enumerate(users):
            setattr(module, 'u{}'.format(index + 1), user)



