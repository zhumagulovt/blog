from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.urls import reverse
from django.views import generic

from .forms import CustomUserChangeForm, CustomUserCreationForm, ProfileEditForm
from .models import Profile, UserFollowing


class CustomLoginView(LoginView):
    template_name = 'users/login.html'

    def get_success_url(self):
        if 'next' in self.request.GET:
            return self.request.GET['next']
        return reverse('users:profile-detail', kwargs={'slug': self.request.user.username})


class ProfileDetailView(generic.DetailView):
    model = Profile
    slug_field = 'user__username'

    def post(self, request, *args, **kwargs):
        self.object=self.get_object()

        if request.is_ajax():

            if 'follow' in request.POST:

                user_follow = UserFollowing.objects.filter(
                    user_id=request.user,
                    following_user_id=self.object.user)

                if user_follow.exists():
                    user_follow[0].delete()
                    return JsonResponse({'follow': False}, status=200)
                else:
                    UserFollowing.objects.create(
                        user_id=request.user,
                        following_user_id=self.object.user)
                    return JsonResponse({'follow': True}, status=200)
        
        if self.object.user != request.user:
            return redirect(reverse('users:profile-detail', kwargs={'slug': self.object.user.username}))
        
        user_form = CustomUserChangeForm(request.POST, instance=request.user)
        profile_form = ProfileEditForm(request.POST, instance=self.object)
        context = super().get_context_data(**kwargs)
        context['is_profile'] = True
        context['user_form'] = user_form
        context['profile_form'] = profile_form

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            user_form = CustomUserChangeForm(instance=request.user)
            profile_form = ProfileEditForm(instance=self.object)
            context['user_form'] = user_form
            context['profile_form'] = profile_form
            return self.render_to_response(context)

        return self.render_to_response(context)


    def get(self, request, *args, **kwargs):
        self.object=self.get_object()
        context = self.get_context_data(object=self.object)
        context['object_list'] = self.object.user.post_set.select_related('category').prefetch_related('likes')
        if UserFollowing.objects.filter(
                    user_id=request.user,
                    following_user_id=self.object.user).exists():
                    context['is_following'] = True

        if self.object.user == request.user:
            context['is_profile'] = True
            context['user_form'] = CustomUserChangeForm(initial={
                'first_name': self.object.user.first_name,
                'last_name': self.object.user.last_name,
                'email': self.object.user.email
                })
            context['profile_form'] = ProfileEditForm(instance=self.object)
        
        return self.render_to_response(context)


def registration(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            return redirect('postapp:home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/registration.html', {'form': form})


class SearchUserView(generic.ListView):
    model = User
    template_name = 'users/search_user.html'

    def get_queryset(self):
        query = self.request.GET.get('q')

        if query is not None and query != '':
            object_list = User.objects.filter(username__icontains=query)
            return object_list

# @login_required
# def edit_profile(request, profile_id):
#     profile = Profil.objects.filter(profil=request.user).get(id=profile_id)
#     user = User.objects.get(id=request.user.id)
#     if request.method == 'POST':
#         form = EditProfile(request.POST, request.FILES, instance=profile)
#         if form.is_valid():
#             new_form = form.save(commit=False)
#             new_form.profil = user
#             new_form.save()
#             return redirect('home')
#     else:
#         form = EditProfile(instance=profile)
#     return render(request, 'editprofile.html', {'form': form})