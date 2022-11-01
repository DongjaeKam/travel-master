from django.shortcuts import render,redirect,get_object_or_404
from .models import Review,Comment,Search,Photo
from .forms import ReviewForm, CommentForm, PhotoForm


def index(request):
    review = Review.objects.all()
    context ={
        "review":review,
    }
    return render(request, 'articles/index.html',context)

def create(request):
    if request.method == "POST":
        review_form = ReviewForm(request.POST, request.FILES)
        photo_form = PhotoForm(request.POST, request.FILES)
        images = request.FILES.getlist('image')
        if review_form.is_valid() and photo_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            if len(images):
                for image in images:
                    image_instance = Photo(review=review, image=image)
                    review.save()
                    image_instance.save()
            else:
                review.save()
            return redirect('articles:index')
    else:
        review_form = ReviewForm()
        photo_form = PhotoForm()
    context = {
        'review_form': review_form,
        'photo_form': photo_form,
    }
    return render(request, 'articles/create.html', context)

def delete(request, pk):
    review = Review.objects.get(pk=pk)
    review.delete()
    return redirect('articles:index')

def detail(request, pk):
    review = get_object_or_404(Review, pk=pk)
    photos = review.photo_set.all()[:3]
    comments = Comment.objects.filter(review_id=pk)
    comment_form = CommentForm()
    comment_form.fields['content'].widget.attrs['placeholder'] = "댓글 작성"
    context = {
            "review": review,
            "all": review.like_users.all(),
            "count": review.like_users.count,
            "comment_form":comment_form,
            "comments":comments,
            "photos":photos,
    }
    return render(request, "articles/detail.html", context)
def update(request, pk):
    review = Review.objects.get(pk=pk)
    photos = Photo.objects.filter(review_id=review.pk)
    if request.method == 'POST':
        review_form = ReviewForm(request.POST, request.FILES, instance=review)
        photo_form = PhotoForm(request.POST, request.FILES)
        images = request.FILES.getlist('image')
        for photo in photos:
            if photo.image:
                photo.delete()
        if review_form.is_valid() and photo_form.is_valid():
            review = review_form.save(commit=False)
            if len(images):
                for image in images:
                    image_instance = Photo(review=review, image=image)
                    review.save()
                    image_instance.save()
            else:
                review.save()
            return redirect('articles:index')
    else:
        review_form = ReviewForm(instance=review)
        if photos:
            photo_form = PhotoForm(instance=photos[0])
        else:
            photo_form = PhotoForm()
    context = {
        'review_form': review_form,
        'photo_form': photo_form,
    }
    return render(request, 'articles/create.html', context)