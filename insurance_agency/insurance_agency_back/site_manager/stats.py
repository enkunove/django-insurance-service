import datetime
import os
import sys

import django
import statistics

from django.db.models import QuerySet
from matplotlib import pyplot as plt

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "insurance_agency_back.settings")
django.setup()

from insurance_agency.models import UserProfile, Realty, Deal



def get_employees_stats(deals: QuerySet[Deal]):
    deal_counts = {}

    for deal in deals:
        if deal.employee:
            deal_counts[deal.employee] = deal_counts.get(deal.employee, 0) + 1

    names = [emp.user.full_name for emp in deal_counts.keys()]
    counts = list(deal_counts.values())

    plt.figure(figsize=(10, 6))
    plt.bar(names, counts, color="skyblue")
    plt.title("Количество сделок по сотрудникам")
    plt.xlabel("Сотрудник")
    plt.ylabel("Количество сделок")
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.savefig(os.path.join(BASE_DIR, "media\\", "stats\\employees_sales_stats.png"))
    plt.show()
    plt.close()


def get_deals_count(deals: QuerySet[Deal]):
    return sum(
        deal.realty.price
        for deal in deals
        if getattr(deal, 'realty', None) and getattr(deal.realty, 'price', None) is not None
    )


def get_average_age(peoples):
    ages = []
    current_year = datetime.date.today().year
    for profile in peoples:
        birth_date = getattr(getattr(profile, 'user', None), 'birth_day', None)
        if birth_date and birth_date.year <= current_year:
            ages.append(current_year - birth_date.year)
    if not ages:
        raise statistics.StatisticsError("No valid birth dates to calculate average age.")
    return statistics.mean(ages)


def get_realty_stats(insurances: QuerySet[Realty]):
    realty_counts = {}

    for realty in insurances:
        if realty.type:
            realty_counts[realty.type] = realty_counts.get(realty.type, 0) + 1

    types = [type.name for type in realty_counts.keys()]
    counts = list(realty_counts.values())

    plt.figure(figsize=(8, 8))
    plt.pie(counts, labels=types, autopct='%1.1f%%', startangle=140)
    plt.title('Распределение недвижимости по типам')
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig(os.path.join(BASE_DIR, "media\\", "stats\\realty_pie_chart.png"))
    plt.show()
    plt.close()
