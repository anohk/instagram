from .comment import *
from .post import *


# 패키지 안쪽에서 임포트해오는데 , post/urls.py에서 임포트할 때 views자체는 파일이 아니라 디렉토리이기 땜에 init에 어떤 메서드 어떤 속성을 가지고 있는지 써줘야한다
# 아니면 url에서 view.post.post_list라고 직접 써줘야함
