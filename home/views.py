from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Question, Answer, AnswerLike
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from django.http import HttpResponseForbidden

@login_required
def home(request):
    context = {}
    if request.method == 'POST':
        post_type = request.POST.get("post_type")
        if post_type == "add_query":
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                return redirect('/')
    else:
        form = PostForm()
    context['post_form'] = form

    posts = Post.objects.all().order_by('-created')
    posts_with_comments = []
    for post in posts:
        comments = Question.objects.filter(post=post).order_by('created')
        posts_with_comments.append({
            'post': post,
            'comments': comments
        })
    context["posts_with_comments"] = posts_with_comments
    return render(request, "index.html", context)

def add_question(request):
    context = {}
    if request.method == "POST":
        comment_data = request.POST.get("comment_data")
        post_id = request.POST.get("post_id")
        post = get_object_or_404(Post, id=post_id)

        Question.objects.create(
            body=comment_data,
            post=post,
            user=request.user
        )
        return redirect('/')

    return render(request, "add_question.html", context)

@login_required
def answer_question(request):
    context = {}

    question_id = request.GET.get("comment_id")
    question_data = get_object_or_404(Question, id=question_id)
    post_data = question_data.post

    if request.method == "POST":
        if 'like_answer' in request.POST:
            answer_id = request.POST.get('answer_id')
            answer = get_object_or_404(Answer, id=answer_id)

            if post_data.author == request.user:
                existing_like = AnswerLike.objects.filter(user=request.user, answer=answer).first()
                if existing_like:
                    existing_like.delete()
                else:
                    AnswerLike.objects.create(user=request.user, answer=answer)

            return redirect(f'/answer_question?post_id={post_data.id}&comment_id={question_data.id}')

        elif 'answer_data' in request.POST:
            Answer.objects.create(
                question=question_data,
                user=request.user,
                body=request.POST.get("answer_data")
            )
            return redirect(f'/answer_question?post_id={post_data.id}&comment_id={question_data.id}')

    answers = Answer.objects.filter(question=question_data)
    answers_with_author_like = []
    for answer in answers:
        liked_by_author = AnswerLike.objects.filter(answer=answer, user=post_data.author).exists()

        answers_with_author_like.append({
            'answer': answer,
            'liked_by_author': liked_by_author,
        })

    context['answers_with_author_like'] = answers_with_author_like
    context['question_data'] = question_data
    context['post_data'] = post_data

    return render(request, "answer_question.html", context)

@login_required
def like_answer(request):
    if request.method == "POST":
        answer = get_object_or_404(Answer, id=request.POST.get('answer_id'))
        post = answer.question.post

        if post.author != request.user:
            return HttpResponseForbidden("You are not allowed to like this answer.")

        existing_like = AnswerLike.objects.filter(answer=answer, user=request.user).first()
        if existing_like:
            existing_like.delete()
        else:
            AnswerLike.objects.create(answer=answer, user=request.user)

        return redirect(f'/answer_question?post_id={post.id}&comment_id={answer.question.id}')
