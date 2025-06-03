from django.contrib import admin

from .models import TypeOfWork, UserProfile, Employee, Owner, Customer, RealtyType, Realty, Deal


@admin.register(TypeOfWork)
class TypeOfWorkAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]
    search_fields = ["name"]
    list_per_page = 10
    readonly_fields = ["id"]


@admin.register(UserProfile)
class UserAdmin(admin.ModelAdmin):
    list_display = ["full_name", "phone_number", "email"]
    search_fields = ["full_name", "email"]
    sortable_by = ["email", "user__username"]
    list_per_page = 20
    readonly_fields = ["id"]


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ["full_name", "phone_number", "email", "work_type"]
    search_fields = ["user__full_name", "work_type"]
    list_per_page = 10
    readonly_fields = ["id", "full_name", "phone_number", "email"]

    def full_name(self, obj):
        return obj.user.full_name
    full_name.short_description = "Full Name"

    def phone_number(self, obj):
        return obj.user.phone_number
    phone_number.short_description = "Phone Number"

    def email(self, obj):
        return obj.user.email
    email.short_description = "Email"


class RealtyInline(admin.TabularInline):
    model = Realty
    extra = 1
    readonly_fields = ["id"]
    fields = ["name", "type", "price", "area", "built_year", "photo"]


@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ["full_name", "phone_number", "email", "rating", "preferred_contact_time"]
    search_fields = ["user__full_name", "user__email"]
    list_per_page = 10
    readonly_fields = ["id", "full_name", "phone_number", "email"]
    inlines = [RealtyInline]

    def full_name(self, obj):
        return obj.user.full_name
    full_name.short_description = "Full Name"

    def phone_number(self, obj):
        return obj.user.phone_number
    phone_number.short_description = "Phone Number"

    def email(self, obj):
        return obj.user.email
    email.short_description = "Email"



@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["full_name", "phone_number", "email", "budget", "is_vip"]
    search_fields = ["user__full_name", "user__email"]
    list_filter = ["is_vip"]
    list_per_page = 10
    readonly_fields = ["id", "full_name", "phone_number", "email"]

    def full_name(self, obj):
        return obj.user.full_name
    full_name.short_description = "Full Name"

    def phone_number(self, obj):
        return obj.user.phone_number
    phone_number.short_description = "Phone Number"

    def email(self, obj):
        return obj.user.email
    email.short_description = "Email"


@admin.register(RealtyType)
class RealtyTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "category"]
    search_fields = ["name", "category"]
    list_filter = ["category"]
    list_per_page = 10
    readonly_fields = ["id"]


@admin.register(Realty)
class RealtyAdmin(admin.ModelAdmin):
    list_display = ["owner_full_name", "name", "price", "built_year"]
    search_fields = ["owner_full_name", "built_year", "name"]
    list_filter = ["price", "area", "built_year"]
    list_per_page = 10
    readonly_fields = ["id", "owner_full_name"]

    def owner_full_name(self, obj):
        return obj.owner.user.full_name
    owner_full_name.short_description = "Owner Full Name"


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ["owner_full_name", "customer_full_name", "insurance_name", "insurance_price", "deal_type", "status"]
    search_fields = ["insurance_name", "owner_full_name", "customer_full_name", "insurance_price"]
    list_filter = ["deal_type", "status"]
    list_per_page = 10
    readonly_fields = ["id", "owner_full_name", "customer_full_name", "insurance_name", "insurance_price"]

    def owner_full_name(self, obj):
        return obj.owner.user.full_name
    owner_full_name.short_description = "Owner Full Name"

    def customer_full_name(self, obj):
        return obj.customer.user.full_name
    customer_full_name.short_description = "Customer Full Name"

    def insurance_name(self, obj):
        return obj.realty.name
    insurance_name.short_description = "insurance Name"

    def insurance_price(self, obj):
        return obj.realty.price
    insurance_price.short_description = "insurance Price"
