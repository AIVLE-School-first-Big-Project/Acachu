from datetime import datetime
from django.urls import reverse
from django.http import HttpResponseRedirect,Http404
from django.shortcuts import redirect, render,get_object_or_404
from pymysql import NULL
from main.models import *
from .forms import *
from django.core.paginator import Paginator

# Create your views here.
def Aut(request):
    if request.method == 'GET':
        page = int(request.GET.get("page",1))
        user_id = request.session['user_id']
        store_info = StoreAuth.objects.get(user_id = user_id)
        user_info=User.objects.get(user_id=user_id)
        store = Store.objects.get(store_id = store_info.store_id)
        review = Review.objects.filter(store_id = store_info.store_id).order_by('-review_reg_date')[:6] # 리뷰 6개
        tags = StoreTag.objects.filter(store_id = store_info.store_id)[:20]
        boards = AuthBoard.objects.filter(user_id = user_info.user_id).order_by('-ab_id') #글
        paginator = Paginator(boards,10) # 글 10개
        posts = paginator.get_page(page) # url에 있는 현재 page값 get_page로 전달

        return render(request,'AuthManagedPage\AuthManagedPage.html',
                      {'store_id':store_info.store_id,
                        'store':store,
                        'reviews':review,
                        'tags':tags,
                        'boards':boards,
                        'posts':posts
                       }
                    )

def post(request): #글작성
    if request.method=='POST':
        post = AuthBoard()
        post.ab_title = request.POST['title']
        post.ab_content = request.POST['content']        
        post.ab_reg_date = datetime.now()
        post.ab_reply_yn = 0
        post.user_id = request.session['user_id']
        post.save()

        img_list = request.FILES.getlist('ab_img')
        for img in img_list:
            imgs = Authpicture.objects.create(authpicture_img=img,ab_id=post.ab_id)
            imgs.save()
            
        return redirect('/../authmanaged/')
    return render(request,'AuthManagedPage\post.html')

def contents(request, id): # 글 작성 후 확인
    try:
        board = AuthBoard.objects.get(pk=id)
        imgs = Authpicture.objects.filter(ab_id = id) # 이미지
        reply = Reply.objects.filter(authboard_id=id)
        Replyform = ReplyForm()
    except AuthBoard.DoesNotExist:
        raise Http404("Does not exist!")
    return render(request, 'AuthManagedPage\contents.html',
                    {
                        'board':board,
                        'imgs':imgs,
                        'replys':reply,
                        'replyform':Replyform
                    })

def contents_update(request,id): #수정기능
    up_post = AuthBoard.objects.get(ab_id=id)
    up_img =  Authpicture.objects.filter(ab_id = id)
    if request.method == "POST":
        up_post.ab_title = request.POST['title']
        up_post.ab_content = request.POST['content']
        up_post.ab_reg_date = up_post.ab_reg_date
        up_post.save()

        ncheck = request.POST['check']

        if ncheck == "":
            up_img.delete()

        img_list = request.FILES.getlist('ab_img')
        for img in img_list:
            up_img = Authpicture.objects.create(authpicture_img=img,ab_id=up_post.ab_id)
            up_img.authpicture_img = img
            up_img.save()

        return redirect('/post/'+str(id),{'board':up_post}) 
    else:
        up_post = AuthBoard.objects.get(ab_id=id)
        up_img = Authpicture.objects.filter(ab_id = id)
        return render(request,'AuthManagedPage/update.html',{'board':up_post, 'imgs':up_img})


def contents_delete(request,id): #삭제
    del_post = AuthBoard.objects.get(pk=id)
    del_post.delete()
    return redirect('/../authmanaged/')

def new_reply(request,id):
    form = ReplyForm(request.POST)
    ab = AuthBoard.objects.get(pk = id)

    if form.is_valid():
        user_id = request.session['user_id']
        content = form.data['reply_content']
        AuthBoard.objects.update()
        Reply.objects.create(
                                reply_content = content,
                                reply_date = datetime.now(),
                                user_id = user_id,
                                authboard_id = id
                            )
        ab.ab_reply_yn = 1
        ab.save()
    return redirect('/post/'+str(id))

def edit_storeprofile(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        store_info = StoreAuth.objects.get(user_id = user_id)
        store = Store.objects.get(store_id = store_info.store_id)
        img = request.FILES['upload_file1']
        store.store_image = img
        store.save()
        return redirect('/authmanaged')