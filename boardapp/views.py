from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import BoardModel
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse_lazy

# Create your views here.
def signupfunc(request):
    user2 = User.objects.get(username='taro')
    print(user2.email)
    if request.method == 'POST':
        username2 = request.POST['username']
        password2 = request.POST['password']
        # 重複してないかチェック
        try:
            User.objects.get(username=username2)
            return render(request, 'signup.html', {'error':'このユーザー名は既に使われています'})
        except:
            user = User.objects.create_user(username2, '', password2)
            return render(request, 'signup.html', {'some':100})

    return render(request, 'signup.html', {'some':100})

def loginfunc(request):
    if request.method == 'POST':
        username2 = request.POST['username']
        password2 = request.POST['password'] 
        user = authenticate(request, username=username2, password=password2)
        if user is not None:
            login(request, user)
            return redirect('list')
        else:
            return redirect('login')
    return render(request, 'login.html')

@login_required
def listfunc(request):
    # modelsで定義したfuncのデータを格納
    object_list = BoardModel.objects.all()
    # コンテキストで指定
    return render(request, 'list.html', {'object_list':object_list})

def logoutfunc(request):
    logout(request)
    return redirect('login')

# urlsで設定したprimary keyを引っ張っておかないといけない
def detailfunc(request, pk):
    object = BoardModel.objects.get(pk=pk)
    return render(request, 'detail.html', {'object':object})

def goodfunc(request, pk):
    post = BoardModel.objects.get(pk=pk)
    # post.goodは、objectのgoodのフィールドのデータ
    post.good += 1
    post.save()
    return redirect('list')

# readtextにユーザー名を格納しておいて、既読有無で処理を分ける
def readfunc(request, pk):
    post = BoardModel.objects.get(pk=pk)
    post2 = request.user.get_username()
    if post2 in post.readtext:
        return redirect('list')
    else:
        post.read += 1
        post.readtext = post.readtext + ' ' + post2
        post.save()
        return redirect('list')

class BoardCreate(CreateView):
    template_name = 'create.html'
    model = BoardModel
    fields = ('title', 'content', 'author', 'images')
    success_url = reverse_lazy('list')




