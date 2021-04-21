from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Category, Post, Subscribe, about
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, JsonResponse
from .utils import SendSubscribeMail
from django.db.models import Count 
from django.template.defaultfilters import slugify
from blog.forms import PostForm, ContactForm
from taggit.models import Tag






# Create your views here.



def index(request):
    posts = Post.objects.filter(roll_out=True).order_by('-publish')
    category = Category.objects.all().annotate(posts_count=Count('post'))
    about_me = about.objects.all()

    
    common_tags = Post.tags.most_common()[:4]

    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 3)  # 6 post per page
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)


    context = {'about_me':about_me,'category':category, 'page_obj':page_obj,'common_tags':common_tags, 'posts':posts}
     
    return render(request, "blog/index.html", context)


def post_detail(request, year, month, day, slug):
    post = get_object_or_404(Post, slug=slug,
                                   roll_out=True,
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)
    post_related = post.tags.similar_objects()
    about_me = about.objects.all()

    context = {'post': post, 'post_related': post_related, 'about_me':about_me}


    return render(request, 'blog/post_detail.html', context)


def subscribe(request):
    if request.method == 'POST':
        email = request.POST['email_id']
        email_qs = Subscribe.objects.filter(email_id = email)
        if email_qs.exists():
            data = {"status" : "404"}
            return JsonResponse(data)
        else:
            Subscribe.objects.create(email_id = email)
            SendSubscribeMail(email) # Send the Mail, Class available in utils.py
    return HttpResponse("/")



def tagged(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tags=tag)
    about_me = about.objects.all()


    paginator = Paginator(posts, 2)  # 6 post per page
    page = request.GET.get('page', 1)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {'posts':posts, 'tag':tag, 'page_obj':page_obj, 'about_me':about_me}
    
    return render(request, "blog/taggit.html", context)



def category_detail_views(request, category_slug):
    category = get_object_or_404(Category, category_slug=category_slug)
    posts = Post.objects.filter(category=category).order_by('-publish')
    about_me = about.objects.all()


    #category_post = []
    #for post in posts:
    #    if post.category.filter(category=category):
    #        category_post.append(post)
    
    paginator = Paginator(posts, 2)  # 6 post per page
    page = request.GET.get('page', 1)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    
    context = {'category':category, 'posts':posts, 'page_obj':page_obj,'about_me':about_me}
 

    return render(request, 'blog/category.html', context)

def aboutme(request):
    about_me = about.objects.all()


    return render(request, 'blog/about.html', {'about_me':about_me})

def contact(request):
    form = ContactForm()
    #if request.method == 'POST':
    #    form = ContactForm(request.POST)
    #    if form.is_valid():
    #        form.save()
    #        return redirect('contact')
    if request.is_ajax():
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({
                'msg':'success'
                
            })


    context = { 'form':form }

    return render(request, 'blog/contact.html', context) 
