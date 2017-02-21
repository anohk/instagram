from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from post.models import Post
from .forms import LoginForm, ProfileImageForm, SignupModelForm, ChangeProfileImageModleForm

"""
request.method == POST일 때와
아닐때의 동작을 구분

POST일 때 로그인 로직 실행
GET일 때 member/login.html을 render해서 return하도록 함
"""


def login_view(request):
    if request.method == 'POST':
        # html파일에서 POST요청을 보내기 위해서
        # form을 작성하고 input 2개 name을
        # username,password로 설정
        # button type submit 실행

        form = LoginForm(data=request.POST)
        if form.is_valid():

            # 전달되어온 POST 데이터에서 username과 password키의 값들을 사용
            username = request.POST['username']
            password = request.POST['password']
            # authenticate의 인자로 POST로 전달받은 username, password 사용
            user = authenticate(username=username, password=password)

            # 인증이 정상적으로 완료되었다면
            # 해당하는 username, password에 일치하는 User객체가 존재할 경우
            if user is not None:
                # Dajgno의 인증관리 시스템을 이용해 세션을 관리해주기 위해 login()함수 사용
                login(request, user)
                return redirect('post:list')
                # return render(request, 'myuser/logout.html')
            # 인증에 실패했다면 username,password에 일치하는 User객체가 존재하지 않을 경우
            else:
                form.add_error(None, 'ID or PW incorrect')
                # return HttpResponse('Login failed')

    # GET method로 요청이 왔을 경우
    else:

        form = LoginForm()

    context = {
        'form': form,
    }
    return render(request, 'myuser/login.html', context)


#
# def signup_fbv(request):
#     """
#     1. myuser/signup.html
#     2. Signup Form 클래스 구현
#     3. 해당 form사용해서 signup.html 템플릿 구성
#     4. POST요청 받아서 MyUser 객체를 생성 후 로그인
#     5. 로그인이 완료되면 post_list뷰로 이동
#     :param request:
#     :return:
#     """
#     if request.method == 'POST':
#         form = SignupForm(request.POST)
#         if form.is_valid():
#             user = form.create_user()
#             login(request, user)
#             return redirect('post:list')
#
#     else:
#         form = SignupForm()
#     context = {
#         'form': form
#     }
#     return render(request, 'myuser/signup.html', context)


def signup_model_form_fbv(request):
    if request.method == 'POST':
        form = SignupModelForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('post:list')
    else:
        form = SignupModelForm()
    context = {
        'form': form
    }
    return render(request, 'myuser/signup.html', context)


@login_required
def profile(request):
    """
    자신의 게시물 수, 자신의 팔로워 수 사진의 팔로우 수를 context로 전달, 출력
    :param request:
    :return:
    """

    post_count = Post.objects.filter(author=request.user).count()
    follower_count = request.user.follower_set.count()
    following_count = request.user.following.count()
    profile_img = request.user.profile_img
    context = {
        'profile_img': profile_img,
        'post_count': post_count,
        'follower_count': follower_count,
        'following_count': following_count,

    }
    return render(request, 'myuser/profile.html', context)


# @login_required
# def change_profile_image(request):
#     """
#     해당 유저의 프로필 이미지를 바꾼다
#     0. 유저모델에 profile_img 필드 추가
#     1. change_profile_image.html  파일 작성
#     2. ProfileImageForm작성
#     3. 해당 Form을 템플릿에 렌더링
#     4. request.method == 'POST'일 때 request.FILES의 값을 이용해서
#     reqeust.user의 img_profile을 변경
#     5. 처리 완료 후 myuser:profile로 이동
#     6. profile.html에서 user의 프로필 이미지를 img태그를 사용해서 보여줌
#     """
#     if request.method == 'POST':
#         form = ProfileImageForm(request.POST, request.FILES)
#
#         if form.is_valid():
#             form = ChangeProfileImageModleForm(
#                 instance=request.user,
#                 data=request.FIELS,
#             )
#             form.save()
#
#             return redirect('myuser:profile')
#
#     else:
#         form = ChangeProfileImageModleForm()
#
#     return render(request, 'myuser/change_profile_image.html', {'form': form})


@login_required
def logout_fbv(request):
    logout(request)
    return redirect('myuser:login')
