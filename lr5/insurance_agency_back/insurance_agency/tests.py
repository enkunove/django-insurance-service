import datetime
from decimal import Decimal
import pytest

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile


from insurance_agency.models import TypeOfWork, Employee, Owner, Customer, RealtyType, Realty, Deal, UserProfile


User = get_user_model()
pytestmark = pytest.mark.django_db


# Create your tests here.
class ModelsTestCase(TestCase):

    def setUp(self):
        # Создаем базового пользователя для связей
        self.user = User.objects.create_user(username="testuser", password="pass1234")
        self.user2 = User.objects.create_user(username="testuser2", password="pass1234")
        self.user3 = User.objects.create_user(username="testuser3", password="pass1234")

    def test_type_of_work(self):
        tow = TypeOfWork.objects.create(name="Plumbing", description="Pipe installation")
        self.assertEqual(str(tow), "Plumbing")

    def test_user_profile(self):
        up = UserProfile.objects.create(
            full_name="Иван Иванов",
            phone_number="+375291234567",
            email="ivan@example.com",
            birth_day=datetime.date(1990, 1, 1),
            is_customer=True,
            is_owner=False,
            time_zone="Europe/Minsk",
            user=self.user
        )
        self.assertTrue(up.pk)
        self.assertIn("Иван Иванов", str(up))
        self.assertIn("ivan@example.com", str(up))

    def test_employee(self):
        tow = TypeOfWork.objects.create(name="Electrician")
        up = UserProfile.objects.create(
            full_name="Петр Петров",
            phone_number="+375291112233",
            email="petr@example.com",
            birth_day=datetime.date(1985, 6, 15),
            is_customer=False,
            is_owner=False,
            time_zone="Europe/Minsk",
            user=self.user
        )
        emp = Employee.objects.create(
            user=up,
            work_type=tow,
            work_experience=5.5,
        )
        self.assertEqual(str(emp), f"Name: {up.full_name}\nWork experience: 5.5")

    def test_owner(self):
        up = UserProfile.objects.create(
            full_name="Анна Смирнова",
            phone_number="+375293334455",
            email="anna@example.com",
            birth_day=datetime.date(1978, 9, 10),
            is_customer=False,
            is_owner=True,
            time_zone="Europe/Minsk",
            user=self.user
        )
        owner = Owner.objects.create(user=up, rating=8.5)
        self.assertIn("Анна Смирнова", str(owner))
        self.assertEqual(owner.rating, 8.5)

    def test_customer(self):
        up = UserProfile.objects.create(
            full_name="Олег Сидоров",
            phone_number="+375294445566",
            email="oleg@example.com",
            birth_day=datetime.date(1995, 3, 20),
            is_customer=True,
            is_owner=False,
            time_zone="Europe/Minsk",
            user=self.user
        )
        customer = Customer.objects.create(user=up, budget=Decimal("100000.00"), is_vip=True)
        self.assertIn("Олег Сидоров", str(customer))
        self.assertEqual(customer.budget, Decimal("100000.00"))
        self.assertTrue(customer.is_vip)

    def test_realty_type(self):
        rt = RealtyType.objects.create(name="Apartment", category=RealtyType.RealtyCategory.RESIDENTIAL)
        self.assertIn("Apartment", str(rt))
        self.assertIn("RES", str(rt))

    def test_realty(self):
        up = UserProfile.objects.create(
            full_name="Виктор Иванов",
            phone_number="+375295556677",
            email="viktor@example.com",
            birth_day=datetime.date(1980, 7, 7),
            is_customer=False,
            is_owner=True,
            time_zone="Europe/Minsk",
            user=self.user
        )
        owner = Owner.objects.create(user=up, rating=9.0)
        rt = RealtyType.objects.create(name="House", category=RealtyType.RealtyCategory.RESIDENTIAL)
        realty = Realty.objects.create(
            type=rt,
            owner=owner,
            name="Sunny House",
            address="123 Sunny St",
            price=Decimal("250000.00"),
            area=Decimal("150.50"),
            built_year=1999,
            is_in_deal=False
        )
        self.assertIn("Sunny House", str(realty))
        self.assertIn("250000.00", str(realty))

    def test_deal(self):
        # Подготовка связанных моделей
        up_owner = UserProfile.objects.create(
            full_name="Владелец",
            phone_number="+375291111111",
            email="owner@example.com",
            birth_day=datetime.date(1975, 5, 5),
            is_customer=False,
            is_owner=True,
            time_zone="Europe/Minsk",
            user=self.user
        )
        owner = Owner.objects.create(user=up_owner)

        up_customer = UserProfile.objects.create(
            full_name="Покупатель",
            phone_number="+375292222222",
            email="customer@example.com",
            birth_day=datetime.date(1990, 2, 2),
            is_customer=True,
            is_owner=False,
            time_zone="Europe/Minsk",
            user=self.user2
        )
        customer = Customer.objects.create(user=up_customer)

        up_employee = UserProfile.objects.create(
            full_name="Сотрудник",
            phone_number="+375293333333",
            email="employee@example.com",
            birth_day=datetime.date(1988, 3, 3),
            is_customer=False,
            is_owner=False,
            time_zone="Europe/Minsk",
            user=self.user3
        )
        tow = TypeOfWork.objects.create(name="Agent")
        employee = Employee.objects.create(user=up_employee, work_type=tow, work_experience=3)

        rt = RealtyType.objects.create(name="Office", category=RealtyType.RealtyCategory.COMMERCIAL)
        realty = Realty.objects.create(
            type=rt,
            owner=owner,
            name="Big Office",
            address="456 Business Rd",
            price=Decimal("500000.00"),
            area=Decimal("300.00"),
            built_year=2010,
            is_in_deal=True
        )
        deal = Deal.objects.create(
            deal_type=Deal.DealType.SALE,
            status=Deal.DealStatus.ACTIVE,
            realty=realty,
            customer=customer,
            employee=employee,
            owner=owner,
            actual_end_date=datetime.date.today()
        )
        self.assertIn("Владелец", str(deal))
        self.assertIn("Покупатель", str(deal))
        self.assertIn("Big Office", str(deal))


