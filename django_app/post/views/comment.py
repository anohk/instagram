from django.shortcuts import redirect

from post.form import CommentForm
from post.models import Comment, Post

__all__ = (
    'comment_add',
    'comment_delete',
)


def comment_add(request, post_id):
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            content = comment_form.cleaned_data['content']

            # POST에는 유저 정보가 항상 같이 온다
            user = request.user

            # if 'list' in request.POST:
            #     list_post_id = request.POST['list'][0]
            #     post = Post.objects.get(id=list_post_id)
            #     post.add_comment(user, content)
            #     return redirect('post:list')
            # else:
            post = Post.objects.get(id=post_id)
            post.add_comment(user, content)

        return redirect('post:list')

        # return redirect(redirect_path) if 'list' in request.POST else redirect(redirect_path, post_id=post_id)
        # else:
        #     comment_form = CommentForm()
        #
        # context = {
        #     'form': comment_form
        # }
        # return render(request, 'post/post_detail.html', context)


def comment_delete(request, comment_id, post_id):
    """
    1. post_detail.html 의 Comment표현 loop내부에 form을 생성
    2. 요청 view(url)가 comment_delete가 되도록 함
    3. 요청받은 후 처리
    4. redirect

    """
    if request.method == 'POST':
        comment = Comment.objects.get(id=comment_id)
        if comment.author.id == request.user.id:
            comment.delete()

        return redirect('post:list')
