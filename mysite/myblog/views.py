from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, reverse
from django.views import generic
from django.views.generic.edit import FormMixin
from django.contrib import messages
from .models import Post, Comment
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from .forms import (CommentForm,
                    CustomUserChangeForm,
                    ProfileUpdateForm,
                    CustomUserCreateForm)
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

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
    form = CustomUserCreateForm(request.POST or None)
    if request.method == "POST":
        new_email = request.POST['email']
        if User.objects.filter(email=new_email).exists():
            messages.error(request, f'Vartotojas su el. paštu {form.instance.email} jau užregistruotas!')
            return redirect("register")
    if form.is_valid():
        form.save()
        return redirect("login")
    return render(request, template_name="register.html", context={"form": form})

@login_required
def profile(request):
    u_form = CustomUserChangeForm(request.POST or None, instance=request.user)
    p_form = ProfileUpdateForm(request.POST or None, request.FILES or None, instance=request.user.profile)
    if request.method == "POST":
        new_email = request.POST['email']
        if new_email and request.user.email != new_email and User.objects.filter(email=new_email).exists():
            messages.error(request, f'Vartotojas su el. paštu {u_form.instance.email} jau užregistruotas!')
            return redirect("profile")
    if u_form.is_valid() and p_form.is_valid():
        u_form.save()
        p_form.save()
        messages.info(request, f'Vartotoją paredagavome!')
        return redirect("profile")
    return render(request, template_name="profile.html", context={"u_form": u_form, "p_form": p_form})


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    template_name = "post_form.html"
    fields = ['title', 'content', 'image']
    success_url = reverse_lazy('posts')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Post
    template_name = "post_form.html"
    fields = ['title', 'content', 'image']

    def get_success_url(self):
        return reverse("post", kwargs={"pk": self.object.pk})

    def test_func(self):
        return self.get_object().author == self.request.user


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Post
    template_name = "post_delete.html"
    context_object_name = "post"
    success_url = reverse_lazy("posts")

    def test_func(self):
        return self.get_object().author == self.request.user