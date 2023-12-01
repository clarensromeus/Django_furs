from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.http import require_http_methods, require_GET
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from .forms import useBlogForm
from .models import Post
from django.contrib.auth.models import User
from django.core.paginator import Paginator


# create blog view
@login_required(login_url="login")
@require_http_methods(["GET", "POST"])
def home(request):
    form = useBlogForm()
    if request.method == "POST":
        userform = useBlogForm(request.POST)
        user = User.objects.filter(id=int(request.user.id)).first()
        if userform.is_valid():
            try:
                post = userform.save(commit=False)
                post.author = user
                post.save()
            except ObjectDoesNotExist as error:
                return HttpResponse({"error ": error})
    userblog = Post.objects.all()  # pylint: disable=no-member
    # grab only 2 posts per page, just for a depictable example
    paginator = Paginator(userblog, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    # just for the fact of running over all pages with a loop in the template file
    num_pages = range(1, paginator.num_pages + 1)
    context = {"page_obj": page_obj, "form": form, "num_pages": num_pages}
    return render(request, "blog/blog.html", context)


# update blog view
@login_required(login_url="login")
@require_http_methods(["GET", "POST"])
def update_post(request, blog_id):
    if request.method == "POST":
        newTitle = request.POST.get("title")
        blog = Post.objects.filter(  # pylint: disable=no-member
            id=blog_id).first()
        # only a user with superuser role or the post creator that can update a post
        if blog and (blog.author == request.user or request.user.is_staff):
            try:
                blog.title = newTitle
                blog.save()
                return redirect("home")
            except PermissionError as error:
                return HttpResponse({"error": error})
    context = {"blog_id": blog_id}
    return render(request, "blog/update.html", context)


# delete blog view
@login_required(login_url="login")
@require_http_methods(["POST"])
def delete_post(request):
    blog_id = request.POST["blog_id"]
    blog = Post.objects.filter(id=blog_id).first()  # pylint: disable=no-member
    # only user with super_user role and the post creator that can delete a post
    if blog and (blog.author == request.user or request.user.is_staff):
        try:
            blog.delete()
            return redirect("home")
        except PermissionError as error:
            return HttpResponse({"error": error})
    return HttpResponse({"message ": "sorry you' re not allowed to delete posts"})


@login_required(login_url="login")
@require_GET
def get_one_post(request, post_id):
    post = Post.objects.filter(  # pylint: disable=no-member
        pk=int(post_id)).first()
    if post is not None:
        context = {"blog": post}
        render(request, "blog/one_blog.html", context)
    return HttpResponse({"message": "no post with that id exists"})
