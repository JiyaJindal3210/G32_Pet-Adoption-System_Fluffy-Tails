from django.contrib import admin
from .models import Breeds, Pet
from django.contrib import admin
from .models import ContactMessage


class BreedsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'species')  
    
class PetAdmin(admin.ModelAdmin):
    list_display = ('pet_id', 'name', 'gender', 'enrolled_breeds_display')
    radio_fields = {'gender': admin.HORIZONTAL}
    filter_horizontal = ('breeds',)
    search_fields = ('name',)
    list_filter = ('gender', 'is_available')

    def enrolled_breeds_display(self, obj):
        breeds_names = []
        for breed in obj.breeds.all():
            breeds_names.append(breed.name)
        return ", ".join(breeds_names)

admin.site.register(Breeds, BreedsAdmin)
admin.site.register(Pet, PetAdmin)
admin.site.register(ContactMessage)
