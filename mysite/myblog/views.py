from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import generic
from .models import Post, Comment
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm

class PostListView(generic.ListView):
    model = Post
    template_name = "posts.html"
    context_object_name = "posts"
    ordering = ['-pk']
    paginate_by = 3


class PostDetailView(generic.DetailView):
    model = Post
    template_name = "post.html"
    context_object_name = "post"


def search(request):
    query = request.GET.get("query")
    posts = Post.objects.filter(Q(title__icontains=query) |
                                Q(content__icontains=query) |
                                Q(author__username__icontains=query))
    context = {
        "posts": posts,
        "query": query,
    }
    return render(request, template_name="search.html", context=context)


class UserPostListView(LoginRequiredMixin, generic.ListView):
    model = Post
    template_name = "user_posts.html"
    context_object_name = "posts"

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

class UserCommentListView(LoginRequiredMixin, generic.ListView):
    model = Comment
    template_name = "user_comments.html"
    context_object_name = "comments"

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user)

def register(request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect("login")
    return render(request, template_name="register.html", context={"form": form})