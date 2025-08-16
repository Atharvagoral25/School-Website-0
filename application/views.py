from django.shortcuts import render,redirect, HttpResponse
from application.models import *
from django.http import HttpResponseRedirect
from application.models import enquiry_table
from django.contrib import messages
from django.contrib.auth import authenticate, login 
from django.contrib.auth.decorators import login_required
from .urls import *
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.

def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'test.html')

def contact(request):
    return render(request, 'contact.html')

def choose(request):
    return render(request, 'choose.html')

def events(request):
    return render(request, 'events.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("dashboard")  # Redirect to the dashboard page after login
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "login.html")

def contact(request):
    if request.method == 'POST':
        a = request.POST.get('name')
        b = request.POST.get('email')
        c = request.POST.get('phone')
        d = request.POST.get('message')

        info = enquiry_table(name=a, email=b, phone=c, message=d)
        info.save()

        messages.success(request, 'Enquiry form submitted.')
        return redirect('contact')  # Redirect to the contact page after submission

    return render(request, 'contact.html')

def tables_view(request):
    # Redirect to the dashboard view
    return redirect('dashboard')

@login_required(login_url='login')
def dashboard(request):
    information = enquiry_table.objects.all()
    return render(request, 'dashboard.html', {'information': information})

def delete_record(request, id):
    if request.method == 'POST':
        try:
            data = enquiry_table.objects.get(pk=id)
            data.delete()
            messages.success(request, 'Record deleted successfully.')
        except enquiry_table.DoesNotExist:
            messages.error(request, 'Record does not exist.')
    return HttpResponseRedirect('/dashboard/')

def edit_record(request, id):
    info = get_object_or_404(enquiry_table, pk=id)
    data = {'information': info}
    return render(request, 'editrecord.html', data)

def update_record(request, id):
    if request.method == 'POST':
        info = get_object_or_404(enquiry_table, pk=id)
        info.name = request.POST.get('name')
        info.email = request.POST.get('email')
        info.phone = request.POST.get('phone')
        info.message = request.POST.get('message')
        info.save()
        messages.success(request, 'Record updated successfully.')
        return redirect('dashboard')
    return HttpResponseRedirect('/dashboard/')
