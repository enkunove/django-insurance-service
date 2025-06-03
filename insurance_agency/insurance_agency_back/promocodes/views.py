from django.shortcuts import render
import logging

from .models import Promocode

logger = logging.getLogger(__name__)

# Create your views here.
def promocodes(request):
    proms = Promocode.objects.order_by('-available_period')[:10]
    logger.info(f"Returned promo codes list")
    return render(request, "promocodes/promocodes.html",
                  {"promocodes": proms})