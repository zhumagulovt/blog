from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Category, Post, Comment
from .forms import CommentForm, PostForm


class PostListView(generic.ListView):
    paginate_by = 3
    model = Post

    def get_queryset(self):
        # create_random()
        return Post.objects.select_related('category', 'author').prefetch_related('likes')


class PostDetailView(generic.DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['comment_form'] = CommentForm()
        data['comments'] = self.object.comment_set.all().select_related('author')
        if self.request.user.is_authenticated:
            if self.request.user in User.objects.filter(likes__id=data['object'].pk):
                data['already_liked'] = True
        return data

    def post(self, request, *args, **kwargs):

        comment_form = CommentForm(request.POST)
        self.object = self.get_object()
        data = super().get_context_data(**kwargs)

        if request.is_ajax():

            if 'like' in request.POST:
                if request.user in self.object.likes.all():
                    self.object.likes.remove(request.user)
                    return JsonResponse({"add": False}, status=200)
                else:
                    self.object.likes.add(request.user)
                    return JsonResponse({"add": True}, status=200)

            if comment_form.is_valid():
                self.object.comment_set.create(
                    author=request.user, content=comment_form.cleaned_data['content'])
                comment_form = CommentForm()
                data['comment_form'] = comment_form
                return JsonResponse({"code": "code"}, status=200)
            else:
                errors = comment_form.errors.as_json()
                return JsonResponse({"errors": errors}, status=400)


class PostCreateView(LoginRequiredMixin, generic.edit.CreateView):
    login_url = '/users/login/'
    model = Post
    form_class = PostForm
    template_name = 'postapp/post_create.html'
    extra_context = {'title': 'Новая публикация'}

    def form_valid(self, form):
        print(form.cleaned_data)
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.save()
        return HttpResponseRedirect(obj.get_absolute_url())


class PostUpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    login_url = '/users/login/'
    model = Post
    form_class = PostForm
    template_name = 'postapp/post_create.html'
    extra_context = {'title': 'Редактировать публикацию'}

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user != self.object.author:
            return redirect(self.object.get_absolute_url())
        return super().get(request, *args, **kwargs)


class PostDeleteView(LoginRequiredMixin, generic.edit.DeleteView):
    model = Post
    success_url = '/'

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class CategoryDetailView(generic.ListView):

    paginate_by = 3
    model = Post
    template_name = 'postapp/category_detail.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['title'] = Category.objects.get(pk=self.kwargs.get('pk'))
        return data

    def get_queryset(self):
        # return Post.objects.filter(category_id=self.kwargs.get('pk'))
        return Post.objects.filter(
            category_id=self.kwargs.get('pk')).select_related('category', 'author').prefetch_related('likes')


class CategoryListView(generic.ListView):

    model = Category


class SearchResultView(generic.ListView):

    model = Post
    template_name = 'postapp/search_result.html'

    def get_queryset(self):
        query = self.request.GET.get('q')

        if query is not None and query != '':

            object_list = Post.objects.filter(title__icontains=query).select_related('category', 'author').prefetch_related('likes')

            return object_list



