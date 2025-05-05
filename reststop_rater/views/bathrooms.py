from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from ..forms import ReviewForm
from ..models.bathroom import Bathroom
from ..services.review import update_bathroom_rating_after_review_change
from ..services.bathroom import update_bathroom_rating
from ..services.gmapsapi import get_all_photo_urls

class BathroomDetail(View):
    template = "bathroomdetail.html"

    def get(self, request, id):
        bathroom = get_object_or_404(Bathroom, id=id)
        reviews = bathroom.reviews.all()
        form = ReviewForm()
        photo_urls = get_all_photo_urls(bathroom.gmaps_id)

        context = {
            'bathroom': bathroom,
            'reviews': reviews,
            'form': form,
            'photo_urls': photo_urls,
        }

        if not request.user.is_authenticated:
            context['login_redirect_url'] = request.get_full_path()

        return render(request, self.template, context)

    def post(self, request, id):
        bathroom = get_object_or_404(Bathroom, id=id)

        if not request.user.is_authenticated:
            return redirect(f'/login/?next={request.path}')

        form = ReviewForm(request.POST)

        if all(key in request.POST for key in ['name', 'address', 'lat', 'long']):
            bathroom.name = request.POST.get("name")
            bathroom.address = request.POST.get("address")
            bathroom.latitude = request.POST.get("lat")
            bathroom.longitude = request.POST.get("long")
            bathroom.save()
            
            print("Updated Bathroom:", bathroom)
            return redirect("bathroom_detail", id=id)
        
        elif form.is_valid():
            existing_review = bathroom.reviews.filter(user=request.user).first()

            if existing_review:
                existing_review.rating = form.cleaned_data["rating"]
                existing_review.comment = form.cleaned_data["comment"]
                existing_review.save()
                updated_review = existing_review

            else:
                new_review = form.save(commit=False)
                new_review.user = request.user
                new_review.bathroom = bathroom
                new_review.save()
                updated_review = new_review


            update_bathroom_rating_after_review_change(updated_review)
            return redirect("bathroom_detail", id=id)
        
        photo_url = bathroom.photo_url or "/static/no-image.jpg"
        reviews = bathroom.reviews.all()
        return render(request, self.template, {
            "bathroom": bathroom,
            "reviews": reviews,
            "form": form,
            'photo_url': photo_url,
        })
    
class ReportView(View):
    def post(self, request, id, response):
        bathroom = get_object_or_404(Bathroom, id=id)
        vote_key = f"report_vote_{id}"
        previous_vote = request.POST.get("previous_vote") or request.COOKIES.get(vote_key)
        response_obj = redirect("bathroom_detail", id=bathroom.id) if "bathroom_detail" in request.path else redirect("/nearby/")

        if previous_vote == response:
            if response == "yes":
                bathroom.report_yes = max(bathroom.report_yes - 1, 0)
            elif response == "no":
                bathroom.report_no = max(bathroom.report_no - 1, 0)
            bathroom.save()
            response_obj.delete_cookie(vote_key)
            return response_obj

        if previous_vote == "yes" and response == "no":
            bathroom.report_yes = max(bathroom.report_yes - 1, 0)
            bathroom.report_no += 1
        elif previous_vote == "no" and response == "yes":
            bathroom.report_no = max(bathroom.report_no - 1, 0)
            bathroom.report_yes += 1
        
        elif previous_vote is None:
            if response == "yes":
                bathroom.report_yes += 1
            elif response == "no":
                bathroom.report_no += 1

        bathroom.save()
        response_obj.set_cookie(vote_key, response, max_age=60 * 60 * 24 * 30)
        return response_obj
    
class QuickRateView(View):
    def post(self, request, id):
        bathroom = get_object_or_404(Bathroom, id=id)
        
        try:
            rating = int(request.POST.get("rating"))
        except (TypeError, ValueError):
            return redirect(request.META.get("HTTP_REFERER", "/"))

        if rating < 1 or rating > 5:
            return redirect(request.META.get("HTTP_REFERER", "/"))

        cookie_key = f"quick_rate_{id}"
        previous_rating = request.COOKIES.get(cookie_key)
        response = redirect(request.META.get("HTTP_REFERER", "/"))

        if str(previous_rating) == str(rating):
            bathroom.quick_rate[str(rating)] = max(bathroom.quick_rate.get(str(rating), 0) - 1, 0)
            bathroom.save(update_fields=["quick_rate"])
            update_bathroom_rating(bathroom)
            response.delete_cookie(cookie_key)
            return response

        if previous_rating:
            bathroom.quick_rate[str(previous_rating)] = max(bathroom.quick_rate.get(str(previous_rating), 0) - 1, 0)

        bathroom.quick_rate[str(rating)] = bathroom.quick_rate.get(str(rating), 0) + 1
        bathroom.save(update_fields=["quick_rate"])
        update_bathroom_rating(bathroom)
        response.set_cookie(cookie_key, rating, max_age=60 * 60 * 24 * 30)

        return response


