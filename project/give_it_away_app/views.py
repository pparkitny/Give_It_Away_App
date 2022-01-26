from django.shortcuts import render
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Category, Institution, Donation
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from .forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, logout


class LandingPageView(View):
    def get(self, request):
        sum_of_bags = 0

        donations = Donation.objects.all()
        for donation in donations:  # count number of bags
            sum_of_bags += donation.quantity

        list_of_donated_institutions = []
        for donation in donations:
            if donation.institution in list_of_donated_institutions:
                pass
            else:
                list_of_donated_institutions.append(donation.institution)
            number_of_donated_institutions = len(list_of_donated_institutions)

        page_num = request.GET.get('page')

        fundations = Institution.objects.filter(type=1)
        fundations_paginator = Paginator(fundations, 5)
        fundations_page = fundations_paginator.get_page(page_num)

        non_gov_org = Institution.objects.filter(type=2)
        non_gov_org_paginator = Paginator(non_gov_org, 5)
        non_gov_org_page = non_gov_org_paginator.get_page(page_num)

        local_collections = Institution.objects.filter(type=3)
        local_collections_paginator = Paginator(local_collections, 5)
        local_collections_page = local_collections_paginator.get_page(page_num)

        ctx = {'sum_of_bags': sum_of_bags,
               'number_of_donated_institutions': number_of_donated_institutions,
               'fundations_page': fundations_page,
               'non_gov_org_page': non_gov_org_page,
               'local_collections_page': local_collections_page}

        return render(request, 'index.html', ctx)

    def post(self, request):
        return render(request, 'index.html')


class AddDonationView(View):
    def get(self, request):
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        institution_categories = Institution.categories.through.objects.all()
        ctx = {'categories': categories, 'institutions': institutions, 'institution_categories': institution_categories}
        return render(request, 'form.html', ctx)

    def post(self, request):
        quantity = request.POST.get('bags')
        institution = Institution.objects.get(name=request.POST.get('organization'))
        address = request.POST.get('address')
        city = request.POST.get('city')
        zip_code = request.POST.get('postcode')
        phone_number = request.POST.get('phone')
        pick_up_date = request.POST.get('date')
        pick_up_time = request.POST.get('time')
        pick_up_comment = request.POST.get('more_info')
        user = request.user
        donation = Donation.objects.create(
            quantity=quantity,
            institution=institution,
            address=address,
            city=city,
            zip_code=zip_code,
            phone_number=phone_number,
            pick_up_date=pick_up_date,
            pick_up_time=pick_up_time,
            pick_up_comment=pick_up_comment,
            user=user
        )

        checked_categories = request.POST.get('checked_categories_backend').split(',')
        for category in checked_categories:
            Donation.categories.through.objects.create(
                donation=donation,
                category=Category.objects.get(id=category)
            )

        return render(request, 'form-confirmation.html')


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        form.is_valid()
        user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])
        if user:  # user is in database
            login(request, user)  # from django.contrib.auth import login
            return redirect('/')
        else:  # user is None
            message = 'Zły email lub hasło'
            return render(request, 'login.html', {'form': form, 'message': message})


class LogoutView(View):
    """ This class is used to logout users"""
    def get(self, request):
        logout(request)  # from django.contrib.auth import logout
        return redirect('/')


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})

    @csrf_exempt
    def post(self, request):
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['email'],
                                            password=form.cleaned_data['password1'],
                                            first_name=form.cleaned_data['first_name'],
                                            last_name=form.cleaned_data['last_name'],
                                            email=form.cleaned_data['email'])
            user.save()
            return redirect('/login/')
        else:
            return render(request, 'register.html', {'form': form})


class MainSiteView(View):
    def get(self, request):
        donations = Donation.objects.all().order_by('pick_up_date').order_by('pick_up_time')
        ctx = {'donations': donations}
        return render(request, 'main-site.html', ctx)
