from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from communication.forms import GuestCommentField, TopicForm, UserCommentField
from communication.models import Comment, Rubric, Topic
from user.models import User


def main_forum(request):
    last_topic = Topic.objects.order_by('-created_date')[:5]
    rubrics = Rubric.objects.all()
    paginator = Paginator(rubrics, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'last_topic': last_topic,
        'page_obj': page_obj,
    }
    return render(request, 'communication/forum_main.html', context)


def detail_topic(request, pk):
    topic = Topic.objects.get(pk=pk)
    comments = Comment.objects.filter(topic=pk, is_active=True)
    initial = {'topic': topic.pk}
    if request.user.is_authenticated:
        initial['author'] = request.user.username
        form_class = UserCommentField
    else:
        form_class = GuestCommentField
    form = form_class(initial=initial)
    if request.method == 'POST':
        c_form = form_class(request.POST)
        if c_form.is_valid():
            c_form.save()
            messages.add_message(request, messages.SUCCESS, 'Comment added')
        else:
            form = c_form
            messages.add_message(request, messages.WARNING, 'Comment not added')
    context = {
        'topic': topic,
        'comments': comments,
        'form': form,
    }
    return render(request, 'communication/detail.html', context)


def rubric_detail(request, pk):
    rubric = Rubric.objects.get(pk=pk)
    topics = Topic.objects.filter(rubric=rubric)
    context = {
        'topics': topics,
        'rubric': rubric
    }
    return render(request, 'communication/rubric_detail.html', context)


def profile_topic(request, pk):
    user = User.objects.get(pk=pk)
    topics = Topic.objects.filter(author=user)
    context = {
        'topics': topics,
        'user': user
    }
    return render(request, 'communication/profile_topic.html', context)


@login_required
def add_topic(request):
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Topic added')
            return redirect('forum_main')
    else:
        form = TopicForm(initial={'author': request.user.pk})
    context = {
        'form': form
    }
    return render(request, 'communication/topic_create.html', context)


@login_required
def change_topic(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    if request.method == 'POST' and request.user.pk == topic.author.pk:
        form = TopicForm(request.POST, instance=topic)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Topic changed')
            return redirect('forum_main')
    else:
        form = TopicForm(instance=topic)
    context = {
        'form': form
    }
    return render(request, 'communication/topic_change.html', context)


@login_required
def delete_topic(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    if request.method == 'POST' and request.user.pk == topic.author.pk:
        topic.delete()
        messages.add_message(request, messages.SUCCESS, 'Topic deleted')
        return redirect('forum_main')
    else:
        context = {
            'topic': topic
        }
        return render(request, 'communication/topic_delete.html', context)
