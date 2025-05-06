from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import Breeds,Pet,Species,Order,ContactMessage
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
import requests



def dashboard1_view(request):
    return render(request, 'dashboard1.html')

@login_required
def home_view(request):
    pets = Pet.objects.filter(is_available=True)
    return render(request, 'home.html', {'pets': pets})


@login_required
def index_view(request):
    pets = Pet.objects.filter(is_available=True)
    return render(request, 'index.html', {'pets': pets})

@login_required
def learn2(request):
    return render(request, 'learnmore2.html')

@login_required
def learn3(request):
    return render(request, 'learnmore3.html')

@login_required
def aboutus2(request):
    return render(request, 'aboutus2.html')

@login_required
def aboutus(request):
    flask_api_url = "http://127.0.0.1:5000/aboutus"

    try:
        response = requests.get(flask_api_url)
        if response.status_code == 200:
            about_info = response.json()
        else:
            about_info = {"error": "Could not fetch About Us information."}
    except requests.exceptions.RequestException as e:
        about_info = {"error": f"Error occurred: {e}"}

    return render(request, 'aboutus.html', {'about_info': about_info})

@login_required
def adopting_pets(request):
    return render(request, 'adoptingpets.html')

@login_required
def foundation(request):
    return render(request, 'foundation.html')

@login_required
def dog_puppies_adoption(request):
    return render(request, 'dogPuppiesAdoption.html')

@login_required
def behavior_dog(request):
    return render(request, 'behavior_dog.html')

@login_required
def cat_kitten_adoption(request):
    return render(request, 'catKittenAdoption.html')

@login_required
def behavior_cat(request):
    return render(request, 'behavior_cat.html')

@login_required
def contact(request):
    return render(request, 'contactus.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        cpassword = request.POST.get('cpassword', '')
        phone = request.POST.get('phone', '').strip()
 
        if password != cpassword:
            messages.error(request, 'Passwords do not match')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already used')
        else:
            try:
                validate_password(password)
                user = User.objects.create_user(
                    username=username, email=email, password=password)
                messages.success(request, 'Registration successful! You can now login.')
                return redirect('login')
            except ValidationError as e:
                for error in e.messages:
                    messages.error(request, error)

        context = {'username': username, 'email': email}
        return render(request, 'register.html', context)

    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        selected_role = request.POST.get('role')

        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = None

        if user:
            if (selected_role == 'admin' and user.is_superuser) or (selected_role == 'user' and not user.is_superuser):
                login(request, user)
                if selected_role == 'admin':
                    return redirect('view_profile_admin')  
                else:
                    return redirect('view_profile')  
            else:
                messages.error(request, 'Role mismatch or unauthorized access.')
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'login.html')


# def view_user_profile_by_id(request, user_id):
#     user = get_object_or_404(User, id=user_id)
#     return render(request, 'user_profile.html', {'user': user})

@login_required
def view_profile(request):
    return render(request, 'user_profile.html', {
        'user': request.user
    })

@login_required
def view_profile_admin(request):
    return render(request, 'admin_profile.html', {
        'user': request.user
    })

@login_required
def dashboard_view(request):
    if not request.user.is_superuser:
        return redirect('home')
    
    return render(request, 'dashboard.html', {'user': request.user})

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def add_breed_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        species_name = request.POST.get('species_name')

        species, created = Species.objects.get_or_create(name=species_name)

        breed = Breeds(name=name, species=species)
        breed.save()

        messages.success(request, f'Breed "{name}" added successfully!')
        return redirect('addbreed')

    breeds = Breeds.objects.all()
    return render(request, 'addbreed.html', {'breeds': breeds})

