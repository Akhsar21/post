from django.utils.translation import gettext as _
from django.db.models import Count, Q
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
import json
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string

from contacts.forms import EmailSignupForm
from contacts.models import Signup
from .forms import PostForm
from .models import Post, Author, PostView, Category, Tag

form = EmailSignupForm()


def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None


class SearchView(View):
    def get(self, request, *args, **kwargs):
        queryset = Post.objects.all()
        query = request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(overview__icontains=query)
            ).distinct()
        context = {
            'queryset': queryset,
            'title': _("This is the results for your search")
        }
        return render(request, 'search_results.html', context)


def get_category_count():
    queryset = Post \
        .objects \
        .values('category__name') \
        .annotate(Count('category__name'))
    return queryset


class PostListView(ListView):
    form = EmailSignupForm()
    model = Post
    context_object_name = 'queryset'
    paginate_by = 8

    def get_context_data(self, **kwargs):
        category_count = get_category_count()
        most_recent = Post.objects.order_by('-published')[:3]
        results = Post.objects.all()
        jsondata = serializers.serialize('json', results)
        context = super().get_context_data(**kwargs)
        context['most_recent'] = most_recent
        context['jsondata'] = jsondata
        context['page_request_var'] = "page"
        context['title'] = _("Read Our Blog")
        context['category_count'] = category_count
        context['form'] = self.form
        return context


class PostDetailView(DetailView):
    model = Post
    # form = CommentForm()

    def get_object(self):
        obj = super().get_object()
        if self.request.user.is_authenticated:
            PostView.objects.get_or_create(
                user=self.request.user,
                post=obj
            )
        return obj

    def get_context_data(self, **kwargs):
        category_count = get_category_count()
        most_recent = Post.objects.order_by('-published')[:3]
        context = super().get_context_data(**kwargs)
        context['category_count'] = category_count
        context['most_recent'] = most_recent
        context['page_request_var'] = "page"
        return context

    # def post(self, request, *args, **kwargs):
    #     user = request.user
    #     post_id = request.POST.get('id')

    #     post = get_object_or_404(Post, id=post_id)
    #     is_liked = False
    #     if post.likes.filter(id=user.id).exists():
    #         post.likes.remove(user)
    #         is_liked = False
    #     else:
    #         post.likes.add(user)
    #         is_liked = True

    #     context = {
    #         'post': post,
    #         'is_liked': is_liked,
    #         'total_likes': post.total_likes(),
    #     }
    #     if request.is_ajax():
    #         html = render_to_string('blogs/like_section.html', context, request=request)
    #         return JsonResponse({'form': html})


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _("Create")
        return context

    def form_valid(self, form):
        form.instance.author = get_author(self.request.user)
        form.save()
        messages.success(self.request, _("Post created successfully!"))
        return redirect(reverse("post-detail", kwargs={
            'slug': form.instance.slug
        }))


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _("Update")
        return context

    def form_valid(self, form):
        form.instance.author = get_author(self.request.user)
        form.save()
        messages.success(self.request, _("Post updated successfully!"))
        return redirect(reverse("post-detail", kwargs={
            'slug': form.instance.slug
        }))


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = '/blog'
    # template_name = 'blogs/post_confirm_delete.html'


class CategoryView(ListView):
    model = Category


class PostCategoryView(ListView):
    model = Post
    template_name = 'posts/post_category.html'

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Post.objects.filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class TagView(ListView):
    model = Tag


class PostTagView(ListView):
    model = Post
    template_name = 'posts/post_tag.html'

    def get_queryset(self):
        self.tags = get_object_or_404(Tag, slug=self.kwargs['slug'])
        return Post.objects.filter(tags=self.tags)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = self.tags
        return context


def getdata(request):
    results = Post.objects.all()
    jsondata = serializers.serialize('json', results)
    return HttpResponse(jsondata)
