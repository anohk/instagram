from django.db import models

from instagram import settings
from myuser.models import Myuser

__all__ = (
    'Post',
    'PostLike',
)


# views/post.py에서 is_visible 조건을 만들었는데, 이런 조건들이 더 추가될 경우 쿼리셋을 매번 바꿔주는 게 힘들기 때문에 매니지에 설정해놓는다
class PostManager(models.Manager):
    def visible(self):
        return super().get_queryset().filter(is_visible=True)


class PostUserVisibleManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_visible=True)


class Post(models.Model):
    """
    1. Post모델에서 content 필드를 없애고 db migration
    2. post_add view에서 동작을 변경 (입력받은 content는 새 comment 객체를 생성하도록함)
    """

    # 사용자 유저 모델을 사용하는 경우에는 설정값을 가져다 써야한다 settings.AUTH_USER_MODEL
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    photo = models.ImageField(upload_to='post', blank=True)
    # content = models.TextField(max_length=300, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=True)
    like_users = models.ManyToManyField(
        Myuser,
        through='PostLike',
        related_name='like_post_set',
    )

    is_visible = models.BooleanField(default=True)
    # 포스트 삭제할 때 실제로 지우는게 아니라 보이는것만 해결하려고함.
    # 이케 처리하고 view에서 필터링함

    objects = PostManager()
    # default 매니저를 교체

    visibles = PostUserVisibleManager()
    # 커스텀 모델 매니저를 추가함
    # Post.visibles.all() 로 참조할 수 있다.
    # Post.obejcts.visible()

    def __str__(self):
        return 'Post{}'.format(self.id)

    class Meta:
        ordering = ('-id',)

    def toggle_like(self, user):
        # if user in self.like_users:
        #     self.like_post_set.remove(user)
        # else:
        #     self.like_users.create(user)
        # return self.like_post_set.remove(user)

        # return self.like_users.get_or_create(user)

        # 현재 인자로 전달된 user가 해당 Post(self)를 좋아요 한 적이 있는지 검사
        # 만약 이미 좋아요를 했을 경우 해당 내역을 삭제한다
        # 중간자 모델을 사용하기 때문에 self.like_users.remove()대신 아래 메서드를 사용한다
        # 없을 경우 생성해준다
        # pl_list = PostLike.objects.filter(post=self, user=user)
        pl_list = self.postlike_set.filter(user=user)

        # if pl_list.exists():
        #     pl_list.delete()
        # else:
        #     PostLike.objects.create(post=self, user=user)
        # 파이선 삼향연산자를 이용해 위의 4줄을 한줄로 표현할 수 있음

        # return PostLike.objects.create(post=self, user=user) if not pl_list.exists() else pl_list.delete()
        return self.postlike_set.create(user=user) if not pl_list.exists() else pl_list.delete()

    @property
    def like_count(self):
        return self.like_users.count()

    @property
    def comment_count(self):
        return self.comment_set.count()

    def add_comment(self, user, content):
        return self.comment_set.create(
            author=user,
            content=content,
        )


class PostLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    post = models.ForeignKey(Post)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            ('user', 'post'),
        )

    def __str__(self):
        return 'Post[{}]\'s Like[{}]'.format(
            # post.id 는 조인하고 가져옴
            self.post_id,
            self.id,
        )
