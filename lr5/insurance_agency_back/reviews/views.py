import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from .models import Review
from .forms import ReviewForm
from insurance_agency.models import UserProfile


logger = logging.getLogger(__name__)


# Create your views here.
def review(request):
    reviews = Review.objects.order_by('-created_at')[:5]
    return render(request, 'reviews/review.html',
                  {"reviews": reviews})


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'form.html'
    success_url = reverse_lazy('reviews')

    def form_valid(self, form):
        form.instance.author = UserProfile.objects.get(user=self.request.user)
        logger.info(f"Review created by {form.instance.author}")
        return super().form_valid(form)


class ReviewListView(LoginRequiredMixin, ListView):
    model = Review
    template_name = 'reviews/review.html'
    context_object_name = 'reviews'

    def get_queryset(self):
        try:
            profile = UserProfile.objects.get(user=self.request.user)
        except UserProfile.DoesNotExist:
            logger.warning(f"User {self.request.user} hasn't got a profile")
            raise Http404("Профиль пользователя не найден.")
        return Review.objects.filter(author=profile)
