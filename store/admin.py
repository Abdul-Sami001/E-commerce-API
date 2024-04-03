from django.contrib import admin, messages
from . import models
#from django.contrib.contenttypes.admin import GenericTabularInline
from django.db.models import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse
#from tags.models import TaggedItem
# Register your models here.

class InventoryFilter(admin.SimpleListFilter):

    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low')
        ]

    def queryset(self, request, queryset):
        if self.value() == '<10':
            return queryset.filter(inventory__lte=10)
#this code depends on the tag app a seperate
#we should not add these code instead use another app to connect these apps
# class TagInline(GenericTabularInline):
#     autocomplete_fields = ['tag']
#     model = TaggedItem


# customizing admin panel specific models
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['collection']
    prepopulated_fields = {
        'slug' : ['title']
    }
    actions = ['clear_inventory']
    #inlines = [TagInline]
    list_display = ["title", "price", "inventory_status", "collection"]
    list_editable = ["price"]
    list_per_page = 10
    list_filter = ['collection', 'last_update', InventoryFilter]
    search_fields = ['title']
    @admin.display(ordering="inventory")
    def inventory_status(self, product):
        if product.inventory < 10:
            return "Low"
        else:
            return "Ok"
    @admin.action(description="Clear inventory")
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
                request,
            f'{updated_count} products were successfully updated.'
                
            )

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "membership"]
    list_editable = ["membership"]
    list_per_page = 10
    list_select_related = ['user']
    ordering = ["user__first_name", "user__last_name"]
    search_fields = ['first_name__istartswith', 'last_name__istartswith']


class OrderItemInline(admin.TabularInline):
    autocomplete_fields = ['product']
    min_num = 1
    max_num =10
    model = models.OrderItem
    extra = 0
    


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ["customer"]
    inlines = [OrderItemInline]
    list_display = ["id", "placed_at", "customer"]


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ["title", "products_count"]
    search_fields = ['title']
    @admin.display(ordering="products_count")
    def products_count(self, collection):
        url = (
            reverse('admin:store_product_changelist')
            + '?'
            + urlencode(
                {
                    'collection__id': str(collection.id)
                }
            )
            )
        return format_html("<a href='{}'>{}</a>",url, collection.products_count)
    

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(products_count=Count("product"))
