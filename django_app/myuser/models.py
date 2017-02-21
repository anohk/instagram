from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class MyuserManager(BaseUserManager):
    def create_user(self, username, password=None):
        # 다른데에서 인증해주고 넘어오는 경우가 있기 때문에 password=None
        user = self.model(
            username=username
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password):
        user = self.model(
            username=username
        )

        # user = self.create_user(username)
        user.set_password(password)

        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class Myuser(PermissionsMixin, AbstractBaseUser):
    CHOICES_GENDER = (
        ('m', 'Male'),
        ('f', 'Female'),
    )

    # password =
    # last_login =
    # is_active =
    username = models.CharField(max_length=40, unique=True)
    email = models.EmailField(blank=True)
    gender = models.CharField(max_length=1, choices=CHOICES_GENDER)
    nickname = models.CharField(max_length=20)
    profile_img = models.ImageField(upload_to='profile_img', blank=True)
    # 팔로우 목록을 나타내는 필드 구현
    # 언제 팔로우를 했는지도 나타내도록 함(중간자 모델을 사용해야한다)
    following = models.ManyToManyField(
        'self',
        related_name='follower_set',
        symmetrical=False,
        blank=True,
        through='RelationShip',
    )

    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    objects = MyuserManager()

    def __str__(self):
        return self.username

    def get_full_name(self):
        return '{} ({})'.format(
            self.nickname,
            self.username,
        )

    def get_short_name(self):
        return self.nickname

    def follow(self, user):
        self.following_relations.create(
            to_user=user
        )

    def unfollow(self, user):
        self.following_relations.filter(
            to_user=user
        ).delete()


class RelationShip(models.Model):
    from_user = models.ForeignKey(Myuser, related_name='following_relations')
    to_user = models.ForeignKey(Myuser, related_name='follower_relations')
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            ('from_user', 'to_user'),
        )

    def __str__(self):
        return 'Relation from [{}] to [{}]'.format(
            self.from_user.username,
            self.to_user.username,
        )