@login_required
def register_pet_view(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You are not authorized to add pets.")

    breeds = Breeds.objects.all()

    if request.method == "POST":
        name = request.POST.get('name')
        gender = request.POST.get('gender')
        breed_ids = request.POST.getlist('breeds')
        age = request.POST.get('age')
        image = request.POST.get('image')

        breed_ids = [bid for bid in breed_ids if bid.isdigit()]

        if not name:
            messages.error(request, "Name is mandatory.")
        elif not breed_ids:
            messages.error(request, "Please select at least one breed.")
        elif not gender:
            messages.error(request, "Gender is required.")
        else:
            try:
                pet = Pet.objects.create(
                    name=name,
                    gender=gender,
                    age=int(age) if age else 0,
                    image=image
                )
                pet.breeds.set(breed_ids)
                messages.success(request, f"Pet {name} registered successfully!")
                return redirect('home')
            except Exception as e:
                messages.error(request, f"An error occurred: {e}")

    return render(request, 'registerpet.html', {'breeds': breeds})

@login_required
def breed_pet_list_view(request, breed_id):
    breed = Breeds.objects.get(id=breed_id)
    pets = breed.pet_set.all().select_related('adopted_by')
    return render(request, 'breed_pet_list.html', context={'breed': breed, 'pets': pets})

@login_required
def delete_breed_view(request, breed_id):
    try:
        breed = Breeds.objects.get(id=breed_id)
    except Breeds.DoesNotExist:
        messages.error(request, "Breed not found.")
        return redirect('addbreed')

    if request.method == "POST":
        breed.delete()
        messages.success(request, f'Breed "{breed.name}" deleted successfully.')
        return redirect('addbreed')

    return render(request, "delete_breed.html", {"breed": breed})

def get_full_name(self):
    full_name = '%s %s' % (self.first_name, self.last_name)
    return full_name.strip()

@login_required
def update_breed_view(request, breed_id):
    try:
        breed = Breeds.objects.get(id=breed_id)
    except Breeds.DoesNotExist:
        messages.error(request, "Breed not found.")
        return redirect('addbreed')

    if request.method == 'POST':
        name = request.POST.get("name", "").strip()

        if name:
            breed.name = name
            breed.save()
            messages.success(request, f'Breed "{name}" updated successfully.')
            return redirect('addbreed')

    return render(request, "update_breed.html", {"breed": breed})

@login_required
def dogs_view(request):
    dogs = Pet.objects.filter(breeds__species__name__iexact="Dog",is_available=True).distinct()
    return render(request, 'dog.html', {'pets': dogs})

@login_required
def cats_view(request):
    cats = Pet.objects.filter(breeds__species__name__iexact="Cat",is_available=True).distinct()
    return render(request, 'cat.html', {'pets': cats})

@login_required
def add_to_cart(request, pet_id):
    cart = request.session.get('cart', [])
    if pet_id not in cart:
        cart.append(pet_id)
    request.session['cart'] = cart
    return redirect('view_cart')

@login_required
def remove_from_cart(request, pet_id):
    cart = request.session.get('cart', [])
    if pet_id in cart:
        cart.remove(pet_id)
    request.session['cart'] = cart
    return redirect('view_cart')

@login_required
def view_cart(request):
    cart = request.session.get('cart', [])
    cart_pets = Pet.objects.filter(pet_id__in=cart)
    return render(request, 'cart.html', {'cart_pets': cart_pets})


@login_required
def about_view(request):
    user = request.user
    flask_api_url = "http://127.0.0.1:5000/aboutus"
    jwt_token = request.session.get('jwt_token')

    headers = {
        'Authorization': f'Bearer {jwt_token}'  # Optional if your Flask route requires auth
    }

    try:
        response = requests.get(flask_api_url, headers=headers)
        if response.status_code == 200:
            about_info = response.json()
        else:
            about_info = {"error": "Could not fetch about us information"}
    except requests.exceptions.RequestException as e:
        about_info = {"error": f"Error occurred: {e}"}

    return render(request, 'about.html', {'user': user, 'about_info': about_info})

@login_required
def adopt_pets(request):
    if request.method == "POST":
        cart = request.session.get('cart', [])

        if not cart:
            messages.error(request, "Your cart is empty.")
            return redirect('cart')

        pets = Pet.objects.filter(pet_id__in=cart, is_available=True)

        if pets.exists():
            order = Order.objects.create(user=request.user)
            order.pets.set(pets)
            order.save()

            pets.update(is_available=False)

            request.session['cart'] = []

            messages.success(request, "Adoption successful!")
        else:
            messages.error(request, "Some pets were already adopted or unavailable.")

    return redirect('orders')

@login_required
def orders_view(request):
    orders = Order.objects.filter(user=request.user) if not request.user.is_superuser else Order.objects.all()

    if not request.user.is_superuser:
        updated_orders = orders.filter(status__in=["Accepted", "Rejected"])
        if updated_orders.exists():
            for order in updated_orders:
                if order.status == "Accepted":
                    messages.success(request, f"Great news! Your order #{order.id} has been accepted! 🐾")
                elif order.status == "Rejected":
                    messages.error(request, f"Sorry! Your order #{order.id} was rejected. 😢")

    return render(request, 'orders.html', {'orders': orders})

def is_admin(user):
    return user.is_superuser


@user_passes_test(is_admin)
def accept_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.status = 'Accepted'
    order.save()
    return HttpResponseRedirect(reverse('orders'))

@user_passes_test(is_admin)
def reject_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.status = 'Rejected'
    order.save()
    return HttpResponseRedirect(reverse('orders'))


@login_required
def view_messages(request):
    try:
        response = requests.get('http://127.0.0.1:5000/api/messages')
        if response.status_code == 200:
            all_messages = response.json()
            print("Flask messages fetched:", all_messages)  # Debugging output
        else:
            all_messages = []
            print("Failed to fetch messages, status code:", response.status_code)
    except Exception as e:
        print("Error fetching messages from Flask:", e)
        all_messages = []

    return render(request, 'view_messages.html', {'all_messages': all_messages})














from .forms import UserUpdateForm, ProfileUpdateForm
from .models import Profile

@login_required
def edit_profile(request):
    # Check if the user has a profile, and create it if not
    if not hasattr(request.user, 'profile'):
        Profile.objects.create(user=request.user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('view_profile')  # redirect to the profile page
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'edit_profile.html', {
        'u_form': u_form,
        'p_form': p_form
    })