from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, reverse
from django.views import generic
from django.views.generic.edit import FormMixin
from .models import Post, Comment
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from .forms import CommentForm

class PostListView(generic.ListView):
    model = Post
    template_name = "posts.html"
    context_object_name = "posts"
    ordering = ['-pk']
    paginate_by = 3


class PostDetailView(FormMixin, generic.DetailView):
    model = Post
    template_name = "post.html"
    context_object_name = "post"
    form_class = CommentForm

    def get_success_url(self):
        return reverse("post", kwargs={'pk': self.object.pk})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.post = self.get_object()
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)


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