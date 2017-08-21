from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator

from .models import Post

import uuid

def root(request):
    return render(request, 'pastebin_app/root.html', {})

def paste(request):
    if request.POST['name'] == '' or request.POST['name'] == None:
        if request.POST['content'] == '' or request.POST['content'] == None:
            error_message = 'Name and content cannot be blank'
        else:
            error_message = 'Name cannot be blank'
        return render(request, 'pastebin_app/root.html', { 'error_message': error_message })
    elif request.POST['content'] == '' or request.POST['content'] == None:
        error_message = 'Content cannot be blank'
        return render(request, 'pastebin_app/root.html', { 'error_message': error_message })

    post = Post(name=request.POST['name'],content = request.POST['content'])
    rand = str(uuid.uuid4())[:10]
    while Post.objects.filter(generated_url=rand):
        rand = str(uuid.uuid4())[:10]
    post.generated_url = rand
    post.save()
    return HttpResponseRedirect(reverse('show', args=(post.generated_url,)))

def search(request):
    '''if search without keyword, display all results'''
    post_list = Post.objects.filter(name__icontains=request.GET.get('name','')).order_by('-id')
    # if not post_list:
    #     return render(request, 'pastebin_app/search.html', { 'posts': posts })
    page = request.GET.get('page',1)
    paginator = Paginator(post_list, 5)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'pastebin_app/search.html', { 'posts': posts })

def show(request,rand_url):
    post = get_object_or_404(Post, generated_url=rand_url)
    return render(request, 'pastebin_app/show.html', {'post':post})

def delete(request,rand_url):
    post = get_object_or_404(Post, generated_url=rand_url)
    post.delete()
    return HttpResponseRedirect(reverse('root'))