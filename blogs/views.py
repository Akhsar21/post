from profiles.models import Profile
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from django.db.models import Count, Q
from django.contrib import messages
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
# import json
from django.http import HttpResponse, JsonResponse
# from django.template.loader import render_to_string

from contacts.forms import EmailSignupForm
# from contacts.models import Signup
from .forms import PostModelForm, CommentModelForm
from .models import Post, Author, PostView, Category, Tag

form = EmailSignupForm()


def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None


class SearchView(generic.View):
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


class PostListView(generic.ListView):
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


class PostDetailView(generic.DetailView):
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
        post = self.get_object()
        category_count = get_category_count()
        most_recent = Post.objects.order_by('-published')[:3]
        context = super().get_context_data(**kwargs)
        context['category_count'] = category_count
        context['most_recent'] = most_recent
        context['admin_object'] = post
        context['page_request_var'] = "page"
        return context


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    form_class = PostForm
    raise_exception = True

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


class PostUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Post
    form_class = PostModelForm
    raise_exception = True

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


class PostDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Post
    success_url = '/blog'
    raise_exception = True

    # def get_object(self, *args, **kwargs):
    #     pk = self.kwargs.get('pk')
    #     obj = Post.objects.get(pk=pk)
    #     if not obj.author.user == self.request.user:
    #         messages.warning(self.request, _("You need to be the author of the post in order to delete it"))
    #         return obj


class CategoryView(generic.ListView):
    model = Category


class PostCategoryView(generic.ListView):
    model = Post
    template_name = 'posts/post_category.html'

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Post.objects.filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class TagView(generic.ListView):
    model = Tag


class PostTagView(generic.ListView):
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


class PostLikeToggle(generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        slug = self.kwargs.get("slug")
        print(slug)
        obj = get_object_or_404(Post, slug=slug)
        url_ = obj.get_absolute_url()
        user = self.request.user
        if user.is_authenticated():
            if user in obj.likes.all():
                obj.likes.remove(user)
            else:
                obj.likes.add(user)
        return url_


@login_required
def like_unlike_post(request):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)
        profile = Profile.objects.get(user=user)

        if profile in post_obj.liked.all():
            post_obj.liked.remove(profile)
        else:
            post_obj.liked.add(profile)

        like, created = Like.objects.get_or_create(user=profile, post_id=post_id)

        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
        else:
            like.value = 'Like'

            post_obj.save()
            like.save()

        data = {
            'value': like.value,
            'likes': post_obj.liked.all().count()
        }

        return JsonResponse(data, safe=False)
    return redirect('post-detail')


@login_required
def post_comment_create_and_list_view(request):
    qs = Post.objects.all()
    profile = Profile.objects.get(user=request.user)

    # initials
    p_form = PostModelForm()
    c_form = CommentModelForm()
    post_added = False

    if 'submit_p_form' in request.POST:
        print(request.POST)
        p_form = PostModelForm(request.POST, request.FILES)
        if p_form.is_valid():
            instance = p_form.save(commit=False)
            instance.author = profile
            instance.save()
            p_form = PostModelForm()
            post_added = True

    if 'submit_c_form' in request.POST:
        print(request.POST)
        c_form = CommentModelForm(request.POST)
        if c_form.is_valid():
            instance = c_form.save(commit=False)
            instance.user = profile
            instance.post = Post.objects.get(id=request.POST.get('post_id'))
            instance.save()
            c_form = PostModelForm()

    context = {
        'qs' = qs,
        'profile' = profile,
        'p_form' = p_form,
        'c_form' = c_form,
        'post_added' = post_added,
    }

    return render(request, 'posts/main.html', context)
