# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib import messages

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.views.decorators.http import require_POST
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Post, Comment
from .forms import PostForm, CommentForm

# --------------- View for posts likes --------------- #
@login_required
@require_POST
def post_like(request):
    post_id = request.POST.get('id')
    action = request.POST.get('action')

    if post_id and action:
        try:
            post = Post.objects.get(id=post_id)
            if action == 'like':
                post.users_like.add(request.user)
            else:
                post.users_like.remove(request.user)
            return JsonResponse({'status':'ok'})
        except:
            pass
    return JsonResponse({'status':'ko'})

#--------------------------------------------------------------------#
##------------------------- FUNCTION-BASED VIEWS ---------------------##
#--------------------------------------------------------------------#

# --------------- List All Posts --------------- #
def index(request):
    queryset_list = Post.objects.all() #.order_by("-created")
    paginator = Paginator(queryset_list, 2)  # Show 3 posts per page

    queryset = request.GET.get('page')
    try:
        queryset = paginator.page(queryset)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            # If the request is AJAX and the page is out of range
            #  return an empty page
            return HttpResponse('')
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    if request.is_ajax():
        return render(request,
                      'posts/list_ajax.html',
                      {'object_list': queryset, 'user': request.user})

    context = {
        'object_list': queryset,
        'user': request.user
    }
    return render(request, 'posts/index.html', context)

# --------------- Get Post By Id --------------- #
def getPostById(request, id=None):
    instance = get_object_or_404(Post, id=id)
    context = {
        'instance': instance
    }
    return render(request, 'posts/post_detail.html', context)

# --------------- Get Post By Slug --------------- #
def getPostBySlug(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)

    # List of active comments for this post
    comments = instance.comments.filter(active=True)

    if request.method == 'POST':
        #  A comment was posted
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            # Create comment object but dont save it to database
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment and to the user
            new_comment.post = instance
            new_comment.user = request.user
            new_comment.save()
        else:
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()
    context = {
        'instance': instance,
        'comments': comments,
        'comment_form': comment_form
    }
    return render(request, 'posts/post_detail.html', context)

# --------------- Create New Post --------------- #
@login_required()
def newPost(request):
    if request.user.is_authenticated():
        form = PostForm(request.POST or None, request.FILES or None)
        if request.method == "POST":
            if form.is_valid():
                # Create, but don't save the new post instance.
                instance = form.save(commit=False)
                instance.user = request.user
                # Save the new instance.
                instance.save()
                # Flash message
                messages.success(request, "Post successfully created.")
                # Redirect
                return HttpResponseRedirect(instance.get_absolute_url())
            else:
                messages.error(request, "Error creating post.")
        context = {
            "form": form
        }
        return render(request, 'posts/post_create.html', context)
    else:
        return HttpResponseRedirect(reverse('login'))

# --------------- Edit Post --------------- #
@login_required()
def editPost(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)

    if request.method == "POST":
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.success(request, "Post successfully saved.")
            return HttpResponseRedirect(instance.get_absolute_url())
        else:
            messages.error(request, "Error saving the post.")

    context = {
        "instance": instance,
        "form": form
    }
    return render(request, 'posts/post_create.html', context)

# --------------- Delete Post --------------- #
@login_required()
def deletePost(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    image = instance.image
    if image:
        image.delete(save=False)
    instance.delete()
    messages.success(request, "Post successfully deleted.")
    return HttpResponseRedirect(reverse('posts:index'))


#--------------------------------------------------------------------#
##------------------------- CLASS-BASED VIEWS ---------------------##
#--------------------------------------------------------------------#

# --------------- List All Posts --------------- #
class PostListView(ListView):
    model = Post
    template_name = 'posts/index.html'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        queryset = Post.objects.all()
        paginator = Paginator(queryset, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            query_set = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            query_set = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            query_set = paginator.page(paginator.num_pages)

        context['object_list'] = query_set
        return context


# --------------- Get Post By Slug --------------- #
class PostDetailView(DetailView):
    context_object_name = 'instance'
    queryset = Post.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super(PostDetailView, self).get_context_data(*args, **kwargs)
        return context

# --------------- Create New Post --------------- #
class PostCreateView(LoginRequiredMixin, CreateView):
    form_class = PostForm
    template_name = 'posts/post_create.html'
    success_url = reverse_lazy('posts:index')

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        #instance.save() # por defecto el form_valid ya hace el save asi q no hace falta
        return super(PostCreateView, self).form_valid(form)

# --------------- Edit Post --------------- #
class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'posts/post_create.html'
    fields = ['title', 'content', 'image']
    success_url = reverse_lazy('posts:index')

# --------------- Delete Post --------------- #
class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('posts:index')

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(PostDeleteView, self).get_object()
        if not obj.user == self.request.user:
            raise Http404
        return obj

    def post(self, request, *args, **kwargs):
        if self.request.POST.get("confirm_delete"):
            # when confirmation page has been displayed and confirm button pressed
            image = self.get_object().image
            if image:
                image.delete(save=False)
            self.get_object().delete()
            return HttpResponseRedirect(self.success_url)
        elif self.request.POST.get("cancel"):
            # when confirmation page has been displayed and cancel button pressed
            return HttpResponseRedirect(reverse('profiles:user_profile', kwargs={'username':self.request.user}))
        else:
            # when data is coming from the form which lists all items
            return self.get(self, *args, **kwargs)