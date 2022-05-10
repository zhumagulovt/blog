from turtle import title
from unicodedata import category
from django.http import JsonResponse
from django.views import generic
from django.contrib.auth.models import User

from .models import Category, Post, Comment
from .forms import CommentForm

from random import shuffle
from string import ascii_letters

class PostListView(generic.ListView):
    model = Post

    def get_queryset(self):
        # create_random()
        return Post.objects.filter().select_related('category', 'author')


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
                else:
                    self.object.likes.add(request.user)
                return JsonResponse({}, status=200)

            if comment_form.is_valid():
                self.object.comment_set.create(
                    author=request.user, content=comment_form.cleaned_data['content'])
                comment_form = CommentForm()
                data['comment_form'] = comment_form
                return JsonResponse({"code": "code"}, status=200)
            else:
                errors = comment_form.errors.as_json()
                return JsonResponse({"errors": errors}, status=400)


class CategoryDetailView(generic.ListView):

    model = Post
    template_name = 'postapp/category_detail.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['title'] = Category.objects.get(pk=self.kwargs.get('pk'))
        return data

    def get_queryset(self):
        return Post.objects.filter(category_id=self.kwargs.get('pk'))
        # return Post.objects.filter(category_id=self.kwargs.get('pk')).select_related('category')

class CategoryListView(generic.ListView):

    model = Category


class SearchResultView(generic.ListView):

    model = Post
    template_name = 'postapp/search_result.html'
    
    def get_queryset(self):
        query = self.request.GET.get('q')

        if query is not None and query != '':

            object_list = Post.objects.filter(title__icontains=query)

            return object_list


def create_random():

    author = User.objects.get(pk=2)

    cat = Category.objects.get(pk=1)
    t = list(ascii_letters)
    c = list(ascii_letters*10)
    for i in range(200):
        shuffle(t)
        shuffle(c)
        t_ = ''.join(t)
        c_ = ''.join(c)
        Post.objects.create(title=t_, content=c_, author=author, category=cat)

# class PostCreateView(LoginRequiredMixin, generic.CreateView):
#     login_url = '/users/login/'
#     # redirect_field_name = reverse('post-detail', kwargs={'pk': 1})
#     form_class = PostForm
#     template_name = 'postapp/post_create_form.html'

#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)
