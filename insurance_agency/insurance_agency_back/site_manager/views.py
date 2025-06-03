import calendar
import json
import logging
import pytz
import requests
from http import HTTPStatus
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import Http404
from django.shortcuts import render, redirect
from django.utils.timezone import now, localtime

from .forms import CustomRegistrationForm
from .models import AboutCompany, FAQ, PrivacyPolicy, Vacancy, Contacts
from articles.models import Article
from insurance_agency.models import Employee, UserProfile, Owner, Customer

from .stats import get_deals_count, get_average_age, get_employees_stats, get_realty_stats
from insurance_agency.models import Deal, Realty

logger = logging.getLogger(__name__)

def home(request):
    last_article = Article.objects.last()
    if not last_article:
        last_article = ""

    utc_now = now().astimezone(tz=pytz.utc)
    local_now = localtime(utc_now)

    logger.debug(f"UTC: {utc_now}")
    logger.debug(f"LOCAL: {local_now}")

    cal = calendar.TextCalendar()
    text_calendar = cal.formatmonth(local_now.year, local_now.month)

    try:
        response = requests.get("https://catfact.ninja/fact")
        if response.status_code == HTTPStatus.OK:
            response_body = json.loads(response.content)
            cat_fact = response_body["fact"]
        else:
            logger.error("Unable to access cat-fact API")
            cat_fact = "No cat fact ☹"
    except Exception:
        cat_fact = "No cat fact ☹"

    try:
        response = requests.get("https://dog.ceo/api/breeds/image/random")
        data = response.json()
        dog_image_url = data["message"]
    except Exception:
        dog_image_url = "No dog picture ☹"
        logger.error("Unable to access dog-picture API")

    context = {
        "utc_now": utc_now.strftime("%d/%m/%Y %H:%M"),
        "local_now": local_now,
        "text_calendar": text_calendar,
        "article": last_article,
        "cat_fact": cat_fact,
        "dog_image_url": dog_image_url
    }
    return render(request, "site_manager/home.html",
    context)


def about(request):
    company = AboutCompany.objects.last()
    if not company:
        return Http404("There is no info about company")
    return render(request, "site_manager/about.html",
    {"company": company})


def faq(request):
    faq = FAQ.objects.all()
    return render(request, 'site_manager/faq.html',
    {"faq": faq})


def contacts(request):
    employees = Contacts.objects.all()
    return render(request, 'site_manager/contacts.html',
                  {"contacts": employees})


def privacy_policy(request):
    policy = PrivacyPolicy.objects.last()
    if not policy: policy = ""
    return render(request, 'site_manager/privacy_policy.html',
                  {"privacy": policy})


def vacancies(request):
    vacancies = Vacancy.objects.all()
    return render(request, 'site_manager/vacancy.html',
                  {"vacancies" : vacancies})


def register(request):
    message = ""
    if request.method == "POST":
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("home")
        else:
            logger.warning(f"User {request.user} send not valid registration form")
            message = "Form is not valid!"
    else:
        form = CustomRegistrationForm()
    return render(request, "form.html",
                  {"form": form, "message": message})


def logout(request):
    auth_logout(request)
    return redirect("home")


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect("profile")
    else:
        logger.info(f"User {request.user} was redirected to login form")
        form = AuthenticationForm()
    return render(request, "registration/login.html",
                  {"form": form})


def profile(request):
    user = UserProfile.objects.get(user=request.user)
    employee = Employee.objects.filter(user=user).first()
    owner = Owner.objects.filter(user=user).first()
    customer = Customer.objects.filter(user=user).first()
    return render(request, 'site_manager/profile.html',
                  { "employee": employee,
                            "owner": owner,
                            "customer": customer})


def statistics(request):
    get_employees_stats(Deal.objects.all())
    get_realty_stats(Realty.objects.all())
    context = {
        "deals_count": get_deals_count(Deal.objects.all()),
        "customers_average_age": round(get_average_age(Customer.objects.all()), 3),
        "employees_average_age": round(get_average_age(Employee.objects.all()), 3),
        "owners_average_age": round(get_average_age(Owner.objects.all()), 3),
        "employees_stats_picture": "/media/stats/employees_sales_stats.png",
        "realty_stats_picture": "/media/stats/realty_pie_chart.png"
    }
    return render(request, 'site_manager/statistics.html', context)
