from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm


# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by(
        "published_date"
    )
    return render(request, "blog/post_list.html", {"posts": posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, "blog/post_detail.html", {"post": post})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            # commit=False means that we don’t want to save the Post model yet – we want to add the author first.
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            # Finally we call post.save() to save the post model with the author.
            post.save()
            return redirect("post_detail", pk=post.pk)
    else:
        form = PostForm()
        return render(request, "blog/post_edit.html", {"form": form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        # We also added an instance argument to the form. This tells Django that we want to edit an existing post.
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            # We added the line post.published_date = timezone.now().
            # This is the missing line we talked about previously! We want to set the published_date field of the blog post before saving the model.
            post.published_date = timezone.now()
            post.save()
            return redirect("post_detail", pk=post.pk)
    else:
        # We added the instance argument to both lines. Now when we get a form with a POST request, we will create a form using the existing post object.
        form = PostForm(instance=post)
        return render(request, "blog/post_edit.html", {"form": form})
