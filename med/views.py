from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from med.forms import AddWordForm, ChengePasswordForm, RegisterUserForm, LoginUserForm, WordForm, GroupForm, EditProfileForm, AvatarUpdateForm, WordsShowForm
from django.views.generic import ListView, CreateView
from django.contrib.auth.views import LoginView
from django.views import View
from django.core.files.storage import default_storage

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.db import transaction

from django.core.paginator import Paginator

from django.contrib.auth import logout, login, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
import os
from med.models import *

def index(request):
    if request.user.is_authenticated:
        return redirect('profile')
    return render(request, 'med/index.html')

def about(request):
    return render(request, 'med/about.html')


@method_decorator(login_required, name='dispatch')
class AddWordView(LoginRequiredMixin, CreateView):
    form_class = AddWordForm
    template_name = 'med/addword.html'
    success_url = reverse_lazy('words')
    extra_context = {'title': 'Add Word'}

    def form_valid(self, form):
        word = form.save(commit=False)
        word.user = self.request.user
        word.save() 

        group_name = f"All {self.request.user.username}'s "
        group, created = WordGroup.objects.get_or_create(
            name=group_name,
            is_main=True,
            user=self.request.user
        )

        group.words.add(word)

        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class ConfirmDeleteView(View):
    def get(self, request, *args, **kwargs):
        word_ids = request.GET.getlist('word_ids')
        group_id = request.GET.get('group_id')
        
        if group_id and word_ids:
            group = get_object_or_404(WordGroup, id=group_id, user=request.user)
            words = group.words.filter(id__in=word_ids)
            return render(request, 'med/confirm_delete.html', {
                'is_group': True,
                'words': words,
                'word_ids': word_ids,
                'group_name': group.name,
                'group_id': group_id,
                'text': f'Are you sure you want to delete these words from group {group.name}?' if len(words) > 1 else f'Are you sure you want to delete this word from group {group.name}?'
            })

        elif group_id and not word_ids:
            group = get_object_or_404(WordGroup, id=group_id, user=request.user)
            return render(request, 'med/confirm_delete.html', {
                'is_group': True,
                'group_name': group.name,
                'group_id': group_id,
                'text': 'Are you sure you want to delete this group?'
            })

        elif word_ids and not group_id:
            words = Word.objects.filter(id__in=word_ids, user=request.user)
            if not words:
                return redirect('words')
            return render(request, 'med/confirm_delete.html', {
                'is_group': False,
                'words': words,
                'word_ids': word_ids,
                'text': 'Are you sure you want to delete these words?' if len(words) > 1 else 'Are you sure you want to delete this word?'
            })

        return redirect('profile') 

    def post(self, request, *args, **kwargs):
        word_ids = request.POST.getlist('word_ids')
        group_id = request.POST.get('group_id')

        if group_id and not word_ids:
            group = get_object_or_404(WordGroup, id=group_id, user=request.user)
            group.delete()
            return redirect('groups')
        
        elif word_ids and not group_id:
            Word.objects.filter(id__in=word_ids, user=request.user).delete()
            return redirect('words')

        elif group_id and word_ids:
            group = get_object_or_404(WordGroup, id=group_id, user=request.user)
            words = group.words.filter(id__in=word_ids)
            for word in words:
                group.words.remove(word)

            return redirect('group_words', group_id=group_id)

        return redirect('profile')


@method_decorator(login_required, name='dispatch')
class EditWordView(View):
    def get(self, request, word_id, *args, **kwargs):
        word = get_object_or_404(Word, id=word_id, user=request.user)
        form = WordForm(instance=word)
        return render(request, 'med/edit_word.html', {'form': form, 'word': word})

    def post(self, request, word_id, *args, **kwargs):
        word = get_object_or_404(Word, id=word_id, user=request.user)
        form = WordForm(request.POST, instance=word)
        if form.is_valid():
            form.save()
            return redirect('words')
        return render(request, 'med/edit_word.html', {'form': form, 'word': word})
    

