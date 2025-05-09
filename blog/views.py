from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
from django.contrib.auth.decorators import login_required
from django.forms.models import BaseModelForm
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,UpdateView,DeleteView)

from django.shortcuts import render,get_object_or_404
from django.contrib.auth.models import User
# Create your views here.
@login_required
def home(request):
    context={"posts":Post.objects.all()}
    return render(request,"blog/home.html",context) #HttpResponse("welcome")
def about(request):
    return render(request,"blog/about.html",{"title":"about"})


class PostListView(LoginRequiredMixin,ListView):
    model=Post    # if not add  template_name     it is search post__list
    template_name ="blog/home.html" #<app>/<model>_<viewtype>.html
    context_object_name="posts"
    ordering=["-date_posted"]
    paginate_by=10 #number of post show in html
    



class PostDetailView(DetailView): #    template_name_suffix = "_detail"
    model=Post
    # context_object_name  this not work  then object_name=object.
    


class PostCreateView(LoginRequiredMixin,CreateView):#    template_name_suffix = "_form" ex:post_form 
    model=Post 
    success_url="/" #with out this line  move to post_detail by get_absolute_url in  Post models
    fields=['title','content']
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.author=self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):#template_name_suffix = "_form" ex:post_form 
    model=Post  
    #   success_url="/" #with out this line  move to post_detail 
    fields=['title','content']
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.author=self.request.user
        return super().form_valid(form)    
    
    def test_func(self) -> bool | None: #UserPassesTestMixin
        post =self.get_object()
        if (self.request.user==post.author or self.request.user.is_superuser):
            return True
        return False
        


class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin, DeleteView):#   template_name_suffix = "_confirm_delete" ex:post_confirm_delete.html
    model=Post             #blog/post_confirm_delete.html if not found this path then error
    success_url="/"        #<app>/<model>_<viewtype>.html
    def test_func(self) -> bool | None:
        post =self.get_object()
        # print( self.request.user.is_superuser)
        if (self.request.user==post.author or self.request.user.is_superuser):
            return True
        return False

class UserPostListView(LoginRequiredMixin,ListView):  
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5 #number of post show in html

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')