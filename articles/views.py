from django.shortcuts import render, redirect, get_object_or_404
from .models import Review, Comment, Search, Photo
from .forms import ReviewForm, CommentForm, PhotoForm
from django.db.models import Q
from django.core.paginator import Paginator


def index(request):
    review = Review.objects.all()
    context = {
        "review": review,
    }
    return render(request, "articles/index.html", context)


def create(request):
    if request.method == "POST":
        review_form = ReviewForm(request.POST, request.FILES)
        photo_form = PhotoForm(request.POST, request.FILES)
        images = request.FILES.getlist("image")
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
            return redirect("articles:index")
    else:
        review_form = ReviewForm()
        photo_form = PhotoForm()
    context = {
        "review_form": review_form,
        "photo_form": photo_form,
    }
    return render(request, "articles/create.html", context)


def delete(request, pk):
    review = Review.objects.get(pk=pk)
    review.delete()
    return redirect("articles:index")


def detail(request, pk):
    review = get_object_or_404(Review, pk=pk)
    photos = review.photo_set.all()[:3]
    comments = Comment.objects.filter(review_id=pk)
    comment_form = CommentForm()
    comment_form.fields["content"].widget.attrs["placeholder"] = "댓글 작성"
    context = {
        "review": review,
        "all": review.like_users.all(),
        "count": review.like_users.count,
        "comment_form": comment_form,
        "comments": comments,
        "photos": photos,
    }
    return render(request, "articles/detail.html", context)


def update(request, pk):
    review = Review.objects.get(pk=pk)
    photos = Photo.objects.filter(review_id=review.pk)
    if request.method == "POST":
        review_form = ReviewForm(request.POST, request.FILES, instance=review)
        photo_form = PhotoForm(request.POST, request.FILES)
        images = request.FILES.getlist("image")
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
            return redirect("articles:index")
    else:
        review_form = ReviewForm(instance=review)
        if photos:
            photo_form = PhotoForm(instance=photos[0])
        else:
            photo_form = PhotoForm()
    context = {
        "review_form": review_form,
        "photo_form": photo_form,
    }
    return render(request, "articles/create.html", context)

def search(request):
    popular_list = {}
    print("확인1")
    if request.method == "GET":
        search = request.GET.get("searched", "")
        print("확인2")

        if not search.isdigit():
            if Review.objects.filter(
                Q(title__icontains=search) | Q(content__icontains=search)
            ):
                popular_list[search] = popular_list.get(search, 0) + 1
        print("확인3")

        for k, v in sorted(popular_list.items(), key=lambda x: -x[1]):
            if Search.objects.filter(title=k):
                s = Search.objects.get(title=k)
                s.count += 1
                s.save()
            else:
                s = Search(title=k, count=v)
                s.save()
        popular = Search.objects.order_by("-count")[:10]

        search_list = Review.objects.filter(
            Q(title__icontains=search)
            | Q(content__icontains=search)
            | Q(place__icontains=search)
            | Q(theme__icontains=search)
        )

        if search:
            print("확인4")

            if search_list:
                print("확인5")

                page = int(request.GET.get("p", 1))
                pagenator = Paginator(search_list, 4)
                boards = pagenator.get_page(page)
                return render(
                    request,
                    "articles/search.html",
                    {
                        "search": search,
                        "boards": boards,
                        "search_list": search_list,
                        "popular": popular,
                    },
                )
            else:
                k = "검색 결과가 없습니다 다시 검색해주세요"
                context = {"v": k}
                return render(request, "articles/searchfail.html", context)
        else:
            k = "검색 결과가 없습니다 다시 검색해주세요"
            context = {"v": k}
            return render(request, "articles/searchfail.html", context)


def searchfail(request):
    return render(request, "articles/searchfail.html")
