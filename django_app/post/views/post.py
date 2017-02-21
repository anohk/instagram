from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from post.form import PostForm
from post.models import Post

# init에서 임포트했을 때 가져올 모든 것들을 써준다
__all__ = (
    'post_list',
    'post_detail',
    'post_add',
    'post_delete',
    'post_like_toggle',
)

"""
post list를 보여주는 화면을 구성

1. View에 post_list 함수 작성
2. template에 post_list.html 파일 작성
3. View에서 post_list.html을 render 한 결과를 리턴하도록 함
4. instagram/urls.py에 post/urls.py를 연결 app_name은 post
5. '/post/'로 접속했을 때 post_list View에 연결되도록 post/urls.py 에 내용을 작성
6. 전체 Post를 가져오는 쿼리셋을 context로 넘기도록 post_list뷰에 구현
7. post_list.html에서 {% for %}태그를 사용해 post_list의 내용을 순회하며 표현
"""


def post_list(request):
    # post = Post.objects.all()

    post = Post.visibles.all()
    # post를 모두 가져오는게 아니라 is_visible이 True인 것만 가져와서 리스트에 뿌려준다
    context = {
        'post_list': post,
    }

    return render(request, 'post/post_list.html', context)


"""
Post Detail (하나의 Post에 대한 상세화면
1. View에 post_detail함수 작성
2~4. 위와 같음
5. '/post/<숫자>/'로 접속했을 때 post_detail View에 연결되도록
    post/ursl.py에 내용작성
    이때, post_id라는 패턴명을 가지도록 정규 표현식 작성
6. url인자로 전달받은 post_id에 해당하는 Post객체를
    context에 넘겨 post_detail 화면을 구성

Post Detail에 댓글작성기능추가

1. request.method에 따라 로직 분리되도록 if/else 추가
2. request.method가 POST일 경우 request.POST에서 'content'키의 값을 가져옴
3. 현재 로그인한 유저는 request.user로 가져오며 Post의 id값은 post_id인자로 전달되므로 두 내용을 사용
4. 위내용과 content를 사용해서 Comment객체 생성 및 저장
5. Post detail로 redirect해준다
"""


def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    context = {
        'post': post,
    }
    return render(request, 'post/post_detail.html', context)


@login_required
def post_add(request):
    def create_post_comment(file, comment_content):
        post = Post(author=request.user, photo=file, )
        post.save()
        if comment_content != '':
            post.add_comment(user=request.user, content=comment_content, )

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('photo')
            comment_content = form.cleaned_data.get('content', '').strip()
            for file in files:
                create_post_comment(file, comment_content)

            return redirect('post:list')
    else:
        form = PostForm()

    context = {
        'form': form
    }
    return render(request, 'post/post_add.html', context)


@login_required
def post_delete(request, post_id, db_delete=False):
    if request.method == 'POST':
        post = Post.objects.get(id=post_id)
        if post.author.id == request.user.id:
            if db_delete:
                # db에서 정말 지우고 싶을 경우 db_delete=True로 지정해주면 지워진다
                post.delete()
            else:
                post.is_visible = False
            post.save()
            # post.delete()

        return redirect('post:list')


# def post_delete(request, post_id):
#     if request.method == 'POST':
#         post = Post.objects.get(id=post_id)
#         if post.author.id == request.user.id:
#             post.delete()
#             post.save()
#             # post.delete()
#
#         return redirect('post:list')

@login_required
def post_like_toggle(request, post_id):
    """
    1. post_detail.html에 form을 하나 더 생성
    2. 요청  view(url)가 post_like 가 되도록 함
    3. 요청받은후  적절히 PostLike 처리
    4. redirect
    :param request:
    :param post_id:
    :return:
    """
    if request.method == 'POST':
        post = Post.objects.get(id=post_id)
        post.toggle_like(user=request.user)
        return redirect('post:list')
