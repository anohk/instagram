from django.db import models

from myuser.models import Myuser


class Post(models.Model):
    author = models.ForeignKey(Myuser)
    photo = models.ImageField(upload_to='post', height_field=400, width_field=400, blank=True)
    content = models.TextField(max_length=300, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=True)
    like_users = models.ManyToManyField(
        Myuser,
        through='PostLike',
        related_name='like_post_set',
    )

    def __str__(self):
        return 'Post{}'.format(self.id)

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
        pl_list = PostLike.objects.filter(post=self, user=user)

        # if pl_list.exists():
        #     pl_list.delete()
        # else:
        #     PostLike.objects.create(post=self, user=user)
        # 파이선 삼향연산자를 이용해 위의 4줄을 한줄로 표현할 수 있음

        return PostLike.objects.create(post=self, user=user) if not pl_list.exists() else pl_list.delete()

    def add_comment(self, user, content):
        return self.comment_set.create(
            author=user,
            content=content,
        )

    @property
    def like_count(self):
        return self.like_users.count()

    @property
    def comment_count(self):
        return self.comment_set.count()


class Comment(models.Model):
    author = models.ForeignKey(Myuser)
    post = models.ForeignKey(Post)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Post[{}]\'s Comment[{}], Author[{}]'.format(
            self.post_id,
            self.id,
            self.author_id,
        )


class PostLike(models.Model):
    user = models.ForeignKey(Myuser)
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