@method_decorator(login_required, name='dispatch')
class WordListView(ListView):
    paginate_by = 25
    model = Word
    template_name = 'med/words.html'
    context_object_name = 'words'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"{self.request.user.username}'s Dictionary"
        return context

    def get_queryset(self):
        return Word.objects.filter(user=self.request.user)


class GroupListView(ListView):
    model = WordGroup
    # paginate_by = 5
    template_name = 'med/groups.html'
    context_object_name = 'groups'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Groups"
        context['title1'] = "Words"
        context['is_group'] = False
        return context

    def get_queryset(self):
        return WordGroup.objects.filter(user=self.request.user)

class GroupWordsView(ListView):
    model = Word
    template_name = 'med/groups.html'
    context_object_name = 'words'

    def is_main(self):
        group_id = self.kwargs.get('group_id')
        is_main = get_object_or_404(WordGroup, id=group_id, user=self.request.user).is_main
        return is_main

    def get_name(self): 
        group_id = self.kwargs.get('group_id')
        name = get_object_or_404(WordGroup, id=group_id, user=self.request.user).name
        return name
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Groups"
        context['title1'] = f"{self.get_name()} Words"
        context['groups'] = WordGroup.objects.filter(user=self.request.user)
        context['is_main'] = self.is_main()
        context['group_id'] = self.kwargs.get('group_id')
        context['is_group'] = True
        context['words_f_g'] = True
        return context

    def get_queryset(self):
        group_id = self.kwargs.get('group_id')
        group = get_object_or_404(WordGroup, id=group_id, user=self.request.user)
        return group.words.all()

@method_decorator(login_required, name='dispatch')
class CreateGroupView(View):
    def get(self, request, *args, **kwargs):
        form = GroupForm()

        return render(request, 'med/create_group.html', {'form': form,})

    def post(self, request, *args, **kwargs):
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.user = request.user
            group.save()
            return redirect('groups')
        return render(request, 'med/create_group.html', {'form': form})
    

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'med/register.html'
    success_url = '/login'
    extra_context = {'title': 'Register'}

    @transaction.atomic
    def form_valid(self, form):
        user = form.save()

        login(self.request, user)
        return redirect('profile', user_name=user.username)


class LoginUser(LoginView):
    form_class =  LoginUserForm
    template_name = 'med/login.html'
    extra_context = {'title': 'Log in'}

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'user_name': self.request.user.username})


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request, user_name, **kwargs):
        curent_loged_user_name = request.user.username
        profile_user = user_name

        print(curent_loged_user_name)
        print(profile_user)

        if curent_loged_user_name == profile_user:
            user_profile, created = UserProfile.objects.get_or_create(user=request.user)

            if user_profile.what_type_show == 'fav':
                recent_words = Word.objects.filter(user=request.user, is_favourite=True)[:user_profile.words_num_in_prof]
            else:
                recent_words = Word.objects.filter(user=request.user)[:user_profile.words_num_in_prof]

            word_count = Word.objects.filter(user=request.user).count()
            group_count = WordGroup.objects.filter(user=request.user).count()

            return render(request, 'med/profile.html', {
                'user': request.user,
                'recent_words': recent_words,
                'word_count': word_count,
                'group_count': group_count,
                'is_favorite': True if user_profile.what_type_show == 'fav' else False,
                'user_profile': user_profile,
                'is_my_profile': True,
                'is_profile': True
            })
        
        else:
            user = get_object_or_404(User, username=user_name)
            user_profile, created = UserProfile.objects.get_or_create(user=user)

            if user_profile.what_type_show == 'fav':
                recent_words = Word.objects.filter(user=user, is_favourite=True)[:user_profile.words_num_in_prof]
            else:
                recent_words = Word.objects.filter(user=user)[:user_profile.words_num_in_prof]

            word_count = Word.objects.filter(user=user).count()
            group_count = WordGroup.objects.filter(user=user).count()

            return render(request, 'med/profile.html', {
                'user': user,
                'logged_user': request.user,
                'recent_words': recent_words,
                'word_count': word_count,
                'group_count': group_count,
                'is_favorite': True if user_profile.what_type_show == 'fav' else False,
                'user_profile': user_profile,
                'is_my_profile': False,
                'is_profile': True
            })

