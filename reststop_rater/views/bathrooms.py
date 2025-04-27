from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from ..forms import ReviewForm
from ..models.bathroom import Bathroom
from ..services.review import update_bathroom_rating_after_review_change

class BathroomDetail(View):
    template = "bathroomdetail.html"

    def get(self, request, id):
        bathroom = get_object_or_404(Bathroom, id=id)
        reviews = bathroom.reviews.all()
        form = ReviewForm()

        context = {
            'bathroom': bathroom,
            'reviews': reviews,
            'form': form,
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
        
        reviews = bathroom.reviews.all()
        return render(request, self.template, {
            "bathroom": bathroom,
            "reviews": reviews,
            "form": form,
        })