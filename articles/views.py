import json
from django.shortcuts import render, redirect, get_object_or_404
from .models import Review, Comment, Search, Photo
from .forms import ReviewForm, CommentForm, PhotoForm
from accounts.models import User
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import datetime
from django.contrib.auth import get_user_model


def index(request):
    popular_search = Search.objects.order_by("-count")[:10]
    review = Review.objects.all()
    context = {
        "review": review,
        "popular_search": popular_search,
    }
    return render(request, "articles/index.html", context)


@login_required(login_url="accounts:login")
def create(request):
    user = User.objects.get(pk=request.user.pk)
    user.rank += 2
    user.save()
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


@login_required
def delete(request, pk):
    review = Review.objects.get(pk=pk)
    review.delete()
    return redirect("articles:index")


def detail(request, pk):
    review = get_object_or_404(Review, pk=pk)
    photos = review.photo_set.all()
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


@login_required
def update(request, pk):
    review = Review.objects.get(pk=pk)
    photos = Photo.objects.filter(review_id=review.pk)

    if review.user == request.user:
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
    else:
        return redirect("accounts:wrong_approach")


def search(request):
    popular_list = {}
    if request.method == "GET":
        search = request.GET.get("searched", "")

        if not search.isdigit():
            if Review.objects.filter(
                Q(title__icontains=search)
                | Q(content__icontains=search)
                | Q(place__icontains=search)
            ):
                popular_list[search] = popular_list.get(search, 0) + 1

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
            | Q(user_id__profile_name__icontains=search)
        )

        if search:
            if search_list:

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


# 댓글생성
@login_required(login_url="accounts:login")
def comment_create(request, pk):
    review = Review.objects.get(pk=pk)
    users = User.objects.get(pk=request.user.pk)
    users.rank += 1
    users.save()

    comment_form = CommentForm(request.POST)
    user = request.user.pk
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.review = review
        comment.user = request.user
        comment.save()
    # 제이슨은 객체 형태로 받질 않음 그래서 리스트 형태로 전환을 위해 리스트 생성
    temp = Comment.objects.filter(review_id=pk).order_by("-pk")
    comment_data = []
    for t in temp:
        t.created_at = t.created_at.strftime("%Y-%m-%d %H:%M")
        comment_data.append(
            {
                "id": t.user_id,
                "userName": t.user.username,
                "content": t.content,
                "commentPk": t.pk,
                "created_at": t.created_at,
                "profile_name": t.user.profile_name,
                "profile_image": t.user.profile_image.url,
            }
        )
    context = {
        "comment_data": comment_data,
        "review_pk": pk,
        "user": user,
    }
    return JsonResponse(context)
    # if request.method == "POST":
    #     comment_form = CommentForm(request.POST)
    #     if comment_form.is_valid():
    #         comment = comment_form.save(commit=False)
    #         comment.user = request.user
    #         comment.review = review
    #         comment.save()
    #     return redirect("articles:review_detail", pk)
    # else:
    #     return redirect("articles:review_detail", pk)
# 댓글삭제
@login_required(login_url="accounts:login")
def comment_delete(request, review_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    review_pk = Review.objects.get(pk=review_pk).pk
    user = request.user.pk
    comment.delete()
    temp = Comment.objects.filter(review_id=review_pk).order_by('-pk')
    comment_data = []
    for t in temp:
        t.created_at = t.created_at.strftime("%Y-%m-%d %H:%M")
        comment_data.append(
            {
                "id": t.user_id,
                "userName": t.user.username,
                "content": t.content,
                "commentPk": t.pk,
                "created_at": t.created_at,
                "profile_name": t.user.profile_name,
                "profile_image": t.user.profile_image.url,
            }
        )
    context = {
        'comment_data': comment_data,
        'review_pk': review_pk,
        'user': user,
    }
    return JsonResponse(context)


# 지도 테스트 용
def map(request):
    return render(request,"articles/map.html")
    # restaurant = get_object_or_404(Restaurant, pk=pk)
    # client_id = '7apalzu8wx';    # 본인이 할당받은 ID 입력
    # client_pw = 'LpKKb9dnZwQUKjkeDuXDZ6n3NgeD1uN50pvk9MYj';    # 본인이 할당받은 Secret 입력

    # endpoint = "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode"
    # url = f"{endpoint}?query={restaurant.address}"

    # headers = {
    # "X-NCP-APIGW-API-KEY-ID": '7apalzu8wx',
    # "X-NCP-APIGW-API-KEY": 'LpKKb9dnZwQUKjkeDuXDZ6n3NgeD1uN50pvk9MYj',
    # }

    # res = requests.get(url, headers=headers)
    # lat = str(res.json()['addresses'][0]['y'])
    # lng = str(res.json()['addresses'][0]['x'])
 
    # context = {
    #     'lat' : lat,
    #     'lng' : lng,
    # }
    # return render(request, 'restaurants/detail.html', context)

    return render(request, "articles/map.html")
def map2(request):
    return render(request, "articles/map2.html")


# 좋아요 기능
def like(request, pk):
    review = Review.objects.get(pk=pk)
    if request.user not in review.like_users.all():
        review.like_users.add(request.user)
        is_like = True
    else:
        review.like_users.remove(request.user)
        is_like = False

    data = {
        "isLike": is_like,
        "likeCount": review.like_users.count(),
    }

    return JsonResponse(data)