class SelectGroupView(View):
    def get(self, request):
        word_ids = request.GET.getlist('word_ids')
        if not word_ids:
            return redirect('words')
        words = Word.objects.filter(id__in=word_ids)
        groups = WordGroup.objects.filter(user=request.user, is_main=False)
        return render(request, 'med/select_group.html', {
            'words': words,
            'word_ids': word_ids,
            'groups': groups,
        })

    def post(self, request, *args, **kwargs):
        word_ids = request.POST.getlist('word_ids')
        group_id = request.POST.get('group')

        if group_id:
            group = get_object_or_404(WordGroup, id=group_id, user=request.user)
        else:
            redirect('words')
        
        group_words = group.words.all()
        words = Word.objects.filter(id__in=word_ids, user=request.user)

        for word in words:
            if word not in group_words:
                group.words.add(word)

        return redirect('group_words', group_id=group_id)
    

@method_decorator(login_required, name='dispatch')
class EditProfileView(View):
    def get(self, request, *args, **kwargs):
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        profile_form = EditProfileForm(instance=request.user)
        words_show_form = WordsShowForm(instance=user_profile)
        avatar_form = AvatarUpdateForm(instance=user_profile)
        password_form = ChengePasswordForm(user=request.user)
        return render(request, 'med/edit_profile.html', {
            'profile_form': profile_form,
            'words_show_form': words_show_form,
            'avatar_form': avatar_form,
            'password_form': password_form,
        })

    def post(self, request, *args, **kwargs):
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        
        if 'update_profile' in request.POST:
            profile_form = EditProfileForm(request.POST, instance=request.user)
            if profile_form.is_valid():
                profile_form.save()
                return redirect('profile')

        if 'update_words_show' in request.POST:
            words_show_form = WordsShowForm(request.POST, instance=user_profile)
            if words_show_form.is_valid():
                words_show_form.save()
                return redirect('profile')

        if 'update_avatar' in request.POST:
            if request.POST.get('avatar') == '' and not request.POST.get('avatar-clear'):
                return redirect('edit_profile')

            old_avatar_path = None

            if user_profile.avatar:
                old_avatar_path = user_profile.avatar.path  

            avatar_form = AvatarUpdateForm(request.POST, request.FILES, instance=user_profile)
            if avatar_form.is_valid():
                avatar_form.save()
                if old_avatar_path:
                    if os.path.isfile(old_avatar_path):
                        default_storage.delete(old_avatar_path)
                return redirect('profile')
            
        if 'change_password' in request.POST:
            password_form = ChengePasswordForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, request.user)
                return redirect('profile')

        profile_form = EditProfileForm(instance=request.user)
        words_show_form = WordsShowForm(instance=user_profile)
        avatar_form = AvatarUpdateForm(instance=user_profile)
        password_form = ChengePasswordForm(user=request.user)

        return render(request, 'med/edit_profile.html', {
            'profile_form': profile_form,
            'words_show_form': words_show_form,
            'avatar_form': avatar_form,
            'password_form': password_form,
        })
        

def logout_user(request):
    logout(request)
    return redirect('login')

def make_favourite(request, word_id):
    try:
        word = get_object_or_404(Word, id=word_id, user=request.user)
        print(word)
        print(word.is_favourite)
        word.is_favourite = not word.is_favourite
        print(word.is_favourite)
        word.save()
        return redirect('words')
    except:
        return redirect('login')

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>404 Page Not Found</h1>")