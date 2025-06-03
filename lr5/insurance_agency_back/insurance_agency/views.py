from itertools import chain
import logging
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView

from .forms import EmployeeForm, CustomerForm, OwnerForm, RealtyForm, DealForm, DealUpdateForm, DealAdminForm, \
    CustomerAdminForm, EmployeeAdminForm
from .models import Employee, UserProfile, Customer, Owner, Realty, Deal


logger = logging.getLogger(__name__)


class EmployeeCreateView(LoginRequiredMixin, CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'form.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        user = UserProfile.objects.get(user=self.request.user)

        if Owner.objects.filter(user=user).exists() or Customer.objects.filter(user=user).exists():
            messages.error(self.request,
            "You are already registered as owner or customer. You can't be an employee."
            "The entered data will not be written to the database.")
            logger.warning(f"User {user} already registered as owner or customer")
            return redirect('profile')

        if Employee.objects.filter(user=user).exists():
            messages.error(self.request, "You are already registered as an employee. "
                                         "The entered data will not be written to the database.")
            logger.warning(f"User {user} already registered as employee")
            return redirect('profile')

        form.instance.user = user

        self.object = form.save(commit=False)
        self.object.image = self.request.FILES.get('image')
        self.object.save()

        auth_user = self.request.user
        auth_user.is_staff = True
        auth_user.save()

        return super().form_valid(form)


class EmployeeAdminUpdateView(LoginRequiredMixin, UpdateView):
    model = Employee
    form_class = EmployeeAdminForm
    template_name = 'form.html'
    success_url = reverse_lazy('employees')


class EmployeeAdminCreateView(LoginRequiredMixin, CreateView):
    model = Employee
    form_class = EmployeeAdminForm
    template_name = 'form.html'
    success_url = reverse_lazy('employees')

    def form_valid(self, form):
        user = form.instance.user

        if Owner.objects.filter(user=user).exists() or Customer.objects.filter(user=user).exists():
            messages.error(self.request,
            "You are already registered as owner or customer. You can't be an employee."
            "The entered data will not be written to the database.")
            logger.warning(f"User {user} already registered as owner or customer")
            return redirect('employees')

        if Employee.objects.filter(user=user).exists():
            messages.error(self.request, "You are already registered as an employee. "
                                         "The entered data will not be written to the database.")
            logger.warning(f"User {user} already registered as employee")
            return redirect('employees')


        user.user.is_staff = True
        user.user.save()
        form.instance.user = user
        return super().form_valid(form)


def employees(request):
    employees = Employee.objects.all()
    return render(request, 'insurance_agency/employees.html',
                  {"employees": employees})


class CustomerCreateView(LoginRequiredMixin, CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'form.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        user = UserProfile.objects.get(user=self.request.user)

        if Customer.objects.filter(user=user).exists():
            messages.error(self.request,
            "You are already registered as the customer."
            "The entered data will not be written to the database.")
            logger.warning(f"User {user} already registered customer")
            return redirect('profile')

        user.is_customer = True
        form.instance.user = user
        user.save()
        return super().form_valid(form)


class CustomerAdminCreateView(LoginRequiredMixin, CreateView):
    model = Customer
    form_class = CustomerAdminForm
    template_name = 'form.html'
    success_url = reverse_lazy('customers')

    def form_valid(self, form):
        user = form.instance.user
        user.is_customer = True
        user.save()
        form.instance.user = user
        return super().form_valid(form)


class CustomerAdminUpdateView(LoginRequiredMixin, UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'form.html'
    success_url = reverse_lazy('customers')


def customers(request):
    customers = Customer.objects.all()
    return render(request, 'insurance_agency/customers.html',
                  {"customers": customers})


class OwnerCreateView(LoginRequiredMixin, CreateView):
    model = Owner
    form_class = OwnerForm
    template_name = 'form.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        user = UserProfile.objects.get(user=self.request.user)

        if Owner.objects.filter(user=user).exists():
            messages.error(self.request,
                           "You are already registered as the owner."
                           "The entered data will not be written to the database.")
            logger.warning(f"User {user} already registered owner")
            return redirect('profile')

        user.is_owner = True
        form.instance.user = user
        user.save()
        return super().form_valid(form)


def insurances(request):
    insurances = Realty.objects.all().order_by('-id').exclude(is_in_deal=True)

    query = request.GET.get("q", "")
    sort_by = request.GET.get("sort_by", "-id")

    insurances = insurances.filter(
        Q(type__name__icontains=query)
    )

    if sort_by:
        insurances = insurances.order_by(sort_by)

    logger.info(f"Returned queryset with filter '{query}' and sorted by '{sort_by}' ")
    return render(request, "insurance_agency/insurances.html",
                  { "insurances": insurances,
                            "offers": len(insurances)})


def my_insurances(request):
    insurances = (Realty.objects.filter(owner=Owner.objects
                                    .get(user=UserProfile.objects
                                         .get(user=request.user)))
               .order_by('-id'))

    query = request.GET.get("q", "")
    sort_by = request.GET.get("sort_by", "-id")

    insurances = insurances.filter(
        Q(name__icontains=query)
    )

    if sort_by:
        insurances = insurances.order_by(sort_by)
    logger.info(f"Returned user owned insurances queryset with filter '{query}' and sorted by '{sort_by}' ")
    return render(request, "insurance_agency/insurances.html",
                  { "insurances": insurances,
                            "offers": len(insurances)})


def insurance(request, id):
    realty = Realty.objects.get(id=id)

    user = UserProfile.objects.get(user=request.user)
    is_current_owner = True if realty.owner.user == user else False
    is_customer = True if user.is_customer and not is_current_owner else False

    if request.user.is_superuser:
        is_current_owner = True
        is_customer = False

    return render(request, "insurance_agency/realty.html",
                  { "realty": realty,
                            "is_owner": is_current_owner,
                            "is_customer": is_customer})


class RealtyCreateView(LoginRequiredMixin, CreateView):
    model = Realty
    form_class = RealtyForm
    template_name = 'form.html'
    success_url = reverse_lazy('insurances-list')

    def form_valid(self, form):
        user = UserProfile.objects.get(user=self.request.user)
        owner = Owner.objects.get(user=user)

        if owner:
            form.instance.owner = owner
            return super().form_valid(form)
        else:
            logger.warning(f"User {user} hasn't got owner profile yet")
            return redirect("assign-owner")


class RealtyUpdateView(LoginRequiredMixin, UpdateView):
    model = Realty
    form_class = RealtyForm
    template_name = 'form.html'
    success_url = reverse_lazy('insurances-list')


class RealtyDeleteView(LoginRequiredMixin, DeleteView):
    model = Realty
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('insurances-list')


class DealCreateView(LoginRequiredMixin, CreateView):
    model = Deal
    form_class = DealForm
    template_name = 'form.html'
    success_url = reverse_lazy('my-deals')

    def dispatch(self, request, *args, **kwargs):
        self.realty = get_object_or_404(Realty, pk=kwargs['realty_pk'])
        self.realty.is_in_deal = True
        self.realty.save()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = UserProfile.objects.get(user=self.request.user)
        customer = get_object_or_404(Customer, user=user)

        form.instance.customer = customer
        form.instance.realty = self.realty
        form.instance.owner = self.realty.owner
        logger.info(f"{form.instance.owner} and {form.instance.customer} make a deal "
                    f"for {form.instance.realty} - {form.instance.realty.price}")
        return super().form_valid(form)


class DealAdminCreateView(LoginRequiredMixin, CreateView):
    model = Deal
    form_class = DealAdminForm
    template_name = 'form.html'
    success_url = reverse_lazy('deals')


    def form_valid(self, form):
        realty = form.instance.realty
        form.instance.owner = realty.owner
        realty.is_in_deal = True
        realty.save()
        logger.info(f"{form.instance.owner} and {form.instance.customer} make a deal "
                    f"for {form.instance.realty} - {form.instance.realty.price}")
        return super().form_valid(form)


class DealUpdateView(LoginRequiredMixin, UpdateView):
    model = Deal
    form_class = DealUpdateForm
    template_name = 'form.html'
    success_url = reverse_lazy('deals')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        employee = getattr(self.object, "employee", None)
        if employee is None:
            self.object.employee = Employee.objects.get(user=UserProfile.objects.get(user=request.user))
            self.object.save()
        return super().dispatch(request, *args, **kwargs)


class DealDeleteView(LoginRequiredMixin, DeleteView):
    model = Deal
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('deals')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        logger.info(f"Deal {self.object.pk} deleted")
        realty = getattr(self.object, "realty", None)
        if realty is not None:
            realty.is_in_deal = False
            realty.save()
        return super().dispatch(request, *args, **kwargs)


def deals(request):
    deals = Deal.objects.all()
    return render(request, "insurance_agency/deals.html",
                  {"deals": deals})


def my_deals(request):
    user = UserProfile.objects.get(user=request.user)
    owner_deals = Deal.objects.none()
    customer_deals = Deal.objects.none()

    if user.is_owner:
        owner = Owner.objects.get(user=user)
        owner_deals = Deal.objects.filter(owner=owner)

    if user.is_customer:
        customer = Customer.objects.get(user=user)
        customer_deals = Deal.objects.filter(customer=customer)

    deals = list(chain(owner_deals, customer_deals))
    logger.info(f"Returned user {user} deals queryset")
    return render(request, "insurance_agency/deals.html",
                  {"deals": deals})