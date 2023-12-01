from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.views.generic import CreateView, DeleteView, UpdateView, ListView
from blog.models import Post
from django.views import View
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator
from blog.forms import useBlogForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import PasswordChangeView, LoginView, LogoutView
from .form import LoginForm, PasswordChangeForm
from user.form import UserForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.


class home(LoginRequiredMixin, View):
    queryset = Post.objects.all()  # pylint: disable=no-member
    template_name = "blog/blog.html"
    login_url = "blog:login"

    def get(self, request):
        form = useBlogForm()
        userblog = self.queryset
        # grab only 2 posts per page, just for a depictable example
        paginator = Paginator(userblog, 2)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        # just for the fact of running over all pages with a loop in the template file
        num_pages = range(1, paginator.num_pages + 1)
        context = {"page_obj": page_obj, "form": form, "num_pages": num_pages}
        return render(request, "blog/blog.html", context)

    def post(self, request):
        userform = useBlogForm(request.POST)
        user = User.objects.filter(id=int(request.user.id)).first()
        if userform.is_valid():
            post = userform.save(commit=False)
            post.author = user
            post.save()
            return redirect(reverse("blog:home"))


class update_post(PermissionRequiredMixin, UpdateView):
    model = Post
    form_class = useBlogForm
    login_url = "blog:login"
    success_url = reverse_lazy("blog:home")
    template_name = "blog/cls_update.html"
    permission_denied_message = "sorry you're not authorized"
    permission_required = ["blog.view_post", "blog.change_post"]


class delete_post(PermissionRequiredMixin, DeleteView):
    model = Post
    form_class = useBlogForm
    success_url = reverse_lazy("blog:home")
    permission_denied_message = "sorry you're not authorized"
    permission_required = ["blog.view_post", "blog.delete_post"]


class get_one_post(LoginRequiredMixin, DetailView):
    model = Post
    form_class = useBlogForm
    pk_url_kwarg = "title"
    context_object_name = "blog"
    login_url = "blog:login"
    template_name = "blog/cls_one_blog.html"
    permission_denied_message = "sorry, you are not authorized"

    def get_object(self):
        queryset = super().get_queryset()
        title = self.kwargs["title"]
        model_obj = get_object_or_404(queryset, title=title)
        return model_obj


class all_post(LoginRequiredMixin, ListView):
    queryset = Post.objects.all()  # pylint: disable=no-member
    form_class = useBlogForm
    login_url = "blog:login"
    template_name = "cls/cls_blog.html"
    paginate_by = 2  # a small quantity of elements per page just for a simple demonstration
    # instead of the defaut object_list context name i customize the name to my suit
    context_object_name = "page_obj"
    permission_denied_message = "you're not allowed"


class create_post(LoginRequiredMixin, CreateView):
    model = Post
    form_class = useBlogForm
    login_url = "blog:login"
    template_name = "cls/cls_createblog.html"
    success_url = reverse_lazy("blog:home")
    permission_denied_message = "sorry you're not authorized"

    def form_valid(self, form):
        user = User.objects.filter(pk=int(self.request.user.id))
        form.author = user
        return super().form_valid(form)


class login(LoginView):
    template_name = "cls/cls_login.html"
    form_class = LoginForm
    redirect_field_name = reverse_lazy("blog:home")
    redirect_authenticated_user = True


class register(UserPassesTestMixin, CreateView):
    template_name = "cls/cls_register.html"
    success_url = reverse_lazy("blog:home")
    form_class = UserForm
    login_url = "blog:register"
    redirect_field_name = reverse_lazy("blog:home")
    raise_exception = True

    def test_func(self) -> bool | None:
        return self.request.user is not None


class all_users(ListView):
    queryset = User.objects.all()
    template_name = "cls/users.html"
    context_object_name = "users"

    def get_context_data(self, **kwargs):
        queryset = self.get_queryset()
        # grab only administrators from the user model
        administrators = get_list_or_404(queryset, is_staff=True)
        context = super().get_context_data(**kwargs)
        context["administrators"] = administrators
        return context


class change_password(LoginRequiredMixin, PasswordChangeView):
    template_name = "blog/change_password",
    success_url = reverse_lazy("blog:login")
    form_class = PasswordChangeForm
    permission_denied_message = "sorry you're not allowed"


class Logout(LogoutView):
    redirect_field_name = reverse_lazy("blog:login")
