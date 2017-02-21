from django.shortcuts import redirect


def index(request):
    """
    유저가 로그인 했을 경우 post:list로 이동
    로그인하지 않았을 경우 myuser:signup으로 이동
    :param request:
    :return:
    """
    if request.user.is_authenticated:
        return redirect('post:list')

    return redirect('myuser:signup')
