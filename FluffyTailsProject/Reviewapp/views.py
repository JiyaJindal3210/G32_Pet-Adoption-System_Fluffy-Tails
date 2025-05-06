from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from .models import ContactMessage
import requests
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def contact_view(request):
    if request.method == 'POST':
        data = {
            'name': request.POST.get('name'),
            'email': request.POST.get('email'),
            'subject': request.POST.get('subject'),
            'message': request.POST.get('message')
        }
        # Send data to Flask API
        response = requests.post('http://127.0.0.1:5000/api/messages', json=data)
        if response.status_code == 201:
            return redirect('view_messages')  # Still works as is
    return render(request, 'contactus.html')
