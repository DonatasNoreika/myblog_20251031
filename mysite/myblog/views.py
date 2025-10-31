from django.shortcuts import render
from django.views import generic
from .models import Post
from django.db.models import Q

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
