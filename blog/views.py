from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.views.generic import (TemplateView, ListView, CreateView,
                                   DetailView, UpdateView, DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout

from .models import Post, Comment
from .forms import PostForm, PostUpdateForm,Comment_Form

# Create your views here.

#About View
class AboutTemplateView(TemplateView):
    template_name = 'blog/about.html'


# POST
class PostListView(ListView):
    model = Post

    #get query set
    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

class PostDetailView(DetailView):
    model = Post

    
class PostCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    # Play with redirect
    # redirect_field_name = 'post_detail.html' # Default: 'next'
    
    model = Post
    form_class = PostForm

class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    # redirect_field_name = 'post_detail.html' # Default: 'next'

    model = Post
    form_class = PostUpdateForm

class PostDeleteView(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    # redirect_field_name = 'post_detail.html' # Default: 'next'

    model = Post
    success_url = reverse_lazy('blog:post_list')

class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    # redirect_field_name = 'post_detail.html' # Default: 'next'
    
    model = Post
    template_name = 'blog/post_draft_list.html'

    
    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('-create_date')


######################################
######################################

@login_required
def publish_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('blog:post_detail', pk=pk)


@login_required
def add_comment_to_post(request, pk):
    print('PK:',pk)
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        comment_form = Comment_Form(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('blog:post_detail', pk=pk) 
    else:
        comment_form = Comment_Form()
    return render(request, 'blog/comment_form.html', {'form':comment_form})

@login_required
def approve_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('blog:post_detail', pk=comment.post.pk)

@login_required
def remove_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('blog:post_detail', pk=post_pk)


def login_view(request):
    next_url = request.GET.get('next', reverse('blog:post_list'))
    print(next_url)

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:

            if user.is_active:
                login(request, user)
                return redirect(next_url)
            else:
                return render(request, 'registration/login.html', {'error_msg': 'User not active!'}) 
        else:
            return render(request, 'registration/login.html', {'error_msg': 'User not found!'}) 
    else:
        return render(request, 'registration/login.html', {}) 

@login_required
def logout_view(request):
    
    logout(request)
    return HttpResponseRedirect(reverse('blog:post_list'))