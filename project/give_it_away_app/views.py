from django.shortcuts import render
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Category, Institution, Donation


class LandingPageView(View):
    def get(self, request):
        number_of_donations = Donation.objects.count()
        sum_of_bags = 0
        for i in range(number_of_donations + 1): # count number of bags
            if i == 0:
                pass
            else:
                obj = Donation.objects.get(id=i)
                sum_of_bags += obj.quantity

        list_of_donated_institutions = []
        for i in range(number_of_donations + 1):
            if i == 0:
                pass
            else:
                obj = Donation.objects.get(id=i)
                if obj.institution in list_of_donated_institutions:
                    pass
                else:
                    list_of_donated_institutions.append(obj.institution)
                number_of_donated_institutions = len(list_of_donated_institutions)

        all_institutions = Institution.objects.all()

        ctx = {'sum_of_bags': sum_of_bags, 'number_of_donated_institutions': number_of_donated_institutions,
               'all_institutions': all_institutions}

        return render(request, 'index.html', ctx)

    def post(self, request):
        return render(request, 'index.html')


class AddDonationView(View):
    def get(self, request):
        return render(request, 'form.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

