from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .models import Post
from .forms import PostForm, CommentForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required

class PostListView(generic.ListView):
    model = Post
    template_name = 'blog/post_list.html'
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Post.objects.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            )
        else:
            return Post.objects.all()

class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.id)
        else:
            print(form.errors)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form': form, 'post': post})


from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('post_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})