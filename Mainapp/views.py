# mainapp/views.py

from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.forms import UserCreationForm
from .models import Post
from .forms import CreatePostForm
from .forms import ReplyPostForm
from .forms import AccountSettingsForm
from .forms import CustomUserCreationForm 


# Example: Import necessary models, forms, or any other dependencies

class HomePageView(View):
    def get(self, request):
        # Retrieve all posts from the database and order them by created_at in descending order
        posts = Post.objects.order_by('-created_at')

        # Get the username if the user is authenticated
        username = request.user.username if request.user.is_authenticated else None

        # Render the 'index.html' template with the ordered posts and username
        return render(request, 'index.html', {'posts': posts, 'form': CreatePostForm(), 'username': username})

    def post(self, request):
        form = CreatePostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('Mainapp:index')

        posts = Post.objects.all()
        return render(request, 'index.html', {'posts': posts, 'form': form, 'username': request.user.username})

class LoginView(BaseLoginView):
    template_name = 'registration/login.html'

    def get(self, request, *args, **kwargs):
        # Logic for displaying the login form
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        # Logic for processing login form submission
        response = super().post(request, *args, **kwargs)

        if self.request.user.is_authenticated:
            # Redirect to the home page or any other page after successful login
            return redirect('Mainapp:index')  # Replace 'index' with the name of your home view

        # If authentication fails or other conditions, you can handle it here

        return response
    
class LogoutView(View):
    def get(self, request):
        # Use Django's built-in logout function
        logout(request)
        # Redirect to the homepage or any other desired page after logout
        return redirect('Mainapp:index')    

class SignupView(View):
    template_name = 'registration/signup.html'

    def get(self, request, *args, **kwargs):
        form = CustomUserCreationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Signup successful! You are now logged in.')
            return redirect('Mainapp:index')

        return render(request, self.template_name, {'form': form})


class PasswordResetView(View):
    template_name = 'registration/password_reset.html'

    def get(self, request, *args, **kwargs):
        form = PasswordResetForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(request=request)
            messages.success(request, 'Password reset email sent. Check your inbox.')
            return redirect('login')

        return render(request, self.template_name, {'form': form})

# mainapp/views.py

from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from .forms import CreatePostForm
from .models import Post

class CreatePostView(View):
    template_name = 'posts/create_post.html'

    def get(self, request):
        if not request.user.is_authenticated:
            # If the user is not authenticated, redirect to the signup page
            return redirect('Mainapp:signup')

        # Logic for displaying the create post form
        form = CreatePostForm()  # Use your CreatePostForm here
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        if not request.user.is_authenticated:
            # If the user is not authenticated, redirect to the signup page
            return redirect('Mainapp:signup')

        # Logic for processing create post form submission
        form = CreatePostForm(request.POST)  # Use your CreatePostForm here
        if form.is_valid():
            # If the form is valid, save the post and do any additional processing
            # For example, you can associate the post with the logged-in user
            post = form.save(commit=False)
            post.author = request.user  # Assuming you have a ForeignKey to User in your Post model
            post.save()

            # Redirect to the post detail page or another relevant page
            return redirect('Mainapp:view_post', pk=post.id)


        # If the form is not valid, re-render the form with errors
        return render(request, self.template_name, {'form': form})


class ViewPostView(View):
    template_name = 'posts/view_post.html'

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        return render(request, self.template_name, {'post': post})
    
class ViewMyPostsView(View):
    template_name = 'posts/view_my_posts.html'

    def get(self, request):
        # Retrieve posts belonging to the current user
        user_posts = Post.objects.filter(author=request.user)
        return render(request, self.template_name, {'user_posts': user_posts})    

class ReplyPostView(View):
    template_name = 'posts/reply_post.html'

    def get(self, request, pk):
        # Logic for displaying the reply post form
        post = get_object_or_404(Post, pk=pk)
        form = ReplyPostForm()  # Use your ReplyPostForm here
        return render(request, self.template_name, {'post': post, 'form': form})

    def post(self, request, pk):
        # Logic for processing reply post form submission
        post = get_object_or_404(Post, pk=pk)
        form = ReplyPostForm(request.POST)  # Use your ReplyPostForm here
        if form.is_valid():
            # If the form is valid, save the reply and associate it with the post
            reply = form.save(commit=False)
            reply.post = post
            reply.save()
            
            # Redirect to the post detail page or another relevant page
            return redirect('Mainapp:view_post', pk=post.id)  # Adjust the URL name as needed

        # If the form is not valid, re-render the form with errors
        return render(request, self.template_name, {'post': post, 'form': form})
    
    
    
class DeletePostView(LoginRequiredMixin, View):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk, author=request.user)
        return render(request, 'posts/delete_post.html', {'post': post})

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk, author=request.user)
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('Mainapp:index')    

class AccountSettingsView(View):
    template_name = 'settings/account_settings.html'

    def get(self, request):
        # Logic for displaying the account settings form
        form = AccountSettingsForm(instance=request.user)  # Use your AccountSettingsForm here
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        # Logic for processing account settings form submission
        form = AccountSettingsForm(request.POST, instance=request.user)  # Use your AccountSettingsForm here
        if form.is_valid():
            # If the form is valid, save the account settings
            form.save()

            # Redirect to the account settings page or another relevant page
            return redirect('account_settings')  # Adjust the URL name as needed

        # If the form is not valid, re-render the form with errors
        return render(request, self.template_name, {'form': form})