class EmployeeTests(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create(username="testuser", password="12345")
        self.user_profile = UserProfile.objects.create(
            full_name="Full name",
            phone_number="+375336594567",
            email="email@example.com",
            birth_day=datetime.date(1980, 7, 17),
            is_customer=False,
            is_owner=False,
            time_zone="Europe/Moscow",
            user=self.user
        )
        self.work_type = TypeOfWork.objects.create(name="Manager")
        self.client.force_login(self.user)
        self.image_file = SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")

    def test_employee_create_view(self):
        url = reverse("admin-employee")
        data = {
            "work_type": self.work_type.id,
            "work_experience": 5,
            "image": self.image_file,
            "user": self.user_profile.id
        }

        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Employee.objects.filter(user=self.user_profile).exists())
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_staff)

    def test_employee_assign_view(self):
        url = reverse("assign-employee")
        data = {
            "work_type": self.work_type.id,
            "work_experience": 5,
            "image": self.image_file,
            "secret_code": "employee_secret_code"
        }

        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Employee.objects.filter(user=self.user_profile).exists())
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_staff)



class OwnerEmployeeTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="owneruser", password="12345")
        self.owner_user_profile = UserProfile.objects.create(
            full_name="Owner User",
            phone_number="+375336594562",
            email="owner@example.com",
            birth_day=datetime.date(1982, 2, 17),
            is_customer=False,
            is_owner=False,
            time_zone="Europe/Moscow",
            user=self.user
        )
        self.work_type = TypeOfWork.objects.create(name="Manager")
        Owner.objects.create(user=self.owner_user_profile)
        self.client.force_login(self.user)
        self.image_file = SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")


    def test_owner_assign_view(self):
        url = reverse("assign-owner")
        data = {
            "preferred_contact_time": "10.00-20.00",
            "notes": "Looking for a 2-bedroom apartment",
        }
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(Owner.objects.filter(user=self.owner_user_profile).exists())


    def test_employee_create_block_if_already_owner(self):
        url = reverse("admin-employee")
        data = {
            "work_type": self.work_type.id,
            "work_experience": 3,
            "image": self.image_file,
            "user": self.owner_user_profile.id
        }
        response = self.client.post(url, data, follow=True)
        self.user.refresh_from_db()
        self.assertFalse(Employee.objects.filter(user=self.owner_user_profile).exists())


class CustomerTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username="customeruser", password="12345")
        self.customer_user_profile = UserProfile.objects.create(
            full_name="Customer User",
            phone_number="+375336594588",
            email="customer@example.com",
            birth_day=datetime.date(1985, 2, 17),
            is_customer=False,
            is_owner=False,
            time_zone="Europe/Moscow",
            user=self.user
        )
        self.client.force_login(self.user)

    def test_customer_create_view(self):
        url = reverse("admin-customer")
        data = {
            "budget": 1000000,
            "notes": "Looking for a 2-bedroom apartment",
            "user": self.customer_user_profile.id,
            "is_vip": False
        }
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(Customer.objects.filter(user=self.customer_user_profile).exists())


    def test_customer_assign_view(self):
        url = reverse("assign-customer")
        data = {
            "budget": 1000000,
            "notes": "Looking for a 2-bedroom apartment",
        }
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(Customer.objects.filter(user=self.customer_user_profile).exists())


class RealtyTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="owneruser", password="12345")
        self.owner_user_profile = UserProfile.objects.create(
            full_name="Owner Realty",
            phone_number="+375336594562",
            email="owner_realty@example.com",
            birth_day=datetime.date(1982, 2, 17),
            is_customer=True,
            is_owner=True,
            time_zone="Europe/Moscow",
            user=self.user
        )
        self.owner = Owner.objects.create(user=self.owner_user_profile)
        self.client.force_login(self.user)
        self.image_file = SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")

    def test_realty_create(self):
        url = reverse("realty-add")
        data = {
            "name": "Luxury Flat",
            "type": "Apartment",
            "price": 1000000,
            "address": "123 Main St",
            "area": 100,
            "built_year": 2020,
            "photo": self.image_file,
        }

        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(Realty.objects.filter(owner=self.owner).exists())
