from django.shortcuts import render,get_object_or_404,redirect
from blog.forms import CreatePostForm, EditPostForm
from .models import Post, Category, User
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, user_passes_test
# Create your views here.


def post_list(request):
    posts = Post.objects.all().order_by('-published_date')
    categories = Category.objects.all()
    
    paginator = Paginator(posts, 9)
    page = request.GET.get('page',1) #sayfadan 'page' değeri geliyorsa al, gelmiyorsa 1 al. bu satır şuan hangi sayfada olduğumuzu alır.
    page_obj = paginator.get_page(page)
    
    '''print(page_obj.paginator.num_pages) #postlar toplam kaç sayfaya dağitildi?
    print(page_obj.paginator.count) #toplam kaç tane post var?'''
    
    return render(request, 'blog/post_list.html', {'page_obj':page_obj, 'categories':categories})


def post_details(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'blog/post_details.html', {'post':post})


def home(request):
    return render(request, 'blog/index.html')


def get_posts_by_category(request, slug):
    categories = Category.objects.all()
    posts = Post.objects.filter(category__slug = slug).order_by('-published_date')
    
    paginator = Paginator(posts, 9)
    page = request.GET.get('page',1) #sayfadan 'page' değeri geliyorsa al, gelmiyorsa 1 al. bu satır şuan hangi sayfada olduğumuzu alır.
    page_obj = paginator.get_page(page)
    
    
    return render(request, 'blog/post_list.html', context={'categories':categories, 'page_obj':page_obj, 'selected_category':slug})


def post_search(request):
    if 'q' in request.GET and request.GET['q'] != '':
        q = request.GET['q']
        categories = Category.objects.all()
        posts = Post.objects.filter(is_active=True, title__contains=q).order_by('-published_date')
    else:
        return redirect("/posts")    
    
    return render(request, 'blog/search.html', context={'categories':categories, 'posts':posts})


#kullanıcı admin ise ve login durumundaysa true döndürür ve method çalışır, admin değilse veya login değilse false döndürür ve method çalışmaz
def is_admin(user): 
    if user.is_authenticated and user.is_superuser:
        return True
    else:
        return False
    

@user_passes_test(is_admin, login_url='/accounts/login') # parametre true ise method çalışır, değilse çalışmaz ve login sayfasına yönlendirir.
def add_post(request):   
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/posts')
    else:
        form = CreatePostForm()
    return render(request, 'blog/add_post.html', context={'form':form})



@user_passes_test(is_admin, login_url='/accounts/login')
def post_operations(request):
    posts = Post.objects.all()
    return render(request, 'blog/post_op.html', {'posts':posts})



def post_edit(request, id):
    post = get_object_or_404(Post, id=id)
    
    if request.method == 'POST':
        form = EditPostForm(request.POST, request.FILES, instance=post)
        form.save()
        return redirect('/post-operations')
    else:
        form = EditPostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form':form, 'id':id, 'img':post.image.url})



def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        post.delete()
        return redirect('/post-operations')
    
    return render(request, 'blog/post_delete.html', {'post':post})
